# phoenix_operator.py
# Combined Operator: run server or act as CLI against a running node.
# Subcommands:
#   serve                  -> run Flask API
#   status/query/ingest    -> same signatures as phoenix_cli.py
#
# Env: CHROMA_PERSIST_DIR, COLLECTION_NAME, API_PORT, HOST, API_KEY

import os
import sys
import argparse
import json
import requests

def run_server():
    # defer import so that operator can run CLI without flask deps until needed
    import phoenix_node_genesis as node
    node.main()

def with_api_key(headers):
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

def do_ingest_json(host: str, paths, recursive, docs):
    payload = {"paths": paths, "recursive": recursive, "documents": docs}
    r = requests.post(f"{host}/api/ingest", json=payload, headers=with_api_key({"Content-Type":"application/json"}))
    print(r.status_code, json.dumps(r.json(), indent=2))

def do_ingest_files(host: str, files, prefix: str):
    fs = [("files", (os.path.basename(p), open(p, "rb"))) for p in files]
    data = {"prefix": prefix}
    r = requests.post(f"{host}/api/ingest", files=fs, data=data, headers=with_api_key({}))
    print(r.status_code, json.dumps(r.json(), indent=2))

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("serve")
    sp.add_argument("--host", default=None, help="Override HOST env for this run")
    sp.add_argument("--port", type=int, default=None, help="Override API_PORT env for this run")

    hp = sub.add_parser("status")
    hp.add_argument("--host", default="http://localhost:5001")

    qp = sub.add_parser("query")
    qp.add_argument("--host", default="http://localhost:5001")
    qp.add_argument("query")
    qp.add_argument("-n", "--n_results", type=int, default=3)

    ip = sub.add_parser("ingest")
    ip.add_argument("--host", default="http://localhost:5001")
    ip.add_argument("--path", action="append")
    ip.add_argument("--recursive", action="store_true")
    ip.add_argument("--files", nargs="*")
    ip.add_argument("--prefix", default="upload")
    ip.add_argument("--text")
    ip.add_argument("--id")
    ip.add_argument("--meta")

    args = ap.parse_args()

    if args.cmd == "serve":
        if args.host:
            os.environ["HOST"] = args.host
        if args.port is not None:
            os.environ["API_PORT"] = str(args.port)
        run_server()
        return

    if args.cmd == "status":
        do_status(args.host); return

    if args.cmd == "query":
        do_query(args.host, args.query, args.n_results); return

    if args.cmd == "ingest":
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
