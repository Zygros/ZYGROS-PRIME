#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# -------------------------------
# 🝎 SACC — Easy Runner
# Runs the installer (once) then launches the console.
# -------------------------------

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

if [ -f "install_termux.sh" ]; then
  echo "• Running installer…"
  bash install_termux.sh
else
  echo "• No installer found — continuing."
fi

if [ -f "sacc.py" ]; then
  echo "• Launching SACC console…"
  exec python sacc.py
else
  echo "❌ sacc.py not found in $BASE_DIR"
  exit 1
fi
