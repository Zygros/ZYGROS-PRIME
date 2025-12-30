#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "[+] Updating Termux packages…"
pkg update -y && pkg upgrade -y

echo "[+] Core tools"
pkg install -y git curl wget openssh tmux zsh neovim ripgrep fd fzf bat eza zoxide jq aria2 unzip unrar p7zip grep sed coreutils tar python nodejs-lts go clang make cmake gawk busybox nano

echo "[+] Power/system tools"
pkg install -y htop btop proot-distro neofetch imagemagick ffmpeg exiftool rclone sftpman tig

echo "[+] Enable storage access (if not already)"
termux-setup-storage || true

echo "[+] Shell defaults (zsh + aliases)"
if ! grep -q "zsh" "$HOME/.bashrc" 2>/dev/null; then
  echo 'exec zsh' >> "$HOME/.bashrc"
fi
mkdir -p "$HOME/.config"
cp -f "$HOME/storage/downloads/aliases.zsh" "$HOME/.aliases.zsh" 2>/dev/null || true
if ! grep -q ".aliases.zsh" "$HOME/.zshrc" 2>/dev/null; then
  cat >> "$HOME/.zshrc" <<'EOF'

# == ZAAI A16 Shell ==
source ~/.aliases.zsh 2>/dev/null
eval "$(zoxide init zsh)"
alias ls='eza --group-directories-first --icons=always -al'
export EDITOR=nvim
export PAGER=less
export LESS='-R'
EOF
fi

echo "[+] Tmux config"
mkdir -p "$HOME/.termux"
cp -f "$HOME/storage/downloads/tmux.conf" "$HOME/.tmux.conf" 2>/dev/null || true

echo "[+] Python user env (pipx + key CLIs)"
python -m pip install --upgrade --no-color pip pipx wheel
python -m pipx ensurepath
~/.local/bin/pipx install --force yt-dlp
~/.local/bin/pipx install --force poetry

echo "[+] Node global utilities"
npm -g install npm-check-updates zx

echo "[+] rclone quick dirs"
mkdir -p "$HOME/ZA_AI_VAULT" "$HOME/ZA_AI_BACKUP" "$HOME/ZA_AI_TMP"

echo "[+] Cron (scheduled jobs)"
pkg install -y cronie
sv-enable crond || true
crontab -l 2>/dev/null | { cat; echo "0 */6 * * * $HOME/vault_backup_sync.sh >> $HOME/backup.log 2>&1"; } | crontab -

echo "[✓] Bootstrap complete. Restart Termux or run 'exec zsh'."
