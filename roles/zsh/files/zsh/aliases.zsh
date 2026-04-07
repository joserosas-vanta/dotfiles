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
alias oc="opencode"
alias occ="opencode -c"
alias oci="opencode-init-repo"
alias ocsr="opencode-sync-repo"
alias sed="sd"
alias extip='curl https://myip.wtf/text'
alias extipjson='curl https://myip.wtf/json'
alias mkdir='mkdir -pv'
alias mv='mv -iv'
alias ports='netstat -tulanp'
alias pk='portkill'
alias rm='rm -iv'
alias rmdir='rmdir -v'
alias sqsh="squoosh-cli"
alias pnpma="pnpm approve-builds"
# alias speedtest='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -'
alias vim="nvim"
alias svim='sudo vim'
alias reload="source ~/.zshrc"
alias zj="zellij"
alias zjls="zellij list-sessions"
alias zshrc="nvim ~/.zshrc"
alias fjson="pbpaste | jq '.' | pbcopy"
alias watch='watch -d'
alias weather='curl wttr.in'
alias wget='wget -c'

# SSH
alias sshg='ensure_ssh_github_key_loaded'
alias sshgv='eval $(ssh-agent) && ssh-add ~/.ssh/gh_id_ed25519'

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

# Obsidian / Vanta
alias mdb="vanta-mongodb"
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
alias jpp='just post-pull'
alias jtest='just unit-test'
alias jutw='just unit-test-watch'
alias jrep='just dev-replace'
alias jrepa='just dev-replace-web && just dev-replace-integration'
alias js='just dev-start'
alias jl='just dev-watch-logs'
alias jlrfl='just dev-watch-logs resource-fetcher-live'
alias jltrl='just dev-watch-logs test-runner-live'
alias jlw='just dev-watch-logs web'
alias jlwc='just dev-watch-logs web-client'
alias jclean='just clean && just yarn && turbo generate-types'
alias jcleanb='just clean && just yarn && turbo generate-types && turbo build:app'

# Remote Development Servers
alias rds-sp="ssh vscode@sp-dev"
