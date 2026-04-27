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
> 1Password support is preserved, but authentication is optional for a successful base install.
> Secret-backed functionality continues to work when `op` is available and authenticated.

```bash
bash -c "$(
  curl -fsSL https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles || \
  wget -qO- https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles
)"
```

For headless installs using a 1Password service account token:
```bash
OP_SERVICE_ACCOUNT_TOKEN=... bash -c "$(
  curl -fsSL https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles || \
  wget -qO- https://raw.githubusercontent.com/joserosas-vanta/dotfiles/main/bin/dotfiles
)"
```

`bin/dotfiles` handles the following during install/update:

- Installs base Ubuntu dependencies needed to run the playbook
- Installs `1password-cli`
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
  - `pi_managed_source_packages`
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

- `bootstrap` (base distro packages and 1Password CLI)
- `users`
- `ssh`
- `openssh`
- `ufw`
- `tailscale`
- `media-tools`
- `volta`

The repo no longer creates the old named personal users during bootstrap.

## OpenCode Guides

This repository does not own OpenCode guide content.
Guide families are maintained in the dedicated guides repository and cloned to
the user environment by the `opencode` role.

Guide-family authoring and governance should happen in the dedicated guides repository.
This repo focuses on environment replication and distribution plumbing.

To install OpenCode and clone the shared guides repository into your environment, run:

```bash
dotfiles -t opencode
```

To initialize a project repo with a local overlay, run:

```bash
opencode-init-repo
```

`opencode-init-repo` creates a repo-root `AGENTS.md` from the shared guides template and writes a
repo-local `opencode.json` that loads both:

- shared guides selector (`~/.local/share/opencode-guides/files/AGENTS.md`)
- repo-local overlay (`AGENTS.md`)

Then edit `AGENTS.md` to add repo-specific context and optional guide additions from the shared
guides `VARIANTS.md`.

To check whether your local overlay scaffold is current with the shared template:

```bash
opencode-sync-repo
```

To update only the managed overlay section (preserving repo context and local additions):

```bash
opencode-sync-repo --write
```
