#!/usr/bin/env zsh

# Add custom bin directories
addToPath "$HOME/.local/share/dotfiles/bin"
addToPath "$HOME/.local/bin"

# Source the first available Nix profile script.
for nix_profile in \
  "$HOME/.nix-profile/etc/profile.d/nix.sh" \
  "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh" \
  "/etc/profile.d/nix.sh"; do
  if [ -e "$nix_profile" ]; then
    source "$nix_profile"
    break
  fi
done

# # Add op plugins NOT UNTIL WE FIGURE OUT RDS
# sourceIfExists "$HOME/.config/op/plugins.sh"

# Add independently install binaries to PATH

addToPath "$HOME/.opencode/bin"

# Prefer the active Node/Corepack toolchain over Nix pnpm shims.
# This keeps repo-pinned pnpm launchers ahead of older Nix-installed pnpm binaries.
if command -v node &>/dev/null; then
    node_bin_dir="$(dirname "$(command -v node)")"
    if [ -d "$node_bin_dir" ]; then
        addToPathFront "$node_bin_dir"
    fi
fi

## Add nix-installed binaries to PATH
# Volta setup
# Volta's Node is a fallback: a machine's own Node (for example the Ona image's nvm
# Node, which repo native modules are built against) must stay first. Volta goes
# last when another Node exists, and first only when it provides the only Node.
if [ -d "$HOME/.volta" ]; then
    export VOLTA_HOME="$HOME/.volta"
    path=("${(@)path:#$VOLTA_HOME/bin}")
    if whence -p node &>/dev/null; then
        path+=("$VOLTA_HOME/bin")
    else
        path=("$VOLTA_HOME/bin" $path)
    fi
    export PATH
fi

# tenv setup: expose managed tool shims (terraform/tofu/terragrunt/etc.)
if command -v tenv &>/dev/null && [ -d "$HOME/.tenv" ]; then
    export PATH="$(tenv update-path)"
fi

# Rustup setup
if command -v rustup &>/dev/null; then
    addToPath "$HOME/.cargo/bin"
fi

# Starship Prompt setup
if command -v starship &>/dev/null; then
    eval "$(starship init zsh)"
fi

# Zoxide setup
if command -v zoxide &>/dev/null; then
    eval "$(zoxide init zsh --cmd cd)"
fi

# Mise setup
if command -v mise &>/dev/null; then
    eval "$(mise activate zsh)"
fi


# Optional tooling setup (e.g., Aactivator)
if command -v aactivator &>/dev/null; then
    eval "$(aactivator init)"
fi
