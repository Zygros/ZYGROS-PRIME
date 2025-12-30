#!/usr/bin/env bash
set -e
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_NAME="PromptSovereign_v1.zip"
cd "$ROOT_DIR/.."
zip -r "$PKG_NAME" "PromptSovereign_v1_20250917_235027" > /dev/null
echo "Created $PKG_NAME"
