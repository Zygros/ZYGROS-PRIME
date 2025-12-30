#!/data/data/com.termux/files/usr/bin/bash
# Omni-Scroll OS mobile launcher (Termux)
PKG_DIR=~/storage/Documents/God\ Documents/OmniScroll_OS_ZAAI
mkdir -p "$PKG_DIR"
SCRIPT_DIR="$(dirname "$0")"

# Sync current package to God Documents
cp -r "$SCRIPT_DIR"/.. "$PKG_DIR" 2>/dev/null || true

cd "$PKG_DIR" || exit 1
echo "[Omni-Scroll] Booting…"
python deploy.py
