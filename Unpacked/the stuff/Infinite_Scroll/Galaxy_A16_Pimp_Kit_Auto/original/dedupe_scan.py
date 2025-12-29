#!/usr/bin/env python3

import os, sys, hashlib, json
from pathlib import Path

CHUNK = 1024 * 1024

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b: break
            h.update(b)
    return h.hexdigest()

def walk(root):
    for p in Path(root).rglob("*"):
        if p.is_file():
            try:
                yield p
            except Exception as e:
                print(f"[skip] {p}: {e}", file=sys.stderr)

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "storage" / "shared"
    index = {}
    dupes = {}
    for p in walk(root):
        try:
            h = md5(p)
        except Exception as e:
            print(f"[err] {p}: {e}", file=sys.stderr)
            continue
        if h in index:
            dupes.setdefault(h, []).append(str(p))
        else:
            index[h] = str(p)
    report = {
        "root": str(root),
        "unique_files": len(index),
        "duplicate_groups": len(dupes),
        "samples": {h: [index[h]] + v for h, v in list(dupes.items())[:10]},
    }
    out = Path.home() / "duplicate_report.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"[+] Full report saved to {out}")

if __name__ == "__main__":
    main()
