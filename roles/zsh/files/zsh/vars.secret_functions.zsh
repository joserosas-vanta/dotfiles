#!/usr/bin/env zsh

function secret() {
  clear_env=false
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      -c|--clear)
        clear_env=true
        shift
        ;;
      -r|--reload)
        __task "${ARROW} ${YELLOW}Reloading secrets...";_task_done
        secret --clear && secret
        return
        ;;
      *)
        echo "Unknown option: $1"
        return 1
        ;;
    esac
  done

  # set -c but already unloaded
  if [[ "$clear_env" == true ]] && [ -z "$SECRETS_ALREADY_LOADED" ]; then
    echo -e " ${GREEN}[${CHECK_MARK}${GREEN}] Secrets already unloaded."
    return
  fi

  # set -c
if [[ "$clear_env" == true ]]; then
    __task "Detecting secret vars..."
    local secret_vars=($(grep -o '^\s*export\s\+\w\+' "$HOME/.config/zsh/vars.secret" | awk '{print $2}'))
    for var in "${secret_vars[@]}"; do
      # Skip unsetting OP_SERVICE_ACCOUNT_TOKEN
      if [[ "$var" == "OP_SERVICE_ACCOUNT_TOKEN" ]]; then
          __task "${RIGHT_ANGLE}${GREEN} Skipping: ${YELLOW}$var"
          continue
      fi
      __task "${RIGHT_ANGLE}${GREEN} Unsetting: ${YELLOW}$var"
      unset "$var"
    done
    _task_done
    unset SECRETS_ALREADY_LOADED
    return
fi

  # loading when already loaded (skip)
  if [ -n "$SECRETS_ALREADY_LOADED" ] && [ "$SECRETS_ALREADY_LOADED" = true ]; then
    echo -e " ${GREEN}[${CHECK_MARK}${GREEN}] Secrets already loaded."
    return
  fi

  __task "Loading Secrets..."
  _cmd "source '$HOME/.config/zsh/vars.secret'"
  export SECRETS_ALREADY_LOADED=true
  _task_done
}
