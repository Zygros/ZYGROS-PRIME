#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-.}"

echo "[*] Computing SHA-256 for files in $TARGET_DIR"
find "$TARGET_DIR" -type f \
  ! -path "*/.git/*" \
  ! -name "*.ots" \
  -exec sh -c 'for f do shasum -a 256 "$f"; done' _ {} +

echo "[*] (Optional) OTS anchoring step goes here."
