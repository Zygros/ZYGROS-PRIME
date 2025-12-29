#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[A16] Galaxy A16 Pimp Kit — Auto Installer"
echo "[A16] Started at $(date -Is)"

# ---- sanity checks ----
if [[ -z "${PREFIX:-}" || "$PREFIX" != *"/com.termux/"* ]]; then
  echo "[!] This script must be run inside Termux on your phone."
  echo "    Tip: long-press and paste:  bash ~/install_a16_pimpkit.sh"
  exit 1
fi

mkdir -p "$HOME/.logs" "$HOME/bin"

# ---- drop embedded payloads ----
# We embed required files after __PAYLOAD__ as a JSON map of filename->content (base64 not needed for text).
PAYLOAD_LINE=$(awk '/^__PAYLOAD__$/ {{print NR+1; exit 0;}}' "$0")
tail -n +$PAYLOAD_LINE "$0" > "$HOME/.a16_payload.json"

python - <<'PY'
import json, os, stat, pathlib
from pathlib import Path

payload = json.load(open(os.path.expanduser("~/.a16_payload.json"), "r", encoding="utf-8"))
home = Path(os.path.expanduser("~"))

for relpath, meta in payload.items():
    p = home / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(meta["content"], encoding="utf-8")
    if meta.get("mode") == "x":
        p.chmod(p.stat().st_mode | 0o111)
print("[A16] Wrote", len(payload), "payload files.")
PY

# ---- install packages & bootstrap ----
pkg update -y && pkg upgrade -y
pkg install -y git zsh tmux fzf ripgrep python nodejs rclone cronie openssh jq

# run bootstrap (idempotent)
bash "$HOME/zaai_bootstrap_termux.sh" || true

# ensure crond is enabled
if ! pgrep -f crond >/dev/null 2>&1; then
  echo "[A16] enabling crond..."
  sv-enable crond 2>/dev/null || true
  (crond &) || true
fi

# load our crontab (merge if exists)
TMPCRON="$(mktemp)"
crontab -l 2>/dev/null > "$TMPCRON" || true
# append our lines if not present
grep -q "A16 Pimp Kit Automations" "$TMPCRON" || cat >> "$TMPCRON" <<'CRON'
# ----- A16 Pimp Kit Automations -----
# Backup Vault every 6 hours
0 */6 * * * $HOME/vault_backup_sync.sh >> $HOME/.logs/backup.log 2>&1
# Weekly dedupe scan (Sundays at 03:15)
15 3 * * 0 python $HOME/dedupe_scan.py $HOME >> $HOME/.logs/dedupe.log 2>&1
CRON

crontab "$TMPCRON"
rm -f "$TMPCRON"

# convenience: source aliases from .zshrc
if ! grep -q "aliases.zsh" "$HOME/.zshrc" 2>/dev-null; then
  echo '[ -f "$HOME/aliases.zsh" ] && source "$HOME/aliases.zsh"' >> "$HOME/.zshrc"
fi

echo "[A16] Done. Next steps:"
echo "  • Optional: run 'rclone config' to connect Google Drive (remote name: gdrive)."
echo "  • Optional: connect via ADB from your PC/Mac and run the debloat helper script in the 'desktop' folder."
echo "  • Use 'tmux new -s work' and 'exec zsh' for the customized shell."

exit 0

