#!/data/data/com.termux/files/usr/bin/bash
# Template: rclone backup/sync (edit REMOTE and paths first!)

set -e
REMOTE="gdrive"                      # <-- change to your rclone remote name
SRC="$HOME/ZA_AI_VAULT"              # what to back up
DST="$REMOTE:ZAAI_BACKUPS/A16"       # remote path

# Log start
echo "[backup] $(date -Is) syncing $SRC -> $DST"

# Sync with checksums, keep 5 versions of changed files
rclone sync "$SRC" "$DST" \
  --checksum --transfers=8 --checkers=16 \
  --progress --human-readable --stats-one-line \
  --backup-dir "$DST/.versions/$(date +%F_%H-%M-%S)" \
  --exclude ".cache/**"

echo "[backup] done."
