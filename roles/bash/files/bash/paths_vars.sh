#!/usr/bin/env bash

# Add custom bin directories
addToPath "$HOME/.local/share/dotfiles/bin"
addToPath "$HOME/.local/bin"

# Source the first available Nix profile script.
for nix_profile in \
    "$HOME/.nix-profile/etc/profile.d/nix.sh" \
    "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh" \
    "/etc/profile.d/nix.sh"; do
    if [ -e "$nix_profile" ]; then
        . "$nix_profile"
        break
    fi
done

# Prefer the active Node/Corepack toolchain over Nix pnpm shims.
# This keeps repo-pinned pnpm launchers ahead of older Nix-installed pnpm binaries.
if command -v node &>/dev/null; then
    node_bin_dir="$(dirname "$(command -v node)")"
    if [ -d "$node_bin_dir" ]; then
        addToPathFront "$node_bin_dir"
    fi
fi
