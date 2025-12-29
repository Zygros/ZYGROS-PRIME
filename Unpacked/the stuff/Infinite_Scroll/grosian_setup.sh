\
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

REMOTE="${REMOTE:-gdrive}"
BUCKET="${BUCKET:-ZAAI_BACKUPS}"
DEVICE="${DEVICE:-A16}"
VAULT="${VAULT:-$HOME/ZA_AI_VAULT}"
DST="$REMOTE:$BUCKET/$DEVICE"
ARCHIVE="$REMOTE:${BUCKET}_ARCHIVE/$DEVICE"

log(){ printf "\n[\033[1;36mGROSIAN\033[0m] %s\n" "$*"; }
warn(){ printf "\n[\033[1;33mWARN\033[0m] %s\n" "$*"; }

log "Updating Termux and installing packages..."
yes | pkg update -y || true
pkg upgrade -y
pkg install -y git zsh tmux fzf ripgrep python nodejs rclone cronie openssh jq rust coreutils findutils tar gzip termux-api nano

log "Ensuring pipx is installed..."
python -m pip install --upgrade pip wheel
python -m pip install --user pipx || true
python -m pipx ensurepath || true
export PATH="$HOME/.local/bin:$PATH"

log "Setting up zsh + auto-tmux..."
grep -q '.local/bin' ~/.zshrc 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
grep -q 'aliases.zsh' ~/.zshrc 2>/dev/null || echo '[ -f "$HOME/aliases.zsh" ] && source "$HOME/aliases.zsh"' >> ~/.zshrc
grep -q 'tmux new -As work' ~/.zshrc 2>/dev/null || printf '\n# auto tmux\nif [ -z "$TMUX" ]; then tmux new -As work; fi\n' >> ~/.zshrc

mkdir -p "$HOME/.logs" "$HOME/grosian_control" "$VAULT"

if [ ! -f "$HOME/aliases.zsh" ]; then
cat >> "$HOME/aliases.zsh" <<'ALIAS'
alias ll='ls -lah'
alias ta='tmux attach -t work || tmux new -s work'
alias td='tmux detach'
update() {
  echo "[update] termux pkgs…"; pkg update -y && pkg upgrade -y
  echo "[update] npm globals…"; command -v npm >/dev/null && npm update -g || true
  echo "[update] pipx tools…"; command -v pipx >/dev/null && pipx upgrade-all || true
  echo "[update] done."
}
ALIAS
fi

log "Installing Grosian control scripts..."

cat > "$HOME/grosian_control/backup.sh" <<'BKP'
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
REMOTE="${REMOTE:-gdrive}"
BUCKET="${BUCKET:-ZAAI_BACKUPS}"
DEVICE="${DEVICE:-A16}"
VAULT="${VAULT:-$HOME/ZA_AI_VAULT}"
DST="$REMOTE:$BUCKET/$DEVICE"
ARCHIVE="$REMOTE:${BUCKET}_ARCHIVE/$DEVICE"
LOG="\${LOG:-$HOME/.logs/backup.log}"
if ! rclone listremotes | grep -q "^\\\$REMOTE"; then
  echo "[backup] rclone remote '\$REMOTE' not configured. Run: rclone config"
  exit 0
fi
mkdir -p "\$VAULT" "\$(dirname "\$LOG")"
echo "[backup] \$(date -Is) syncing '\$VAULT' -> '\$DST'"
rclone sync "\$VAULT" "\$DST" --create-empty-src-dirs --fast-list --checksum \
  --transfers=8 --checkers=8 --progress --human-readable --stats-one-line \
  --backup-dir "\$ARCHIVE/\$(date +%F_%H-%M-%S)" \
  --exclude ".cache/**" \
  --log-file "\$LOG" --log-level INFO
echo "[backup] done."
BKP

cat > "$HOME/grosian_control/dedupe.sh" <<'DED'
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
python - <<'PY'
import os, hashlib, json, time
root = os.path.expanduser("~")
index = {}
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp,f)
        try:
            with open(p,'rb') as fh:
                h = hashlib.md5(fh.read()).hexdigest()
            index.setdefault(h, []).append(p)
        except Exception:
            pass
dupes = {h:paths for h,paths in index.items() if len(paths)>1}
out = os.path.expanduser("~/duplicate_report.json")
json.dump({"scanned":root,"ts":time.time(),"dupes":dupes}, open(out,"w"), indent=2)
print(f"[dedupe] wrote {out} with {sum(len(v)-1 for v in dupes.values())} duplicates")
PY
DED

cat > "$HOME/grosian_control/update.sh" <<'UPD'
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
echo "[update] termux packages…"; pkg update -y && pkg upgrade -y
echo "[update] npm globals…"; command -v npm >/dev/null && npm update -g || true
echo "[update] pipx upgrade-all…"; command -v pipx >/dev/null && pipx upgrade-all || true
echo "[update] done."
UPD

cat > "$HOME/grosian_control/health.sh" <<'HLT'
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
echo "====== HEALTH REPORT ======"
date -Is
echo "-- Disk usage (home) --"; du -sh "$HOME" 2>/dev/null | head -n1
echo "-- Cron jobs --"; crontab -l 2>/dev/null || echo "(none)"
echo "-- Last backup log --"; tail -n 20 "$HOME/.logs/backup.log" 2>/dev/null || echo "(no backups yet)"
echo "-- Rclone remotes --"; rclone listremotes || true
echo "==========================="
HLT

cat > "$HOME/grosian_control/grosian" <<'MST'
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
echo "[Grosian] Starting: update → dedupe → backup → health"
bash "$HOME/grosian_control/update.sh"
bash "$HOME/grosian_control/dedupe.sh"
bash "$HOME/grosian_control/backup.sh"
bash "$HOME/grosian_control/health.sh"
echo "[Grosian] All tasks complete."
MST

chmod +x "$HOME/grosian_control/"*.sh "$HOME/grosian_control/grosian"
grep -q 'grosian_control' ~/.zshrc 2>/dev/null || echo 'export PATH="$PATH:$HOME/grosian_control"' >> ~/.zshrc

log "Activating cron jobs..."
pgrep -f crond >/dev/null || (crond || true)
TMP="$(mktemp)"; crontab -l 2>/dev/null > "$TMP" || true
grep -q "Grosian Daily" "$TMP" || cat >> "$TMP" <<CRON
20 2 * * * $HOME/grosian_control/grosian >> $HOME/.logs/grosian_daily.log 2>&1
0 */6 * * * $HOME/grosian_control/backup.sh >> $HOME/.logs/backup.log 2>&1
CRON
crontab "$TMP"; rm -f "$TMP"

log "First-run test..."
mkdir -p "$VAULT/test"
echo "hello $(date -Is)" > "$VAULT/test/hello.txt"
if rclone listremotes | grep -q "^$REMOTE"; then
  bash "$HOME/grosian_control/backup.sh" || warn "backup skipped; check logs"
else
  warn "rclone remote '$REMOTE' not found. Run: rclone config"
fi

log "Done. Run 'grosian' anytime."
