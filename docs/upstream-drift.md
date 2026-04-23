# Upstream Drift Tracker (`sp-dotfiles` -> `dotfiles`)

## Audit Snapshot
- Date: 2026-04-23
- Dotfiles HEAD: `087a7f6`
- Upstream HEAD: `c90dc31`
- Divergence: ahead 14 / behind 20

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
| d44a514 | media-tools | `roles/media-tools/tasks/{main,arch,ubuntu}.yml` | add libvips installation/tags | todo | Useful for image tooling and OCR-adjacent workflows |
| c90dc31 | pi | `group_vars/all.yml` | fix enabled model id format | ported | Ported with fork list retaining `claude-opus-4-7` |
| 3604677 | nix | `roles/nix/files/sillypoise/home.nix` | add duckdb package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 08183f8 | nix | `roles/nix/files/sillypoise/home.nix` | add jjui package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 366512e | nix | `roles/nix/files/sillypoise/home.nix` | add aria2 package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 402c2ca | zsh | `roles/zsh/files/zsh/vars.zsh` | add `PI_GUIDES_DEV_SOURCE` env var | ported | Ported with fork path default `$HOME/pi-guides` |
| faceef4 | zsh/secrets | `roles/zsh/files/zsh/vars.autoload.secret.tpl` | add `KIMI_API_KEY` and `GH_TOKEN` autoload | skipped | Intentionally omitted in this fork; no shell-autoload for these secrets |

## Skipped/Superseded Buckets
- Legacy upstream `pi` bootstrap/config commits (`25059bd` through `86c7f02`) are mostly superseded by fork-specific local-checkout behavior in `dotfiles`.
- `.pi/guides.json` profile drift is currently aligned (`coreplus`).

## Change Log
- 2026-04-22: Created tracker with current upstream drift snapshot and initial triage.
- 2026-04-23: Added mandatory drift-check routine and ported `faceef4` zsh secret pi-provider settings.
- 2026-04-23: Ported `402c2ca` `PI_GUIDES_DEV_SOURCE` with fork-local default path.
- 2026-04-23: Ported upstream `c90dc31` enabled model-id fix into fork-specific `pi_enabled_models`.
- 2026-04-23: Reverted `faceef4` secret-autoload port; removed `KIMI_API_KEY` and `GH_TOKEN` from shell autoload template.
