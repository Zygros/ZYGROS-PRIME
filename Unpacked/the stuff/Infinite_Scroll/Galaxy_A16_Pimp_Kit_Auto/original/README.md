# Galaxy A16 Pimp Kit (Non‑Root First, Root Optional)

**Updated:** 2025-08-07 23:29 UTC

This kit gives you a fast, safe path to supercharge your Samsung Galaxy A16 without root. 
It includes:
- `zaai_bootstrap_termux.sh` – one‑shot Termux setup (tools, zsh, tmux, fzf, rclone, ffmpeg, dev utils).
- `vault_backup_sync.sh` – rclone backup/sync template to Google Drive (or any rclone remote).
- `quick_optimize.md` – settings toggles for speed/battery/privacy.
- `adb_debloat_samsung.txt` – **optional** package list for ADB debloat (reversible).
- `dedupe_scan.py` – fast duplicate/scatter scan for your storage (hash-based index).
- `tmux.conf` – sane defaults for long‑running jobs on Android.
- `aliases.zsh` – handy shortcuts for your daily flow.
- `cron_jobs.md` – how to run scheduled jobs via `cronie` on Termux.

**Workflow**
1. Install **Termux** (F-Droid) → open → run: `termux-setup-storage`.
2. Copy `zaai_bootstrap_termux.sh` to your phone (Download folder is fine).
3. In Termux: `bash ~/storage/downloads/zaai_bootstrap_termux.sh`
4. Configure `rclone` once (`rclone config`) then edit `vault_backup_sync.sh` (set your remote name and paths).
5. (Optional) Debloat via **ADB** using `adb_debloat_samsung.txt` (read the notes inside).

All scripts are plain‑text. Review before running.
