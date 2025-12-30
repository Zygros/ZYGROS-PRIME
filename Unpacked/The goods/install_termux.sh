#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# -------------------------------
# 🝎 SACC — Termux Dependency Installer (Safe/Pip-Friendly)
# This installs the minimal packages needed for SACC on Termux.
# It WILL NOT try to upgrade pip (Termux forbids that).
# -------------------------------

echo "🝎 SACC Installer — Termux"

# Ask for storage permission once (no deletion of your files)
if command -v termux-setup-storage >/dev/null 2>&1; then
  if [ ! -d "$HOME/storage" ]; then
    echo "• Requesting storage permission (Android popup)…"
    termux-setup-storage || true
  fi
fi

echo "• Updating Termux packages…"
pkg update -y >/dev/null

echo "• Installing prerequisites…"
# python (runtime), python-pip (pip), unzip (extract zip), git (optional), termux-api (clipboard/openers), coreutils (sha256sum etc)
pkg install -y python python-pip unzip git termux-api coreutils >/dev/null

# Confirm versions so you know what's installed
python --version
pip --version

# If a requirements.txt exists in this folder, install it (user scope to avoid permission issues)
if [ -f "requirements.txt" ]; then
  echo "• Installing Python deps from requirements.txt (user scope)…"
  pip install --user -r requirements.txt
else
  echo "• No requirements.txt found — skipping Python deps."
fi

# Make helper scripts executable if present
if [ -f "bin/open_url.sh" ]; then
  chmod +x bin/open_url.sh
fi

echo "✅ SACC Installer complete."