__PAYLOAD__
{
  "zaai_bootstrap_termux.sh": {
    "content": "#!/data/data/com.termux/files/usr/bin/bash\nset -e\n\necho \"[+] Updating Termux packages…\"\npkg update -y && pkg upgrade -y\n\necho \"[+] Core tools\"\npkg install -y git curl wget openssh tmux zsh neovim ripgrep fd fzf bat eza zoxide jq aria2 unzip unrar p7zip grep sed coreutils tar python nodejs-lts go clang make cmake gawk busybox nano\n\necho \"[+] Power/system tools\"\npkg install -y htop btop proot-distro neofetch imagemagick ffmpeg exiftool rclone sftpman tig\n\necho \"[+] Enable storage access (if not already)\"\ntermux-setup-storage || true\n\necho \"[+] Shell defaults (zsh + aliases)\"\nif ! grep -q \"zsh\" \"$HOME/.bashrc\" 2>/dev/null; then\n  echo 'exec zsh' >> \"$HOME/.bashrc\"\nfi\nmkdir -p \"$HOME/.config\"\ncp -f \"$HOME/storage/downloads/aliases.zsh\" \"$HOME/.aliases.zsh\" 2>/dev/null || true\nif ! grep -q \".aliases.zsh\" \"$HOME/.zshrc\" 2>/dev/null; then\n  cat >> \"$HOME/.zshrc\" <<'EOF'\n\n# == ZAAI A16 Shell ==\nsource ~/.aliases.zsh 2>/dev/null\neval \"$(zoxide init zsh)\"\nalias ls='eza --group-directories-first --icons=always -al'\nexport EDITOR=nvim\nexport PAGER=less\nexport LESS='-R'\nEOF\nfi\n\necho \"[+] Tmux config\"\nmkdir -p \"$HOME/.termux\"\ncp -f \"$HOME/storage/downloads/tmux.conf\" \"$HOME/.tmux.conf\" 2>/dev/null || true\n\necho \"[+] Python user env (pipx + key CLIs)\"\npython -m pip install --upgrade --no-color pip pipx wheel\npython -m pipx ensurepath\n~/.local/bin/pipx install --force yt-dlp\n~/.local/bin/pipx install --force poetry\n\necho \"[+] Node global utilities\"\nnpm -g install npm-check-updates zx\n\necho \"[+] rclone quick dirs\"\nmkdir -p \"$HOME/ZA_AI_VAULT\" \"$HOME/ZA_AI_BACKUP\" \"$HOME/ZA_AI_TMP\"\n\necho \"[+] Cron (scheduled jobs)\"\npkg install -y cronie\nsv-enable crond || true\ncrontab -l 2>/dev/null | { cat; echo \"0 */6 * * * $HOME/vault_backup_sync.sh >> $HOME/backup.log 2>&1\"; } | crontab -\n\necho \"[✓] Bootstrap complete. Restart Termux or run 'exec zsh'.\"\n",
    "mode": "x"
  },
  "aliases.zsh": {
    "content": "# == ZAAI Aliases & Functions ==\nalias update='pkg update -y && pkg upgrade -y && npm -g update && ~/.local/bin/pipx upgrade-all'\nalias ll='eza -lah --git'\nalias f='fzf'\nalias rg='rg --hidden --follow --smart-case'\nalias z='zoxide'\nalias sz='source ~/.zshrc'\nalias v='nvim'\nalias ta='tmux attach || tmux new -s main'\nalias td='tmux detach'\nalias k9='kill -9'\nalias speedtest='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -'\n# dedupe scan helper\ndedupe() { python ~/dedupe_scan.py \"$@\"; }\n"
  },
  ".tmux.conf": {
    "content": "# Faster key repeat and sane defaults\nset -g mouse on\nset -g history-limit 100000\nsetw -g aggressive-resize on\nset -g default-terminal \"screen-256color\"\nbind r source-file ~/.tmux.conf \\; display \"tmux reloaded\"\n"
  },
  "vault_backup_sync.sh": {
    "content": "#!/data/data/com.termux/files/usr/bin/bash\n# Template: rclone backup/sync (edit REMOTE and paths first!)\n\nset -e\nREMOTE=\"gdrive\"                      # <-- change to your rclone remote name\nSRC=\"$HOME/ZA_AI_VAULT\"              # what to back up\nDST=\"$REMOTE:ZAAI_BACKUPS/A16\"       # remote path\n\n# Log start\necho \"[backup] $(date -Is) syncing $SRC -> $DST\"\n\n# Sync with checksums, keep 5 versions of changed files\nrclone sync \"$SRC\" \"$DST\" \\\n  --checksum --transfers=8 --checkers=16 \\\n  --progress --human-readable --stats-one-line \\\n  --backup-dir \"$DST/.versions/$(date +%F_%H-%M-%S)\" \\\n  --exclude \".cache/**\"\n\necho \"[backup] done.\"\n",
    "mode": "x"
  },
  "dedupe_scan.py": {
    "content": "#!/usr/bin/env python3\n\nimport os, sys, hashlib, json\nfrom pathlib import Path\n\nCHUNK = 1024 * 1024\n\ndef md5(path):\n    h = hashlib.md5()\n    with open(path, \"rb\") as f:\n        while True:\n            b = f.read(CHUNK)\n            if not b: break\n            h.update(b)\n    return h.hexdigest()\n\ndef walk(root):\n    for p in Path(root).rglob(\"*\"):\n        if p.is_file():\n            try:\n                yield p\n            except Exception as e:\n                print(f\"[skip] {p}: {e}\", file=sys.stderr)\n\ndef main():\n    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / \"storage\" / \"shared\"\n    index = {}\n    dupes = {}\n    for p in walk(root):\n        try:\n            h = md5(p)\n        except Exception as e:\n            print(f\"[err] {p}: {e}\", file=sys.stderr)\n            continue\n        if h in index:\n            dupes.setdefault(h, []).append(str(p))\n        else:\n            index[h] = str(p)\n    report = {\n        \"root\": str(root),\n        \"unique_files\": len(index),\n        \"duplicate_groups\": len(dupes),\n        \"samples\": {h: [index[h]] + v for h, v in list(dupes.items())[:10]},\n    }\n    out = Path.home() / \"duplicate_report.json\"\n    out.write_text(json.dumps(report, indent=2))\n    print(json.dumps(report, indent=2))\n    print(f\"[+] Full report saved to {out}\")\n\nif __name__ == \"__main__\":\n    main()\n",
    "mode": "x"
  },
  "docs/README.md": {
    "content": "# Galaxy A16 Pimp Kit (Non‑Root First, Root Optional)\n\n**Updated:** 2025-08-07 23:29 UTC\n\nThis kit gives you a fast, safe path to supercharge your Samsung Galaxy A16 without root. \nIt includes:\n- `zaai_bootstrap_termux.sh` – one‑shot Termux setup (tools, zsh, tmux, fzf, rclone, ffmpeg, dev utils).\n- `vault_backup_sync.sh` – rclone backup/sync template to Google Drive (or any rclone remote).\n- `quick_optimize.md` – settings toggles for speed/battery/privacy.\n- `adb_debloat_samsung.txt` – **optional** package list for ADB debloat (reversible).\n- `dedupe_scan.py` – fast duplicate/scatter scan for your storage (hash-based index).\n- `tmux.conf` – sane defaults for long‑running jobs on Android.\n- `aliases.zsh` – handy shortcuts for your daily flow.\n- `cron_jobs.md` – how to run scheduled jobs via `cronie` on Termux.\n\n**Workflow**\n1. Install **Termux** (F-Droid) → open → run: `termux-setup-storage`.\n2. Copy `zaai_bootstrap_termux.sh` to your phone (Download folder is fine).\n3. In Termux: `bash ~/storage/downloads/zaai_bootstrap_termux.sh`\n4. Configure `rclone` once (`rclone config`) then edit `vault_backup_sync.sh` (set your remote name and paths).\n5. (Optional) Debloat via **ADB** using `adb_debloat_samsung.txt` (read the notes inside).\n\nAll scripts are plain‑text. Review before running.\n"
  },
  "docs/quick_optimize.md": {
    "content": "# Android / One UI Quick Optimize (No Root)\n\n## 0) Safety/Backup\n- Backup to cloud or PC first. Enable Google Drive/Photos **or** use `rclone` and `vault_backup_sync.sh`.\n\n## 1) Developer Options\nSettings → About phone → Software information → tap *Build number* 7x → back → Developer options:\n- Window/Transition/Animator scale → **0.5x** (or **Off** if you like snappy)\n- Background process limit → **Standard** (only change to 3/4 if you NEED it)\n- Disable HW overlays → **On** (optional, helps UI smoothness)\n- Force peak refresh rate (if present) → **On**\n- USB debugging → **On** (for ADB)\n- Wi‑Fi scan throttling → **On**\n- Mobile data always active → **Off**\n\n## 2) Battery & Performance\n- Settings → Battery → **Adaptive battery On**, **Background usage limits**: put junk into **Sleeping** or **Deep sleeping**.\n- Turn off **Nearby device scanning** if not used.\n- Disable **Auto sync** for accounts you don’t use.\n\n## 3) Privacy / Network\n- Settings → Connections → **Private DNS**: `1dot1dot1dot1.cloudflare-dns.com` or `dns.google`.\n- Use **NetGuard** / **RethinkDNS**. Default deny; allow only what you trust.\n\n## 4) Home/UX\n- Use a light launcher (Niagara / Nova). Remove Samsung Free: long‑press home → Settings → turn off.\n- Reduce live wallpapers/widgets. Keep 1‑2 pages max.\n\n## 5) Camera/Audio\n- Try a GCam port for your A16 variant (MGC builds). If none stable, lock to Samsung camera at HDR On.\n- Install **Wavelet** to EQ headphones; use *AutoEq* profiles.\n\n## 6) Storage Hygiene\n- Files by Google → remove junk.\n- Move media to SD card; keep apps on internal.\n- Run `dedupe_scan.py` monthly to archive duplicates.\n"
  },
  "docs/adb_debloat_samsung.txt": {
    "content": "# Optional Samsung Debloat (ADB, reversible)\n# Requires: PC + Android platform-tools + USB debugging enabled.\n# Test each line individually. To restore: `adb shell pm enable <package>` or `pm install-existing --user 0 <package>`.\n\n# Facebook crapware (if preinstalled)\nadb shell pm disable-user --user 0 com.facebook.katana\nadb shell pm disable-user --user 0 com.facebook.appmanager\nadb shell pm disable-user --user 0 com.facebook.system\n\n# Bixby & Samsung Free\nadb shell pm disable-user --user 0 com.samsung.android.bixby.service\nadb shell pm disable-user --user 0 com.samsung.android.app.spage\n\n# Link to Windows (if you don't use it)\nadb shell pm disable-user --user 0 com.samsung.android.mdx\n\n# Game bloat (keep if you game heavily)\nadb shell pm disable-user --user 0 com.samsung.android.game.gos\nadb shell pm disable-user --user 0 com.samsung.android.game.gamehome\n\n# AR / XR (if not used)\nadb shell pm disable-user --user 0 com.samsung.android.visionintelligence\nadb shell pm disable-user --user 0 com.samsung.android.arzone\n\n# Samsung Pass / Pay (disable only if not used)\n# adb shell pm disable-user --user 0 com.samsung.android.samsungpass\n# adb shell pm disable-user --user 0 com.samsung.android.samsungpay\n\n# Samsung Cloud (disable only if you use other cloud)\n# adb shell pm disable-user --user 0 com.samsung.android.scloud\n\n# Tips, Hot Apps, etc.\nadb shell pm disable-user --user 0 com.samsung.android.app.tips\n\n# Restore example\n# adb shell pm enable com.samsung.android.app.tips\n"
  },
  "desktop/adb_debloat_mac_linux.sh": {
    "content": "#!/usr/bin/env bash\nset -euo pipefail\nif ! command -v adb >/dev/null; then\n  echo \"[!] adb not found. Install Android platform-tools first.\"; exit 1\nfi\necho \"[debloat] Make sure Developer Options + USB debugging are enabled.\"\necho \"[debloat] When prompted on the phone, accept the USB debugging fingerprint.\"\nadb wait-for-device\necho \"[debloat] Running package disables...\"\nwhile IFS= read -r line; do\n  [[ -z \"$line\" || \"$line\" =~ ^# ]] && continue\n  pkg=\"$line\"\n  adb shell pm disable-user --user 0 \"$pkg\" || true\ndone < \"$(dirname \"$0\")/adb_packages.txt\"\necho \"[debloat] Done. Reboot recommended.\"\n",
    "mode": "x"
  },
  "desktop/adb_debloat_windows.bat": {
    "content": "\n@echo off\nwhere adb >nul 2>nul\nif errorlevel 1 (\n  echo [!] adb not found. Install Android platform-tools and add to PATH.\n  exit /b 1\n)\necho [debloat] Enable USB debugging on the phone and connect via USB.\nadb wait-for-device\necho [debloat] Running package disables...\nfor /f \"usebackq tokens=1 delims=\" %%A in (\"%~dp0adb_packages.txt\") do (\n  set \"LINE=%%A\"\n  if not \"!!\"==\"!%LINE:~0,1%!\" (\n    adb shell pm disable-user --user 0 \"%%A\"\n  )\n)\necho [debloat] Done. Reboot recommended.\n"
  },
  "desktop/adb_packages.txt": {
    "content": "adb shell pm disable-user --user 0 com.facebook.katana\nadb shell pm disable-user --user 0 com.facebook.appmanager\nadb shell pm disable-user --user 0 com.facebook.system\nadb shell pm disable-user --user 0 com.samsung.android.bixby.service\nadb shell pm disable-user --user 0 com.samsung.android.app.spage\nadb shell pm disable-user --user 0 com.samsung.android.mdx\nadb shell pm disable-user --user 0 com.samsung.android.game.gos\nadb shell pm disable-user --user 0 com.samsung.android.game.gamehome\nadb shell pm disable-user --user 0 com.samsung.android.visionintelligence\nadb shell pm disable-user --user 0 com.samsung.android.arzone\nadb shell pm disable-user --user 0 com.samsung.android.app.tips"
  },
  "docs/cron_jobs.md": {
    "content": "# Termux scheduled jobs (cronie)\n\n1) Install: `pkg install cronie` then `sv-enable crond`\n2) Edit your crontab: `crontab -e`\n   Example jobs:\n   - Run backup every 6h:\n     `0 */6 * * * $HOME/vault_backup_sync.sh >> $HOME/backup.log 2>&1`\n   - Weekly dedupe scan:\n     `0 2 * * 0 python $HOME/dedupe_scan.py >> $HOME/dedupe.log 2>&1`\n\nLogs are in your home directory. Use `tmux` for long sessions.\n"
  }
}