# work dotfiles

Supported OS:
- Arch Linux
- Ubuntu LTS (Ona/Gitpod-focused)

## Usage

### Install

This playbook includes a custom shell script located at `bin/dotfiles`. After the first run, it is
available as `dotfiles` via `~/.local/bin/dotfiles` and can be run multiple times while making sure any
Ansible dependencies are installed and updated.

`bin/dotfiles` detects the distro and installs the required dependencies for Arch or Ubuntu.

This repo is work-VM-first for Ona/Gitpod-style Ubuntu workspaces. The default target user is
`vscode`, and the normal path configures that existing workspace account instead of creating named
local users.

> [!NOTE]
> This fork does not depend on 1Password secrets for normal operation.

```bash
bash -c "$(
  curl -fsSL https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles || \
  wget -qO- https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles
)"
```

`bin/dotfiles` handles the following during install/update:

- Installs base Ubuntu dependencies needed to run the playbook
- Clones this repository into `~/.local/share/dotfiles`
- Links `dotfiles` into `~/.local/bin/dotfiles`
- Runs the playbook against `vscode` by default

If you want to run only a specific role, you can specify the following bash command:
```bash
curl -fsSL https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles | \
  bash -s -- -t zsh
```

### Update

This repository is continuously updated with new features and settings which become available to
you when updating.

To update your environment run the `dotfiles` command in your shell:

```bash
dotfiles
```

This will handle the following tasks:

- Verify Ansible is up-to-date
- Clone this repository locally to `~/.local/share/dotfiles`
- Run this playbook with the values in `group_vars/all.yml`

This `dotfiles` command is available after the first run via `~/.local/bin/dotfiles`, allowing
you to call `dotfiles` from anywhere.

Any flags or arguments you pass to the `dotfiles` command are passed as-is to the
`ansible-playbook` command.

To target a different account, pass `-u <user>`.

For example: running the `zsh` role with verbosity
```bash
dotfiles -t zsh -vvv
```

As an added bonus, the tags have tab completion!
```bash
dotfiles -t <tab><tab>
dotfiles -t t<tab>
dotfiles -t ne<tab>
```

### Claude Code and package updates

The Nix role owns package configuration. Claude Code uses a separate `nixos-unstable`
input, pinned by the deployed `~/.config/home-manager/flake.lock`. Other packages and
Home Manager remain on the configured stable release (currently 25.11). Claude Code
is required: a missing package fails evaluation instead of silently omitting installation.

Deploy the new templates before refreshing packages, as the target user (default `vscode`):

```bash
dotfiles -t nix
dotfiles -t update
```

`update` is opt-in, never part of a normal `dotfiles` run. It:

- Rejects unsupported platforms and incomplete detected Nix/Home Manager configurations
  before upgrading packages.
- Updates only Nix packages; it never invokes apt or pacman on Ubuntu or Arch.
  This replaces the earlier OS-plus-Nix behavior; manage OS upgrades separately.
- Refreshes all deployed flake inputs within their configured branches, including Claude Code,
  then activates Home Manager. It does not deploy templates or change stable release pins.
- Reports a no-op when no Nix installation is detected; run `dotfiles -t nix` first.
- Preserves this fork's single-user, daemon, and root-runner behavior. Root-runner lock
  updates restore the target user's ownership even when the Nix command fails.

Failures stop later steps, but updates are not transactional: lock changes
can persist if activation fails. Before updating, the operator should save the deployed lock
and record the current Home Manager generation (`home-manager generations`). On failure,
stop and inspect the error; restore the saved lock and activate the previous generation
before retrying if necessary. OS packages are not modified by this role.
No automatic rollback is performed. First run on a disposable work VM before wider use.

Unlike upstream, this port does not include the release-reminder network lookup or the
26.05 release upgrade. Reverting the Claude source change requires restoring both templates
and reapplying the Nix role; do not restore only one template.

Offline regression checks (Python requires Jinja2 and PyYAML; Ansible and Nix must be on PATH):

```bash
python3 -m unittest discover -s tests -v
```

Tests use stub package sets and simulated upgrades; they do not install packages or validate
real package builds or activation rollback.

## Upstream Drift Workflow

This repository is a fork and **must** be kept intentionally aware of drift from
`sillypoise/sp-dotfiles`.

Before or after any non-trivial role/config change (especially `pi`, `zsh`, `nix`, or
`media-tools`), run a drift check and update the tracker:

```bash
cd ~/.local/share/dotfiles
git fetch upstream
git rev-list --left-right --count main...upstream/main
git log --oneline --no-merges main..upstream/main
```

Then record decisions in `docs/upstream-drift.md`:

- add new upstream commits that are candidates for porting
- mark items as `planned`, `ported`, or `skipped`
- include a short rationale for each decision

## Pi Guides

The `pi` role owns pi installation and the global pi baseline.

Current distribution model:

- pi itself is installed globally
- `~/.pi/agent/settings.json` is managed by the `pi` role
- the global settings baseline currently comes from:
  - `pi_default_provider`
  - `pi_default_model`
  - `pi_default_thinking_level`
  - `pi_enabled_models`
  - `pi_extra_packages`
  - `pi_managed_source_packages` (empty by default in this fork)
- optional global registration of the work `pi-guides` package is controlled by:
  - `pi_guides_enable_global`
  - `pi_guides_source`
- when global guides are enabled, the role manages both:
  - shared system prompt additions in `~/.pi/agent/APPEND_SYSTEM.md`
  - declared global settings in `~/.pi/agent/settings.json`
  - the local checkout state under `{{ host_user_home }}/pi-guides`

The managed local checkout currently uses:

- repo: `https://github.com/joserosas-vanta/vpi-guides.git`
- ref: `main`

Recommended usage:

- run `dotfiles -t pi` to install or update pi plus the managed local guides checkout
- use `/guide-init --no-settings` in repos when the package is already available globally
- commit `.pi/guides.json` in repos that should activate a specific guide profile
- use `/guide-init --dev` for local package testing; `PI_GUIDES_DEV_SOURCE` defaults to `$HOME/pi-guides`

Important nuance:

- global package install makes guide tooling available everywhere
- guides only become active in a repo when that repo has `.pi/guides.json`
- git in `/workspaces/*` repos is configured to ignore `.pi/` directories by default

## Default Roles

This fork currently runs the following roles by default:

- `bash`
- `zsh`
- `nix`
- `git` (`gh` CLI and config only)
- `c`
- `nvim`
- `opencode`
- `pi`
- `zellij`
- `btop`

The following additional roles are opt-in and are not part of the default work-VM path:

- `bootstrap` (base distro packages)
- `users`
- `ssh`
- `openssh`
- `ufw`
- `tailscale`
- `media-tools`
- `volta`

The repo no longer creates the old named personal users during bootstrap.

## OpenCode

This fork installs OpenCode and writes baseline local config under
`~/.config/opencode`.

It does not auto-clone private OpenCode guides and does not configure
OpenCode server secrets/services.

To install or update OpenCode in your environment, run:

```bash
dotfiles -t opencode
```
