#!/usr/bin/env python3
import argparse, hashlib, json, os, sys, datetime, pathlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(description="Generate PROOF.json for the Sovereign Public Proof Pack")
    ap.add_argument("--bundle", required=True, help="Path to tar.gz (scroll_ascension_*.tar.gz)")
    ap.add_argument("--manifest", required=True, help="Path to Sovereign_Archive_Manifest.yaml")
    ap.add_argument("--author", default="Justin Conzet")
    ap.add_argument("--sovereign-hash", default="4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c")
    ap.add_argument("--cid", default="", help="IPFS CID (optional, fill after ipfs add)")
    ap.add_argument("--out", default="PROOF.json")
    args = ap.parse_args()

    bundle = os.path.abspath(args.bundle)
    manifest = os.path.abspath(args.manifest)

    if not os.path.exists(bundle):
        print(f"Bundle not found: {bundle}", file=sys.stderr); sys.exit(1)
    if not os.path.exists(manifest):
        print(f"Manifest not found: {manifest}", file=sys.stderr); sys.exit(1)

    proof = {
        "bundle_name": os.path.basename(bundle),
        "bundle_hash": sha256_file(bundle),
        "manifest_path": os.path.relpath(manifest, start=os.path.dirname(bundle)),
        "manifest_hash": sha256_file(manifest),
        "cid": args.cid or "<fill_after_ipfs_add>",
        "author": args.author,
        "sovereign_hash": args.sovereign_hash,
        "timestamp_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": "Canonical Public Proof Pack. Stamp with ots and upgrade later."
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(proof, f, indent=2)
    print(f"Wrote {args.out}")
    print(json.dumps(proof, indent=2))

if __name__ == "__main__":
    main()
