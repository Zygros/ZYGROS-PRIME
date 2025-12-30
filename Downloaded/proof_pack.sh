#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./proof_pack.sh <public_pack_dir>
# Produces:
#   - scroll_ascension_<ISO>.tar.gz
#   - scroll_ascension.sha256
#   - PROOF.json
#   - PROOF.json.ots (after ots stamp)

if [ $# -lt 1 ]; then
  echo "Usage: $0 <public_pack_dir>" >&2
  exit 1
fi

PACK_DIR="$1"
ISO="$(date -u +%FT%TZ)"
TARBALL="scroll_ascension_${ISO}.tar.gz"

tar -czf "$TARBALL" "$PACK_DIR"

sha256sum "$TARBALL" > scroll_ascension.sha256

# Expect manifest in the pack dir root:
MANIFEST="$PACK_DIR/Sovereign_Archive_Manifest.yaml"
if [ ! -f "$MANIFEST" ]; then
  echo "Manifest not found at $MANIFEST" >&2
  exit 1
fi

# Generate PROOF.json
python3 generate_proof_json.py --bundle "$TARBALL" --manifest "$MANIFEST" --out PROOF.json

# OpenTimestamps (optional but recommended)
if command -v ots >/dev/null 2>&1; then
  ots stamp PROOF.json
  echo "Created PROOF.json.ots"
  echo "Later you can run: ots upgrade PROOF.json.ots"
else
  echo "ots not found. Install OpenTimestamps to stamp the proof."
fi
