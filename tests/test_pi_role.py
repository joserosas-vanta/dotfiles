"""Validate Pi defaults and release resolution without installing Pi or packages.

Static checks protect the pinned package contract. A reduced Ansible play exercises
latest-release, offline fallback, explicit-pin, and fresh-offline failure branches.
"""

import pathlib
import re
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "roles/pi/tasks/main.yml"


def task_by_name(tasks, name):
    matches = [task for task in tasks if task.get("name") == name]
    assert len(matches) == 1
    return dict(matches[0])


def release_resolution_tasks():
    tasks = yaml.safe_load(TASKS_PATH.read_text())
    names = (
        "pi | pick latest local pi-guides release",
        "pi | fail when no local pi-guides release can be resolved",
        "pi | warn when keeping the installed local pi-guides release",
        "pi | resolve local pi-guides checkout ref",
        "pi | set expected local pi-guides version",
    )
    selected = [task_by_name(tasks, name) for name in names]
    selected.append({
        "name": "report resolved release",
        "ansible.builtin.debug": {
            "msg": (
                "RESULT ref={{ pi_guides_resolved_local_checkout_ref }} "
                "version={{ pi_guides_expected_version }}"
            ),
        },
    })
    return selected


class PiRoleTests(unittest.TestCase):
    def run_release_case(self, variables, *, succeeds, result=None):
        case_variables = {
            "pi_guides_enable_global": True,
            "pi_guides_source_kind": "local",
            "pi_guides_manage_local_checkout": True,
            **variables,
        }
        play = [{
            "hosts": "localhost",
            "gather_facts": False,
            "vars": case_variables,
            "tasks": release_resolution_tasks(),
        }]
        with tempfile.TemporaryDirectory() as directory:
            playbook = pathlib.Path(directory) / "play.yml"
            playbook.write_text(yaml.safe_dump(play))
            process = subprocess.run(
                ["ansible-playbook", "--inventory", "localhost,", "--connection", "local",
                 str(playbook)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        output = process.stdout + process.stderr
        self.assertEqual(process.returncode == 0, succeeds, output)
        if result is None:
            self.assertNotIn("RESULT ref=", output)
        else:
            self.assertIn(result, output)
        return output

    def test_upstream_pi_defaults_with_fork_guide_source(self):
        variables = yaml.safe_load((ROOT / "group_vars/all.yml").read_text())
        self.assertEqual(variables["pi_default_provider"], "claude-bridge")
        self.assertEqual(variables["pi_default_model"], "claude-opus-5-5")
        self.assertIn("claude-bridge/claude-opus-5-5", variables["pi_enabled_models"])
        self.assertIn("openai-codex/gpt-6.1-sol", variables["pi_enabled_models"])
        self.assertIn("kimi-for-coding", variables["pi_enabled_models"])
        self.assertEqual(variables["pi_guides_local_checkout_ref"], "")
        self.assertIn("joserosas-vanta/vpi-guides", variables["pi_guides_local_checkout_repo"])

    def test_managed_packages_are_complete_and_commit_pinned(self):
        variables = yaml.safe_load((ROOT / "group_vars/all.yml").read_text())
        packages = variables["pi_managed_source_packages"]
        self.assertEqual([package["name"] for package in packages],
                         ["pi-claude-bridge"])
        for package in packages:
            self.assertRegex(package["ref"], re.compile(r"^[0-9a-f]{40}$"))
            self.assertTrue(package["repo"].startswith("https://github.com/"))
            self.assertTrue(package["dependency_marker"])
            self.assertTrue(package["install_command"].startswith("npm ci "))

    def test_release_lookup_contract_is_bounded_and_fail_closed(self):
        tasks = yaml.safe_load(TASKS_PATH.read_text())
        lookup = task_by_name(tasks, "pi | list local pi-guides release tags")
        self.assertEqual(lookup["ansible.builtin.command"]["argv"][:5],
                         ["git", "ls-remote", "--tags", "--refs", "--sort=-v:refname"])
        self.assertFalse(lookup["failed_when"])
        self.assertFalse(lookup["changed_when"])
        failure = task_by_name(tasks, "pi | fail when no local pi-guides release can be resolved")
        self.assertIn("pi_guides_local_installed_version | default('') | length == 0",
                      failure["when"])
        npm_check = task_by_name(tasks, "pi | check npm for managed source packages")
        self.assertIn(".volta/bin", npm_check["environment"]["PATH"])
        npm_failure = task_by_name(
            tasks, "pi | fail when npm is unavailable for managed source packages")
        self.assertIn("pi_managed_source_package_npm_check.rc != 0", npm_failure["when"])
        sync = task_by_name(tasks, "pi | sync managed local pi-guides checkout")
        self.assertIn("pi_guides_local_latest_tag", sync["when"][-1])

    def test_latest_release_and_explicit_pin(self):
        base = {
            "pi_guides_local_installed_version": "",
            "pi_guides_local_release_tags": {
                "stdout_lines": ["abc refs/tags/v0.7.0", "def refs/tags/not-semver"],
                "stderr": "",
            },
        }
        self.run_release_case(
            dict(base, pi_guides_local_checkout_ref=""),
            succeeds=True,
            result="RESULT ref=v0.7.0 version=0.7.0",
        )
        self.run_release_case(
            {
                "pi_guides_local_checkout_ref": "v0.6.0",
                "pi_guides_local_release_tags": {},
            },
            succeeds=True,
            result="RESULT ref=v0.6.0 version=0.6.0",
        )

    def test_offline_existing_install_and_fresh_failure(self):
        release_tags = {"stdout_lines": [], "stderr": "offline"}
        output = self.run_release_case(
            {
                "pi_guides_local_checkout_ref": "",
                "pi_guides_local_installed_version": "0.6.0",
                "pi_guides_local_release_tags": release_tags,
            },
            succeeds=True,
            result="RESULT ref=HEAD version=0.6.0",
        )
        self.assertIn("keeping installed v0.6.0", output)
        self.run_release_case(
            {
                "pi_guides_local_checkout_ref": "",
                "pi_guides_local_installed_version": "",
                "pi_guides_local_release_tags": release_tags,
            },
            succeeds=False,
        )


if __name__ == "__main__":
    unittest.main()
