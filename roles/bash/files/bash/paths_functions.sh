#!/usr/bin/env bash

addToPath() {
    if [[ "$PATH" != *"$1"* ]]; then
        export PATH=$PATH:$1
    fi
}

addToPathFront() {
    local directory="$1"
    local path_parts=()
    local path_entry

    IFS=':' read -r -a path_parts <<< "$PATH"

    PATH="$directory"
    for path_entry in "${path_parts[@]}"; do
        if [[ "$path_entry" != "$directory" ]]; then
            PATH+="::$path_entry"
        fi
    done

    PATH="${PATH//::/:}"
    export PATH
}

sourceIfExists() {
    local path="$1"
    if [ -e "$path" ]; then
        . "$path"
        echo "Sourced $path"
    else
        echo "Warning: $path not found, skipping."
    fi
}

# change_background() {
#     dconf write /org/mate/desktop/background/picture-filename "'$HOME/anime/$(ls ~/anime| fzf)'"
# }

die() {
    echo >&2 "$@"
    exit 1
}
