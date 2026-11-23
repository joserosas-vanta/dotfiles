#!/usr/bin/env zsh

# Ona writes user and org secrets (GH_TOKEN, JIRA_API_TOKEN, ...) to this file and
# only bash login shells load it, through /etc/profile. zsh never reads
# /etc/profile.d, so load it here. The file is Ona-managed; no values live in dotfiles.
if [ -r /etc/profile.d/ona-secrets.sh ]; then
    source /etc/profile.d/ona-secrets.sh
fi
