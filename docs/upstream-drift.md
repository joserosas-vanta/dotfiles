# Upstream Drift Tracker (`sp-dotfiles` -> `dotfiles`)

## Audit Snapshot
- Date: 2026-04-22
- Dotfiles HEAD: `e38b991`
- Upstream HEAD: `86c7f02`
- Divergence: ahead 13 / behind 19

## Porting Policy
- Port when: useful for this fork and compatible with work-VM/local-checkout architecture.
- Skip when: conflicts with fork-specific design or is already superseded locally.

## Drift Items

| Commit | Area | Files | Summary | Status | Decision Note |
|---|---|---|---|---|---|
| d44a514 | media-tools | `roles/media-tools/tasks/{main,arch,ubuntu}.yml` | add libvips installation/tags | todo | Useful for image tooling and OCR-adjacent workflows |
| 3604677 | nix | `roles/nix/files/sillypoise/home.nix` | add duckdb package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 08183f8 | nix | `roles/nix/files/sillypoise/home.nix` | add jjui package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 366512e | nix | `roles/nix/files/sillypoise/home.nix` | add aria2 package | todo | Port to `roles/nix/templates/home.nix.j2` |
| 402c2ca | zsh | `roles/zsh/files/zsh/vars.zsh` | add `PI_GUIDES_DEV_SOURCE` env var | todo | Helpful for local guide-dev bootstrap |
| faceef4 | zsh/secrets | `roles/zsh/files/zsh/vars.autoload.secret.tpl` | add `KIMI_API_KEY` and `GH_TOKEN` autoload | planned | Confirm secret-management preference before porting |

## Skipped/Superseded Buckets
- Legacy upstream `pi` bootstrap/config commits (`25059bd` through `86c7f02`) are mostly superseded by fork-specific local-checkout behavior in `dotfiles`.
- `.pi/guides.json` profile drift is currently aligned (`coreplus`).

## Change Log
- 2026-04-22: Created tracker with current upstream drift snapshot and initial triage.
