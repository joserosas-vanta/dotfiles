# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a work-VM-first dotfiles repository that uses Ansible to manage development environment
configuration. The primary target is Ubuntu LTS workspaces that already provide a `vscode` user.
Arch Linux support remains available, but the default flow is tuned for Ubuntu work VMs.

## Key Commands

### Dotfiles Management
```bash
# Run full configuration update
dotfiles

# Run specific role (with tab completion support)
dotfiles -t <role>

# Override the default vscode target user
dotfiles -u <user> -t <tag>

# Debug mode with verbose output
dotfiles -t <role> -vvv

# Syntax check the playbook
ansible-playbook main.yml --syntax-check
```

### Testing Changes
```bash
# Test a specific role
dotfiles -t test

# Verify 1Password CLI authentication
op whoami
```

## Architecture

### Core Structure
- **main.yml**: Orchestrates all role executions in proper order
- **bin/dotfiles**: Main script that handles installation, updates, and Ansible playbook execution
- **pre_tasks/facts.yml**: Detects OS, user, 1Password, Nix, GitHub CLI, and other runtime facts
- **roles/**: Contains individual configuration roles (bash, git, nvim, etc.)
- **group_vars/all.yml**: Defines default roles and global variables

### Default Work-VM Path
- Default target user: `vscode`
- Default roles: `bash`, `zsh`, `nix`, `git`, `c`, `nvim`, `opencode`, `zellij`, `btop`
- Repository clone path: `~/.local/share/dotfiles`
- Command link path: `~/.local/bin/dotfiles`

### Security & Secrets
- Uses 1Password CLI for secure credential management
- Template files (`.tpl`) require 1Password authentication to populate secrets
- Sensitive configs are managed through 1Password integration

### Opt-In Roles
- **bootstrap**: Base distro packages and 1Password CLI install
- **users**: Hostname and password sync for the target user
- **ssh/openssh**: SSH client and server configuration
- **tailscale**: Mesh VPN setup
- **ufw**: Firewall rules
- **media-tools** / **volta** / **test**: Optional tooling and validation roles

### Key Ansible Roles
- **nix**: Package management with Home Manager
- **zsh/bash**: Shell configurations
- **nvim**: Neovim setup
- **git**: GitHub CLI install and config
- **opencode**: OpenCode install, guides sync, and service setup

## Development Guidelines

### Adding New Roles
1. Create role directory under `roles/`
2. Add to `default_roles` in `group_vars/all.yml`
3. Include tasks in `roles/<role>/tasks/main.yml`
4. Use templates with `.j2` extension for dynamic configs

### Working with Templates
- Templates requiring secrets should use `.tpl` extension
- Access 1Password items via `op://` references in templates
- Always verify 1Password authentication before running sensitive roles

### Testing Modifications
- Test individual roles with `-t <role>` flag
- Use `-vvv` for debugging Ansible execution
- Verify 1Password auth with `op whoami` when working on secret-backed roles

### Common Patterns
- Use `become: true` for tasks requiring sudo
- Tag tasks appropriately for selective execution
- Follow existing role structure for consistency
- Keep idempotency in mind - tasks should be safe to run multiple times
