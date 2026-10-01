"""Run rendered update scripts with local stubs; never invoke Nix or change ownership.

Exercise missing/existing locks, daemon/single-user/root runners, and failure cleanup.
"""

import os
import pathlib
import shlex
import subprocess
import tempfile
import unittest

from jinja2 import Environment, StrictUndefined
import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


class UpdateShellTests(unittest.TestCase):
    def run_case(self, *, root_runner=False, daemon=False, lock_exists=False,
                 update_status=0, ownership_status=0):
        tasks = yaml.safe_load((ROOT / "roles/update/tasks/main.yml").read_text())
        task = next(task for task in tasks if "ansible.builtin.shell" in task)
        environment = Environment(undefined=StrictUndefined)
        environment.filters["quote"] = shlex.quote
        with tempfile.TemporaryDirectory(prefix="update test ") as directory:
            root = pathlib.Path(directory)
            binary = root / "nix"
            binary.write_text(
                '#!/bin/bash\nset -e\n'
                'printf "%s|%s|%s\\n" "$*" "$HOME" "${NIX_REMOTE-unset}" > invocation\n'
                f'printf "updated" > flake.lock\nexit {update_status}\n'
            )
            binary.chmod(0o755)
            ownership = root / "chown"
            ownership.write_text(
                '#!/bin/bash\nprintf "%s\\n" "$*" > ownership\n'
                f'exit {ownership_status}\n'
            )
            ownership.chmod(0o755)
            if lock_exists:
                (root / "flake.lock").write_text("old")
            script = environment.from_string(task["ansible.builtin.shell"]).render(
                nix_runtime_profile_script="",
                nix_install_mode="daemon" if daemon else "single-user",
                host_user="vscode", host_user_home=directory, nix_binary_path=str(binary),
                nix_requires_root_runner=root_runner,
            )
            process_environment = dict(os.environ, PATH=directory + ":" + os.environ["PATH"])
            process_environment.pop("NIX_REMOTE", None)
            result = subprocess.run(["/bin/bash", "-c", script], cwd=root,
                                    env=process_environment, capture_output=True, text=True,
                                    timeout=10, check=False)
            self.assertEqual(result.returncode, ownership_status or update_status, result.stderr)
            self.assertEqual((root / "flake.lock").read_text(), "updated")
            self.assertEqual((root / "invocation").read_text().strip(),
                             f'flake update|{directory}|{"daemon" if daemon else "unset"}')
            self.assertEqual((root / "ownership").exists(), root_runner)
            if root_runner:
                self.assertEqual((root / "ownership").read_text().strip(),
                                 "vscode:vscode flake.lock")

    def test_runtime_modes_and_lock_boundaries(self):
        for root_runner, daemon in ((False, False), (False, True), (True, False)):
            for lock_exists in (False, True):
                with self.subTest(root=root_runner, daemon=daemon, lock=lock_exists):
                    self.run_case(root_runner=root_runner, daemon=daemon, lock_exists=lock_exists)

    def test_failure_status_and_ownership_cleanup(self):
        self.run_case(update_status=7)
        self.run_case(root_runner=True, update_status=7)
        self.run_case(root_runner=True, ownership_status=9)


if __name__ == "__main__":
    unittest.main()
