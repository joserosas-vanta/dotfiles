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
