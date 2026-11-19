"""Exercise the Rex upgrade tasks with simulated commands, never touching the test host.

Cover a missing binary, an upgrade with a server still on the old version, an
up-to-date server, no running server, and installer failure. Static checks ensure
the tasks never stop a server and never start one by accident.
"""

import pathlib
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "roles/update/tasks/rex.yml"

OLD = "0.0.1793632279-ge7974b"
NEW = "0.0.1795103044-gcbde95"


def version_output(version):
    return f"rex {version}\ncommit: abc\napi: revision 19 (supports 0 to 19)\n"


def simulated_tasks(*, installed, before, after, server, install_fails):
    tasks = yaml.safe_load(TASKS_PATH.read_text())
    results = {
        "update_rex_binary": {"stat": {"exists": installed}},
        "update_rex_before": {"stdout": version_output(before), "rc": 0},
        "update_rex_after": {"stdout": version_output(after), "rc": 0},
        "update_rex_server": (
            {"rc": 0, "stdout": f"pid: 1\nversion: {server}\nsessions: 1\n"}
            if server else {"rc": 1, "stdout": ""}
        ),
    }
    for task in tasks:
        for module in ("ansible.builtin.stat", "ansible.builtin.command",
                       "ansible.builtin.get_url"):
            if module not in task:
                continue
            task.pop(module)
            for key in ("become", "become_user", "environment", "changed_when", "failed_when"):
                task.pop(key, None)
            variable = task.pop("register", None)
            if variable:
                task["ansible.builtin.set_fact"] = {variable: results[variable]}
            elif "install latest release" in task["name"] and install_fails:
                task["ansible.builtin.fail"] = {"msg": "EVENT:install"}
            else:
                task["ansible.builtin.debug"] = {"msg": "EVENT:" + task["name"]}
    return tasks


class UpdateRexTests(unittest.TestCase):
    def run_case(self, *, installed=True, before=OLD, after=NEW, server=OLD,
                 install_fails=False, succeeds=True):
        tasks = simulated_tasks(installed=installed, before=before, after=after,
                                server=server, install_fails=install_fails)
        play = [{"hosts": "localhost", "gather_facts": False,
                 "vars": {"host_user": "vscode", "host_user_home": "/home/vscode"},
                 "tasks": tasks}]
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "play.yml"
            path.write_text(yaml.safe_dump(play))
            result = subprocess.run(
                ["ansible-playbook", "--inventory", "localhost,",
                 "--connection", "local", str(path)],
                cwd=ROOT, capture_output=True, text=True, timeout=60, check=False,
            )
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode == 0, succeeds, output)
        return output

    def test_missing_binary_skips_everything(self):
        output = self.run_case(installed=False)
        self.assertIn("Run dotfiles -t rex first", output)
        self.assertNotIn("EVENT:", output)

    def test_upgrade_leaves_old_server_running(self):
        output = self.run_case()
        self.assertIn(f"upgraded from {OLD} to {NEW}", output)
        self.assertIn(f"still on {OLD} and was not restarted", output)
        self.assertIn("changed=1", output)

    def test_up_to_date_server(self):
        output = self.run_case(before=NEW, server=NEW)
        self.assertIn(f"already at {NEW}", output)
        self.assertIn("The running server already uses it", output)
        self.assertIn("changed=0", output)

    def test_no_running_server(self):
        output = self.run_case(server=None)
        self.assertIn("No Rex server is running", output)

    def test_installer_failure_stops_before_report(self):
        output = self.run_case(install_fails=True, succeeds=False)
        self.assertNotIn("Rex binary", output)

    def test_never_stops_or_autostarts_a_server(self):
        tasks = yaml.safe_load(TASKS_PATH.read_text())
        for task in tasks:
            self.assertIn("update", task["tags"])
            argv = task.get("ansible.builtin.command", {}).get("argv", [])
            self.assertNotIn("stop", argv)
            self.assertNotIn("start", argv)
        status = next(task for task in tasks if task["name"].endswith("running server version"))
        self.assertIn("--autostart=false", status["ansible.builtin.command"]["argv"])
        self.assertEqual(status["become_user"], "{{ host_user }}")
        main = yaml.safe_load((ROOT / "roles/update/tasks/main.yml").read_text())
        self.assertEqual(main[1]["ansible.builtin.import_tasks"], "rex.yml")


if __name__ == "__main__":
    unittest.main()
