# phoenix_cli.py
# Simple CLI to interact with Phoenix Codex Node
# Usage examples:
#   python phoenix_cli.py status --host http://localhost:5001
#   python phoenix_cli.py query "what is the phoenix?" -n 5
#   python phoenix_cli.py ingest --path ./docs --recursive
#   python phoenix_cli.py ingest --text "inline content" --id mydoc --meta '{"path":"inline:mydoc"}'

import os
import json
import argparse
from typing import List, Dict, Any
import requests

def with_api_key(headers: Dict[str,str]) -> Dict[str,str]:
    key = os.getenv("API_KEY")
    if key:
        headers = dict(headers)
        headers["X-API-Key"] = key
    return headers

def do_status(host: str) -> None:
    r = requests.get(f"{host}/api/status", headers=with_api_key({}))
    print(r.status_code, json.dumps(r.json(), indent=2))

def do_query(host: str, query: str, n: int) -> None:
    payload = {"query": query, "n_results": n}
    r = requests.post(f"{host}/api/query", json=payload, headers=with_api_key({"Content-Type":"application/json"}))
    print(r.status_code, json.dumps(r.json(), indent=2))

def do_ingest_json(host: str, paths: List[str], recursive: bool, docs: List[Dict[str, Any]]) -> None:
    payload = {"paths": paths, "recursive": recursive, "documents": docs}
    r = requests.post(f"{host}/api/ingest", json=payload, headers=with_api_key({"Content-Type":"application/json"}))
    print(r.status_code, json.dumps(r.json(), indent=2))

def do_ingest_files(host: str, files: List[str], prefix: str) -> None:
    fs = [("files", (os.path.basename(p), open(p, "rb"))) for p in files]
    data = {"prefix": prefix}
    r = requests.post(f"{host}/api/ingest", files=fs, data=data, headers=with_api_key({}))
    print(r.status_code, json.dumps(r.json(), indent=2))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="http://localhost:5001", help="Phoenix node base URL")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("status")

    qp = sub.add_parser("query")
    qp.add_argument("query")
    qp.add_argument("-n", "--n_results", type=int, default=3)

    ip = sub.add_parser("ingest")
    ip.add_argument("--path", action="append", help="Path(s) to a file or directory (can repeat)")
    ip.add_argument("--recursive", action="store_true", help="Recurse into directories (default true if not using --files)")
    ip.add_argument("--files", nargs="*", help="Upload file(s) via multipart")
    ip.add_argument("--prefix", default="upload", help="prefix for multipart uploads")
    ip.add_argument("--text", help="inline text to ingest")
    ip.add_argument("--id", help="id for inline text (required if --text)")
    ip.add_argument("--meta", help="metadata JSON for inline text")

    args = ap.parse_args()

    if args.cmd == "status":
        do_status(args.host)
    elif args.cmd == "query":
        do_query(args.host, args.query, args.n_results)
    elif args.cmd == "ingest":
        docs = []
        if args.text:
            if not args.id:
                raise SystemExit("--id is required when using --text")
            meta = {}
            if args.meta:
                meta = json.loads(args.meta)
            docs.append({"id": args.id, "text": args.text, "metadata": meta})

        if args.files:
            do_ingest_files(args.host, args.files, args.prefix)
        else:
            paths = args.path or []
            recursive = True if (args.path and not args.files) else bool(args.recursive)
            do_ingest_json(args.host, paths, recursive, docs)

if __name__ == "__main__":
    main()
