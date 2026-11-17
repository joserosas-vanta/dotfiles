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


def binary_metadata_tasks():
    tasks = yaml.safe_load(TASKS_PATH.read_text())
    names = (
        "pi | set version facts",
        "pi | fail when latest version is unavailable",
        "pi | resolve release asset metadata",
        "pi | extract release asset digest",
        "pi | fail when release asset metadata is missing",
        "pi | fail when digest is invalid",
    )
    selected = [task_by_name(tasks, name) for name in names]
    selected.append({
        "name": "report binary metadata",
        "ansible.builtin.debug": {
            "msg": (
                "BINARY version={{ pi_coding_agent_latest_version }} "
                "sha256={{ pi_coding_agent_sha256 }}"
            ),
        },
    })
    return selected


def node_bootstrap_tasks():
    tasks = yaml.safe_load(TASKS_PATH.read_text())
    failure = task_by_name(tasks, "pi | fail when npm and Volta are unavailable")
    install = task_by_name(tasks, "pi | install Node LTS through Volta when npm is unavailable")
    install.pop("ansible.builtin.command")
    for key in ("become", "become_user", "environment", "changed_when"):
        install.pop(key, None)
    install["ansible.builtin.debug"] = {"msg": "NODE_BOOTSTRAP"}
    return [failure, install, {
        "name": "report package manager readiness",
        "ansible.builtin.debug": {"msg": "NODE_READY"},
    }]


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
    def run_node_case(self, *, npm_status, volta_status, succeeds, bootstraps):
        play = [{
            "hosts": "localhost",
            "gather_facts": False,
            "vars": {
                "pi_managed_source_packages": [{}],
                "pi_managed_source_package_npm_check": {"rc": npm_status},
                "pi_managed_source_package_volta_check": {"rc": volta_status},
            },
            "tasks": node_bootstrap_tasks(),
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
        self.assertEqual("NODE_BOOTSTRAP" in output, bootstraps, output)
        self.assertEqual("NODE_READY" in output, succeeds, output)

    def run_binary_case(self, variables, *, succeeds, result=None):
        play = [{
            "hosts": "localhost",
            "gather_facts": False,
            "vars": variables,
            "tasks": binary_metadata_tasks(),
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
            self.assertNotIn("BINARY version=", output)
        else:
            self.assertIn(result, output)

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

    def test_binary_metadata_avoids_api_rate_limits_and_validates_checksum(self):
        tasks = yaml.safe_load(TASKS_PATH.read_text())
        role_source = TASKS_PATH.read_text()
        variables = yaml.safe_load((ROOT / "group_vars/all.yml").read_text())
        lookup = task_by_name(tasks, "pi | list release tags")
        self.assertEqual(lookup["ansible.builtin.command"]["argv"][:5],
                         ["git", "ls-remote", "--tags", "--refs", "--sort=-v:refname"])
        self.assertNotIn("api.github.com", role_source)
        self.assertEqual(variables["pi_coding_agent_repository_url"],
                         "https://github.com/earendil-works/pi")

        digest = "a" * 64
        base = {
            "pi_coding_agent_repository_url": variables["pi_coding_agent_repository_url"],
            "pi_coding_agent_asset_name": "pi-linux-x64.tar.gz",
            "pi_coding_agent_version_check": {"stdout": "0.85.1"},
            "pi_coding_agent_release_tags": {
                "stdout_lines": [
                    "abc refs/tags/v1.5.2",
                    "def refs/tags/v1.6.0-beta.1",
                ],
                "stderr": "",
            },
            "pi_coding_agent_checksums": {
                "content": f"{digest}  pi-linux-x64.tar.gz\n",
            },
        }
        self.run_binary_case(
            base,
            succeeds=True,
            result=f"BINARY version=1.5.2 sha256={digest}",
        )
        missing_checksum = dict(base)
        missing_checksum["pi_coding_agent_checksums"] = {"content": ""}
        self.run_binary_case(missing_checksum, succeeds=False)
        missing_release = dict(base)
        missing_release["pi_coding_agent_release_tags"] = {
            "stdout_lines": [],
            "stderr": "offline",
        }
        self.run_binary_case(missing_release, succeeds=False)

    def test_node_bootstrap_paths(self):
        self.run_node_case(npm_status=0, volta_status=1, succeeds=True, bootstraps=False)
        self.run_node_case(npm_status=1, volta_status=0, succeeds=True, bootstraps=True)
        self.run_node_case(npm_status=1, volta_status=1, succeeds=False, bootstraps=False)

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
        volta_check = task_by_name(tasks, "pi | check Volta when npm is unavailable")
        self.assertIn("pi_managed_source_package_npm_check.rc != 0", volta_check["when"])
        tool_failure = task_by_name(tasks, "pi | fail when npm and Volta are unavailable")
        self.assertIn("pi_managed_source_package_volta_check.rc | default(1) != 0",
                      tool_failure["when"])
        node_install = task_by_name(
            tasks, "pi | install Node LTS through Volta when npm is unavailable")
        self.assertEqual(node_install["ansible.builtin.command"]["argv"],
                         ["volta", "install", "node@lts"])
        npm_failure = task_by_name(tasks, "pi | fail when npm remains unavailable")
        self.assertIn("pi_managed_source_package_npm_verified.rc != 0", npm_failure["when"])
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
