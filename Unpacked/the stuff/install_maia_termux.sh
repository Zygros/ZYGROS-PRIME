\
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
echo ">>> 🔥 MAIA Termux Installer (v1.3.0)"

# 0) Sanity
if ! command -v termux-info >/dev/null 2>&1; then
  echo "This script is intended for Termux on Android." >&2
  exit 1
fi

# 1) Packages
echo ">>> 📦 Updating packages"
pkg update -y
pkg install -y python termux-api git tmux

# 2) Layout
MAIA_DIR="$HOME/maia"
mkdir -p "$MAIA_DIR" "$MAIA_DIR/logs"

# 3) Install binary
cp -f "$(dirname "$0")/maia.py" "$MAIA_DIR/maia.py"
chmod +x "$MAIA_DIR/maia.py"

# 4) CLI shim
BIN="$PREFIX/bin/maia"
cat > "$BIN" <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
exec "$HOME/maia/maia.py" "$@"
SH
chmod +x "$BIN"

echo ">>> ✅ Installed. Try:  maia shell"
