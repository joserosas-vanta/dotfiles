# Upstream Drift Tracker (`sp-dotfiles` -> `dotfiles`)

## Audit Snapshot
- Date: 2026-11-17
- Dotfiles HEAD: `5a143c4` (before the Nix transport update)
- Upstream HEAD: `1e775d3`
- Divergence: ahead 36 / behind 72 (commit ancestry; includes previously ported changes)

## Porting Policy
- Port when: useful for this fork and compatible with work-VM/local-checkout architecture.
- Skip when: conflicts with fork-specific design or is already superseded locally.

## Required Drift Check Routine
- Always run a drift check before/after non-trivial changes to `pi`, `zsh`, `nix`, or `media-tools`.
- Always refresh this file in the same work session when upstream has new commits.

```bash
cd ~/.local/share/dotfiles
git fetch upstream
git rev-list --left-right --count main...upstream/main
git log --oneline --no-merges main..upstream/main
```

## Drift Items

| Commit | Area | Files | Summary | Status | Decision Note |
|---|---|---|---|---|---|
| 1e775d3 | pi | guide source variables and resolution tasks | follow newest semantic guide release with offline fallback | ported | Adapted to the managed local `vpi-guides` checkout; explicit refs still pin |
| 7cb4ae0 | pi | provider and model defaults | default to Claude Bridge and retain current GPT/Kimi cycling | ported | Ported directly; provider package is managed at a commit SHA |
| 8bcd9d0 | pi | managed package variables | add pinned `pi-claude-bridge` checkout | ported | Ported with validation; audit disposition is in `docs/security-exceptions.md` |
| 8196c8b | pi-guides | package release | update guide package to v0.6.0 | superseded | `vpi-guides` was fast-forwarded through tested v0.7.0 instead |
| c4e06f6 | nix | flake/home templates, tests | isolate Claude Code on locked unstable input | ported | Adapted to fork template; stable pins unchanged |
| 0fae6e4 | update/nix | update role, shared activation, tests | opt-in OS and Nix package upgrades | ported | Nix-only in this fork; omits OS upgrades, preserves runtime modes and lock ownership |
| e69be6e | update | release reminder | advisory release lookup | deferred | Not requested in this port |
| 3be8fdb | nix | release variables | upgrade stable pins to 26.05 | deferred | Keep 25.11; evaluate package compatibility before upgrading |
| cdfa372 | nix | `roles/nix/files/sillypoise/home.nix` | add `ps.pillow` and `imagemagick` | todo | Port to `roles/nix/templates/home.nix.j2` if image tooling is desired |
| cdfa372 | repo config | `.pi/guides.json` | enable `behavior.autoCommit: true` | planned | Decide explicitly for this fork before adopting |
| 5a84122 | pi | `group_vars/all.yml` | bump upstream guides source to `v0.3.0` | skipped | Fork uses local checkout source (`vpi-guides`) instead of upstream pin |
| 886cea7 | pi | `group_vars/all.yml`, `roles/pi/tasks/main.yml` | manage source-based `pi-fff` package checkout/install | skipped | Generic task support remains, but `fff.nvim` is not needed by this fork |
| 3702067 | pi | `group_vars/all.yml`, `roles/pi/tasks/main.yml` | add `pi_extra_packages` support | ported | Added validation and merged package source composition |
| 3702067 | volta | `roles/volta/tasks/main.yml` | install `pnpm` via Volta | todo | Likely low-risk portability win |
| 3702067 | nix | `roles/nix/files/sillypoise/home.nix` | add `zig` package | todo | Port to template if needed for current workflows |
| 6eb30a6 | pi | `group_vars/all.yml` | default model to `gpt-5.5` and thinking `low` | ported | Updated defaults and kept fork-compatible model patterns |
| d44a514 | media-tools | `roles/media-tools/tasks/{main,arch,ubuntu}.yml` | add libvips installation/tags | todo | Useful for image tooling and OCR-adjacent workflows |
| c90dc31 | pi | `group_vars/all.yml` | fix enabled model id format | ported | Ported with fork list retaining `claude-opus-4-7` |
| 3604677 | nix | `roles/nix/files/sillypoise/home.nix` | add duckdb package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 08183f8 | nix | `roles/nix/files/sillypoise/home.nix` | add jjui package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 366512e | nix | `roles/nix/files/sillypoise/home.nix` | add aria2 package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 402c2ca | zsh | `roles/zsh/files/zsh/vars.zsh` | add `PI_GUIDES_DEV_SOURCE` env var | ported | Ported with fork path default `$HOME/pi-guides` |
| faceef4 | zsh/secrets | `roles/zsh/files/zsh/vars.autoload.secret.tpl` | add `KIMI_API_KEY` and `GH_TOKEN` autoload | skipped | Intentionally omitted in this fork; no shell-autoload for these secrets |

