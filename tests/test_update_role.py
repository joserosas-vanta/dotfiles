"""Exercise real Ansible branching with simulated I/O, never upgrading the test host.

Cover both distros, absent/incomplete Nix, missing lock, unsupported OS, and failures
at each mutation step. Assertions check that later effects never follow a failure.
Run with /usr/bin/python3 -m unittest discover -s tests -v.
"""

import pathlib
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


def simulated_tasks(*, nix_exists, files_exist, executable, failure):
    tasks = yaml.safe_load((ROOT / "roles/update/tasks/main.yml").read_text())
    apply_tasks = yaml.safe_load((ROOT / "roles/nix/tasks/apply.yml").read_text())
    tasks[-1:] = [dict(task, when=[tasks[-1]["when"], task["when"]]) for task in apply_tasks]
    events = iter(["lock", "apply", "apply_root"])
    for task in tasks:
        # Reject OS mutations before executing even a simulated playbook.
        assert "ansible.builtin.apt" not in task
        assert "community.general.pacman" not in task
        assert "ansible.builtin.package" not in task
        if "ansible.builtin.stat" in task:
            variable = task.pop("register")
            task.pop("ansible.builtin.stat")
            task.pop("loop", None)
            value = {"stat": {"exists": nix_exists, "executable": executable, "path": "/test/nix"}}
            if variable == "update_home_manager_files":
                value = {"results": [{"stat": {"isreg": exists}} for exists in files_exist]}
            task["ansible.builtin.set_fact"] = {variable: value}
        for module in ("ansible.builtin.shell",):
            if module not in task:
                continue
            task.pop(module)
            for key in ("args", "register", "changed_when", "become_user", "become"):
                task.pop(key, None)
            event = next(events)
            replacement = "ansible.builtin.fail" if event == failure else "ansible.builtin.debug"
            task[replacement] = {"msg": "EVENT:" + event}
    return tasks


class UpdateRoleTests(unittest.TestCase):
    def run_case(self, *, distro="ubuntu", nix_exists=True, files_exist=(True, True),
                 executable=True, failure=None, expected=(), succeeds=True, root_runner=False):
        tasks = simulated_tasks(nix_exists=nix_exists, files_exist=files_exist,
                                executable=executable, failure=failure)
        play = [{"hosts": "localhost", "gather_facts": False, "vars": {
            "facts_is_ubuntu": distro in ("ubuntu", "both"),
            "facts_is_arch": distro in ("arch", "both"),
            "nix_requires_root_runner": root_runner,
        }, "tasks": tasks}]

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
        if nix_exists is False:
            self.assertIn("no packages were updated", output)
            self.assertIn("Run dotfiles -t nix first", output)
        for event in ("apt", "pacman", "lock", "apply", "apply_root"):
            self.assertEqual('"EVENT:' + event + '"' in output, event in expected, output)

    def test_platforms_and_absent_nix(self):
        for distro in ("ubuntu", "arch"):
            with self.subTest(distro=distro):
                self.run_case(distro=distro, expected=("lock", "apply"))
                self.run_case(distro=distro, nix_exists=False, expected=())

    def test_preflight_rejections_have_no_effects(self):
        for distro in ("unsupported", "both"):
            self.run_case(distro=distro, succeeds=False)
        self.run_case(executable=False, succeeds=False)
        for files in ((False, True), (True, False), (False, False)):
            self.run_case(files_exist=files, succeeds=False)

    def test_failures_stop_later_effects(self):
        for distro in ("ubuntu", "arch"):
            self.run_case(distro=distro, failure="lock", expected=("lock",), succeeds=False)
            self.run_case(distro=distro, failure="apply", expected=("lock", "apply"), succeeds=False)

    def test_root_runner_paths(self):
        self.run_case(root_runner=True, expected=("lock", "apply_root"))
        self.run_case(root_runner=True, failure="lock", expected=("lock",), succeeds=False)
        self.run_case(root_runner=True, failure="apply_root",
                      expected=("lock", "apply_root"), succeeds=False)

    def test_opt_in_and_module_contracts(self):
        defaults = yaml.safe_load((ROOT / "group_vars/all.yml").read_text())
        self.assertNotIn("update", defaults["default_roles"])
        tasks = yaml.safe_load((ROOT / "roles/update/tasks/main.yml").read_text())
        for task in tasks:
            self.assertIn("update", task["tags"])
        for task in tasks:
            self.assertNotIn("ansible.builtin.apt", task)
            self.assertNotIn("community.general.pacman", task)
            self.assertNotIn("ansible.builtin.package", task)
        lock = next(task for task in tasks if "ansible.builtin.shell" in task)
        self.assertNotIn("creates", lock["args"])  # Missing and existing locks both update.
        self.assertEqual(lock["become_user"],
                         "{{ 'root' if nix_requires_root_runner | default(false) else host_user }}")
        self.assertIn("set -e", lock["ansible.builtin.shell"])
        self.assertEqual(tasks[-1]["ansible.builtin.import_role"]["tasks_from"], "apply")


if __name__ == "__main__":
    unittest.main()
