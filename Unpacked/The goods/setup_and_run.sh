#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# -------------------------------
# 🝎 SACC One-Step Termux Setup & Launch
# This script:
# 1) Grants storage, updates Termux, installs Python/pip/unzip/git/termux-api
# 2) Locates SACC.zip (Downloads or current dir)
# 3) Verifies SHA-256 hash
# 4) Unzips into ~/SACC (or ~/SACC-<n> if taken)
# 5) Runs install_termux.sh (if present)
# 6) Launches python sacc.py
# -------------------------------

EXPECTED_SHA="6303b67ae4f554979717f7e70bf36da600a574535082b9b68c2e088693449cce"

echo "🝎 Sovereign AI Command Console — One-Step Setup"
echo "• Granting storage access (first run may prompt)…"
if command -v termux-setup-storage >/dev/null 2>&1; then
  termux-setup-storage || true
fi

echo "• Updating Termux packages…"
pkg update -y >/dev/null

echo "• Installing prerequisites: python, pip, unzip, git, termux-api…"
pkg install -y python python-pip unzip git termux-api >/dev/null

# Make sure pip is available and fresh
python -m ensurepip >/dev/null 2>&1 || true
pip install --upgrade pip >/dev/null

# Try to find SACC.zip in common locations
echo "• Searching for SACC.zip…"
ZIP_CANDIDATES=(
  "$PWD/SACC.zip"
  "$HOME/SACC.zip"
  "$HOME/downloads/SACC.zip"
  "$HOME/Downloads/SACC.zip"
  "/sdcard/Download/SACC.zip"
  "/sdcard/Downloads/SACC.zip"
)

ZIP_PATH=""
for p in "${ZIP_CANDIDATES[@]}"; do
  if [ -f "$p" ]; then ZIP_PATH="$p"; break; fi
done

if [ -z "$ZIP_PATH" ]; then
  echo "❌ Could not find SACC.zip."
  echo "   Please download it to your phone and place it in one of these:"
  printf "   - %s\n" "${ZIP_CANDIDATES[@]}"
  exit 1
fi

echo "• Found: $ZIP_PATH"
echo "• Verifying SHA-256…"

# Some Androids have 'sha256sum' available; fallback to busybox if present
if command -v sha256sum >/dev/null 2>&1; then
  ACTUAL_SHA="$(sha256sum "$ZIP_PATH" | awk '{print $1}')"
elif command -v busybox >/dev/null 2>&1; then
  ACTUAL_SHA="$(busybox sha256sum "$ZIP_PATH" | awk '{print $1}')"
else
  echo "⚠️  sha256sum not found; installing coreutils…"
  pkg install -y coreutils >/dev/null
  ACTUAL_SHA="$(sha256sum "$ZIP_PATH" | awk '{print $1}')"
fi

if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
  echo "❌ SHA-256 mismatch!"
  echo "   Expected: $EXPECTED_SHA"
  echo "   Actual:   $ACTUAL_SHA"
  echo "   Aborting for your safety. Re-download SACC.zip and retry."
  exit 2
fi
echo "✅ Hash verified."

# Choose a target directory (~/SACC or ~/SACC-<n> if exists)
TARGET="$HOME/SACC"
i=1
while [ -e "$TARGET" ]; do
  TARGET="$HOME/SACC-$i"
  i=$((i+1))
done

echo "• Unzipping to: $TARGET"
mkdir -p "$TARGET"
unzip -q "$ZIP_PATH" -d "$TARGET"

cd "$TARGET"

# Run bundle installer if present
if [ -f "install_termux.sh" ]; then
  echo "• Running bundle installer…"
  chmod +x install_termux.sh
  bash install_termux.sh
else
  echo "⚠️  install_termux.sh not found in bundle — continuing."
fi

# Optional: ensure Python deps from requirements.txt
if [ -f "requirements.txt" ]; then
  echo "• Installing Python requirements…"
  # Use user install to avoid permission issues
  pip install --user -r requirements.txt
fi

# Launch the console
if [ -f "sacc.py" ]; then
  echo "• Launching SACC console…"
  exec python sacc.py
else
  echo "❌ sacc.py not found in $TARGET"
  exit 3
fi
