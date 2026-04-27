# Upstream Drift Tracker (`sp-dotfiles` -> `dotfiles`)

## Audit Snapshot
- Date: 2026-04-27
- Dotfiles HEAD: `7388647`
- Upstream HEAD: `cdfa372`
- Divergence: ahead 15 / behind 25

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
| cdfa372 | nix | `roles/nix/files/sillypoise/home.nix` | add `ps.pillow` and `imagemagick` | todo | Port to `roles/nix/templates/home.nix.j2` if image tooling is desired |
| cdfa372 | repo config | `.pi/guides.json` | enable `behavior.autoCommit: true` | planned | Decide explicitly for this fork before adopting |
| 5a84122 | pi | `group_vars/all.yml` | bump upstream guides source to `v0.3.0` | skipped | Fork uses local checkout source (`vpi-guides`) instead of upstream pin |
| 886cea7 | pi | `group_vars/all.yml`, `roles/pi/tasks/main.yml` | manage source-based `pi-fff` package checkout/install | planned | Task support ported; default package disabled in fork due runtime dependency issues |
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
- 2026-04-22: Created tracker with current upstream drift snapshot and initial triage.
- 2026-04-23: Added mandatory drift-check routine and ported `faceef4` zsh secret pi-provider settings.
- 2026-04-23: Ported `402c2ca` `PI_GUIDES_DEV_SOURCE` with fork-local default path.
- 2026-04-23: Ported upstream `c90dc31` enabled model-id fix into fork-specific `pi_enabled_models`.
- 2026-04-23: Reverted `faceef4` secret-autoload port; removed `KIMI_API_KEY` and `GH_TOKEN` from shell autoload template.
- 2026-04-27: Refreshed snapshot and added newly detected upstream drift items (`cdfa372`, `5a84122`, `886cea7`, `3702067`, `6eb30a6`).
- 2026-04-27: Ported core pi updates from upstream (`6eb30a6`, `3702067`) and task scaffolding from `886cea7`.
- 2026-04-27: Disabled default `pi-fff` managed source package and reverted provider-prefixed model patterns after runtime validation issues.
