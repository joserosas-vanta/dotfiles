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

  # Code Generation & Types
  alias motypes="turbo generate-types"
  alias motypesw="just generate-types-watch"

  # Testing
  alias motest="just unit-test"
  alias motestp="just unit-test-project"
  alias motestw="just unit-test-watch"

  # Development Services
  alias modev="just dev-start resource-fetcher-live test-runner-live web web-client lambda-test-rollout-management api-service auth-service"

  # Log watching
  alias ml="just dev-watch-logs"
  alias mlrfl="just dev-watch-logs resource-fetcher-live"
  alias mltrl="just dev-watch-logs test-runner-live"
  alias mlw="just dev-watch-logs web"
  alias mlwc="just dev-watch-logs web-client"

  # Clean operations
  alias moclean="just clean && just yarn && turbo generate-types"
  alias mocleanb="just clean && just yarn && turbo generate-types &&
  turbo build:app"

  # Build operations
  alias mobrfl="turbo build:app -F @vanta/resource-fetcher"
  alias mobtrl="turbo build:app -F @vanta/test-runner"
  alias mobw="turbo build:app -F @vanta/web"

  # Service replacement
  alias morep="just dev-replace"
  alias morepa="just dev-replace-web && just dev-replace-integration"
  alias morepwc="just dev-replace web-client"
  alias moreprfl="just dev-replace resource-fetcher-live"

  # Turbo shortcuts with workspace support
  alias tts='turbo typecheck'
  alias ttsw='turbo typecheck:watch'
  alias ttsni='turbo typecheck:no-incremental'
  alias tlint='turbo lint'
  alias tlintf='turbo lint:fix'
  alias ttest='turbo unit-test'
  alias tbuild='turbo build:app'
  alias tgen='turbo generate-types'

  # Turbo shortcuts with workspace support
  alias ttsf='turbo typecheck -F'
  alias ttswf='turbo typecheck:watch -F'
  alias ttsnif='turbo typecheck:no-incremental -F'
  alias tlintf='turbo lint -F'
  alias tlintff='turbo lint:fix -F'
  alias ttestf='turbo unit-test -F'
  alias tbuildf='turbo build:app -F'
  alias tgenf='turbo generate-types -F'

  # Just shortcuts
  alias jpp="just post-pull"
  alias jut="just unit-test"
  alias jutw="just unit-test-watch"
  alias jdr="just dev-replace"
  alias jds="just dev-start"
  alias jdw="just dev-watch-logs"

  # Terraform (if you still use these)
  alias tfcreate='./legacy_scripts/tf/create_aws_sandbox.py sandbox'
  alias tfapply='./legacy_scripts/tf/apply_aws_sandbox.py sandbox'
  alias tfdestroy='./legacy_scripts/tf/destroy_aws_sandbox.py sandbox'
