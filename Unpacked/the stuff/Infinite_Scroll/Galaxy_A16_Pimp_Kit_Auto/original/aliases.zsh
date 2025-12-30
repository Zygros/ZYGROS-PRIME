# == ZAAI Aliases & Functions ==
alias update='pkg update -y && pkg upgrade -y && npm -g update && ~/.local/bin/pipx upgrade-all'
alias ll='eza -lah --git'
alias f='fzf'
alias rg='rg --hidden --follow --smart-case'
alias z='zoxide'
alias sz='source ~/.zshrc'
alias v='nvim'
alias ta='tmux attach || tmux new -s main'
alias td='tmux detach'
alias k9='kill -9'
alias speedtest='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -'
# dedupe scan helper
dedupe() { python ~/dedupe_scan.py "$@"; }
