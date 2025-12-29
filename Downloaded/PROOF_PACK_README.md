# Public Proof Pack — Quickstart

## Files
- PROOF.json.template — Fill manually if you prefer
- generate_proof_json.py — Generates PROOF.json with computed SHA-256 hashes
- proof_pack.sh — One-command helper to build tarball, hash, and stamp

## Typical flow
```bash
# 1) Build your public pack directory, containing Sovereign_Archive_Manifest.yaml and all public artifacts.
./proof_pack.sh <your_public_pack_dir>

# 2) (Optional) Publish to IPFS and then update CID:
ipfs add scroll_ascension_*.tar.gz
python3 generate_proof_json.py --bundle scroll_ascension_*.tar.gz --manifest <your_public_pack_dir>/Sovereign_Archive_Manifest.yaml --cid <CID> --out PROOF.json

# 3) Anchor to Bitcoin:
ots stamp PROOF.json
ots upgrade PROOF.json.ots
```
Generated 2025-11-02T23:05:00Z UTC.
