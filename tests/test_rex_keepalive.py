"""Offline keep-alive tests; never contact Ona or signal real processes."""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

SCRIPT = Path(__file__).resolve().parents[1] / 'roles/rex/files/ona-rex-keepalive'
loader = importlib.machinery.SourceFileLoader('rex_keepalive', str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
helper = importlib.util.module_from_spec(spec)
loader.exec_module(helper)


class KeepaliveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for target, value in [('ROOT', self.root), ('identity', Mock(return_value='boot:start'))]:
            p = patch.object(helper, target, value)
            p.start()
            self.addCleanup(p.stop)
        p = patch.object(helper.os, 'getuid', return_value=1000)
        p.start()
        self.addCleanup(p.stop)

    def test_ensure_is_opt_in(self):
        with patch.object(helper.subprocess, 'run') as run:
            helper.main('ensure')
            run.assert_not_called()
        self.assertFalse((self.root / 'enabled').exists())

    def test_reused_pid_is_not_killed(self):
        with patch.object(helper.os, 'kill') as kill:
            helper.stop({'pid': 42, 'identity': 'old-boot:start'})
            kill.assert_not_called()

    def test_stop_removes_preference_without_touching_rex(self):
        (self.root / 'enabled').touch()
        (self.root / 'process.json').write_text(json.dumps({'pid': 42, 'identity': 'old'}))
        with patch.object(helper.os, 'kill') as kill:
            helper.main('stop')
            kill.assert_not_called()
        self.assertFalse((self.root / 'enabled').exists())

    def test_enable_missing_cli_does_not_opt_in(self):
        with patch.object(helper.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(RuntimeError, 'CLI missing'):
                helper.main('enable')
        self.assertFalse((self.root / 'enabled').exists())

    def test_failed_rex_status_does_not_launch_watcher(self):
        with patch.object(helper.shutil, 'which', return_value='/bin/ona'), \
             patch.object(helper.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'rex')), \
             patch.object(helper.subprocess, 'Popen') as spawn:
            with self.assertRaises(subprocess.CalledProcessError):
                helper.main('enable')
            spawn.assert_not_called()

    def test_duplicate_enable_reuses_watcher(self):
        state = {'pid': 42, 'identity': 'boot:start', 'rex_pid': 99, 'rex_identity': 'boot:start'}
        (self.root / 'process.json').write_text(json.dumps(state))
        with patch.object(helper.shutil, 'which', return_value='/bin/ona'), \
             patch.object(helper.subprocess, 'run', return_value=Mock(stdout='pid: 99\n')), \
             patch.object(helper.subprocess, 'Popen') as spawn:
            helper.main('enable')
            spawn.assert_not_called()
        self.assertTrue((self.root / 'enabled').exists())

    def test_launch_is_detached_and_records_preference(self):
        process = Mock(pid=42)
        process.poll.return_value = None
        with patch.object(helper.shutil, 'which', return_value='/bin/ona'), \
             patch.object(helper.subprocess, 'run', return_value=Mock(stdout='pid: 99\n')), \
             patch.object(helper.subprocess, 'Popen', return_value=process) as spawn, \
             patch.object(helper.time, 'sleep'):
            helper.main('enable')
            self.assertTrue(spawn.call_args.kwargs['start_new_session'])
            self.assertIn('99', spawn.call_args.args[0])
        self.assertTrue((self.root / 'enabled').exists())

    def test_immediate_failure_does_not_opt_in(self):
        process = Mock(pid=42)
        process.poll.return_value = 1
        with patch.object(helper.shutil, 'which', return_value='/bin/ona'), \
             patch.object(helper.subprocess, 'run', return_value=Mock(stdout='pid: 99\n')), \
             patch.object(helper.subprocess, 'Popen', return_value=process), \
             patch.object(helper.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'exited'):
                helper.main('enable')
        self.assertFalse((self.root / 'enabled').exists())


if __name__ == '__main__':
    unittest.main()
