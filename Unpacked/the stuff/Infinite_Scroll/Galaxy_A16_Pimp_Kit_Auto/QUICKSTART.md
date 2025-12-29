# Galaxy A16 Pimp Kit — Auto Installer (Termux)

## Quick Start (on phone)
1) Install **Termux** from F-Droid.
2) Download this file to your phone: `install_a16_pimpkit.sh`
3) In Termux:
   ```bash
   bash ~/install_a16_pimpkit.sh
   ```
4) Follow the prompts. When done:
   - Optional: `rclone config` to link Google Drive (remote name: `gdrive`).
   - Use `desktop/adb_debloat_*` on your computer for Samsung debloat.

## Debloat (from a computer)
- Install Android **platform-tools** (ADB).
- Connect phone via USB with **USB debugging** enabled.
- Run:
  - macOS/Linux: `./adb_debloat_mac_linux.sh`
  - Windows: double-click `adb_debloat_windows.bat`

## What gets installed
- Zsh, tmux, fzf, ripgrep, python, nodejs, rclone, cronie
- Aliases & tmux config
- `vault_backup_sync.sh` and `dedupe_scan.py`
- Crontab entries for automated backups & weekly dedupe

## Uninstall / Revert
- Re-enable any disabled package using: `adb shell pm enable <package>`
- Remove crontab: `crontab -r`
- Remove files: delete `~/aliases.zsh`, `~/.tmux.conf`, `~/vault_backup_sync.sh`, `~/dedupe_scan.py`
