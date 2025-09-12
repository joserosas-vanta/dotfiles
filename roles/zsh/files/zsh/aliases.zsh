# Aliases
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias br="broot"
alias brt="broot --cmd :print_tree"
alias c='clear'
alias cp='cp -iv'
alias cat="bat"
alias chmod="chmod -c"
alias chown="chown -c"
alias find="fd"
alias grep="rg"
alias lg="lazygit"
alias ld="lazydocker"
alias ls="exa"
alias ll="exa -l"
alias sed="sd"
alias extip='curl https://myip.wtf/text'
alias extipjson='curl https://myip.wtf/json'
alias mkdir='mkdir -pv'
alias mv='mv -iv'
alias ports='netstat -tulanp'
alias rm='rm -iv'
alias rmdir='rmdir -v'
alias sqsh="squoosh-cli"
alias pnx="pnpm nx"
# alias speedtest='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -'
alias vim="nvim"
alias svim='sudo vim'
alias reload="source ~/.zshrc"
alias zj="zellij"
alias zshrc="nvim ~/.zshrc"
alias fjson="pbpaste | jq '.' | pbcopy"
alias watch='watch -d'
alias weather='curl wttr.in'
alias wget='wget -c'

# SSH
alias sshg='eval $(ssh-agent) && ssh-add ~/.ssh/gh_id_ed25519'
alias sshgv='eval $(ssh-agent) && ssh-add ~/.ssh/vanta_gh_id_ed25519'
alias ssha='eval $(ssh-agent) && ssh-add ~/.ssh/aws_id_ed25519'
alias sshsp='eval $(ssh-agent) && ssh-add ~/.ssh/sp_work_ed25519'

## Python aliases
alias py="python3"
alias pvenv='python3 -m venv venv && ln -s venv/bin/activate .activate.sh && echo "deactivate" > .deactivate.sh'

## SQLite
alias sqlite="sqlite3"
alias sqlu="sqlite-utils"

# git aliases
alias g="git"
alias gs="git status"
alias ga="git add"
alias gci="git commit"
alias gP="git push"
alias gf="git fetch"
alias gp="git pull"
alias gpr="git pull --rebase"
alias gco="git checkout"

# GH & Copilot CLI 
alias ghas="gh auth switch"

 # === JUST ALIASES ===
  # Database
  alias mdb="vanta-mongodb"

  # Development Services
  alias jdev="just dev-start resource-fetcher-live test-runner-live web web-client lambda-test-rollout-management api-service auth-service"

  # Turbo shortcuts for all workspaces
  alias ttsa='turbo typecheck'
  alias ttswa='turbo typecheck:watch'
  alias ttsnia='turbo typecheck:no-incremental'
  alias tlinta='turbo lint'
  alias tlintfa='turbo lint:fix'
  alias ttesta='turbo unit-test'
  alias tbuilda='turbo build:app'
  alias tgena='turbo generate-types'

  # Turbo shortcuts with workspace support
  alias tts='turbo typecheck -F'
  alias ttsw='turbo typecheck:watch -F'
  alias ttsni='turbo typecheck:no-incremental -F'
  alias tlint='turbo lint -F'
  alias tlintf='turbo lint:fix -F'
  alias ttest='turbo unit-test -F'
  alias tbuild='turbo build:app -F'
  alias tgen='turbo generate-types -F'
  alias tpsa='turbo project-static-analysis'

  # Just shortcuts
  alias jpp="just post-pull"
  alias jtest="just unit-test"
  alias jutw="just unit-test-watch"
  alias jrep="just dev-replace"
  alias jrepa="just dev-replace-web && just dev-replace-integration"
  alias js="just dev-start"
  alias jl="just dev-watch-logs"
  alias jlrfl="just dev-watch-logs resource-fetcher-live"
  alias jltrl="just dev-watch-logs test-runner-live"
  alias jlw="just dev-watch-logs web"
  alias jlwc="just dev-watch-logs web-client"
  alias jclean="just clean"
  alias jclean="just clean && just yarn && turbo generate-types"
  alias jcleanb="just clean && just yarn && turbo generate-types &&
  turbo build:app"

  # Terraform (if you still use these)
  alias tfcreate='./legacy_scripts/tf/create_aws_sandbox.py sandbox'
  alias tfapply='./legacy_scripts/tf/apply_aws_sandbox.py sandbox'
  alias tfdestroy='./legacy_scripts/tf/destroy_aws_sandbox.py sandbox'