## Skipped/Superseded Buckets
- Legacy upstream `pi` bootstrap/config commits (`25059bd` through `86c7f02`) are mostly superseded by fork-specific local-checkout behavior in `dotfiles`.
- `.pi/guides.json` profile id/mode remains aligned (`coreplus`/`compact`), but upstream now also sets `behavior.autoCommit`.

## Change Log
- 2026-11-23: zsh loads Ona's `/etc/profile.d/ona-secrets.sh`, which only bash login shells
  read, so Ona user secrets such as `GH_TOKEN` reach zsh and Rex shells. No values live in
  dotfiles. `bin/dotfiles` waits up to 10 minutes for the dpkg lock held by a fresh machine's
  startup apt-get. Fork-local.
- 2026-11-19: `dotfiles -t update` also upgrades the Rex binary through the official installer,
  without restarting a running server, and reports when a restart is pending. Fork-local.
- 2026-11-19: zsh now appends Volta's `bin` to PATH when another Node exists (such as the
  Ona image's nvm Node), and prepends it only when Volta provides the only Node. Volta's
  Node 26 had shadowed nvm's Node 24, breaking native modules built against 24. Fork-local.
- 2026-11-17: Replaced `github:` Nix flake inputs with shallow HTTPS Git inputs and exposed the
  locked Home Manager package from the local flake. Activation no longer performs a separate
  GitHub-registry lookup, avoiding the shared egress address's exhausted REST API quota.
- 2026-11-17: Added a Pi-role fallback that provisions Node LTS through Nix-managed Volta when
  `npm` is absent from the non-interactive target-user environment.
- 2026-11-17: Replaced Pi's unauthenticated GitHub REST release lookup with Git tag discovery and
  release `SHA256SUMS` verification after a shared remote egress address exhausted the API quota.
- 2026-11-17: Refreshed upstream through `1e775d3` and ported only Pi changes. Updated provider,
  model cycling, the pinned Claude Bridge package, and release-based local guide resolution.
  Fast-forwarded `joserosas-vanta/vpi-guides` from v0.6.0 to tested v0.7.0 and published the
  `v0.7.0` tag. `fff.nvim` remains disabled because it is not required by this fork.
- 2026-10-01: Restricted `update` to Nix packages on both Ubuntu and Arch. Missing Nix is
  an explicit no-op; OS upgrades must be managed separately. Regression tests reject OS modules.
- 2026-10-01: Refreshed upstream snapshot; ported only Claude Code source isolation and opt-in
  package updates. Added offline negative-path tests. No release-pin, Pi, secret, or package-list
  changes beyond Claude Code. Earlier todo entries below are historical, not a fresh full audit.
- 2026-04-22: Created tracker with current upstream drift snapshot and initial triage.
- 2026-04-23: Added mandatory drift-check routine and ported `faceef4` zsh secret pi-provider settings.
- 2026-04-23: Ported `402c2ca` `PI_GUIDES_DEV_SOURCE` with fork-local default path.
- 2026-04-23: Ported upstream `c90dc31` enabled model-id fix into fork-specific `pi_enabled_models`.
- 2026-04-23: Reverted `faceef4` secret-autoload port; removed `KIMI_API_KEY` and `GH_TOKEN` from shell autoload template.
- 2026-04-27: Refreshed snapshot and added newly detected upstream drift items (`cdfa372`, `5a84122`, `886cea7`, `3702067`, `6eb30a6`).
- 2026-04-27: Ported core pi updates from upstream (`6eb30a6`, `3702067`) and task scaffolding from `886cea7`.
- 2026-04-27: Disabled default `pi-fff` managed source package and reverted provider-prefixed model patterns after runtime validation issues.
- 2026-04-27: Fork policy change: removed 1Password-dependent setup paths (OpenCode guides/server secrets, zsh secret injection, SSH key injection, bootstrap onepassword install).
