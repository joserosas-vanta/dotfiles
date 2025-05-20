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

# work
alias mdb="vanta-mongodb"
alias motypes="turbo generate-types"
alias mosync="make sync-airtable"
alias motest="make unit-test"
alias modev="make dev-start resource-fetcher-live test-runner-live web web-client lambda-test-rollout-management api-service auth-service"
alias ml="make dev-watch-logs"
alias mlrfl="ml resource-fetcher-live"
alias mltrl="ml test-runner-live"
alias mlw="ml web"
alias mlwc="ml web-client"
alias moclean="make clean yarn generate-types"
alias mocleanb="make clean yarn generate-types build"
alias mobrfl="turbo build -F @vanta/resource-fetcher"
alias mobtrl="turbo build -F @vanta/test-runner"
alias mobw="turbo build -F @vanta/web"
alias morep="make dev-replace"
alias morepa="make dev-replace-WEB && make dev-replace-INTEGRATION && make dev-replace build"
alias morepwc="make dev-replace web-client"
alias moreprfl="make dev-replace resource-fetcher-live"
alias tfcreate='./legacy_scripts/tf/create_aws_sandbox.py sandbox'
alias tfapply='./legacy_scripts/tf/apply_aws_sandbox.py sandbox'
alias tfdestroy='./legacy_scripts/tf/destroy_aws_sandbox.py sandbox'

