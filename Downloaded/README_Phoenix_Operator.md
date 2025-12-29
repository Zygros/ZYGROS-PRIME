# Phoenix Operator Pack (API + CLI + Ingest)

This bundle gives you **all three**:
1. A hardened Flask API with `/api/status`, `/api/query`, and `/api/ingest`.
2. A CLI client (`phoenix_cli.py`) to talk to a running node.
3. A combined operator (`phoenix_operator.py`) that can either `serve` or invoke `status|query|ingest`.

---

## 0) Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install flask chromadb requests pypdf python-docx markdown
```

*(If you don't need PDF/DOCX, you can skip `pypdf` and `python-docx`.)*

## 1) Run the server

```bash
export CHROMA_PERSIST_DIR=./chroma_store
export COLLECTION_NAME=sovereign-archive
export API_PORT=5001
# optional: require a key for all calls
export API_KEY="change-me"

python phoenix_node_genesis.py
# or
python phoenix_operator.py serve --host 0.0.0.0 --port 5001
```

## 2) Status

```bash
python phoenix_cli.py status --host http://localhost:5001
# or
python phoenix_operator.py status --host http://localhost:5001
```

## 3) Query

```bash
python phoenix_cli.py query "core architecture overview" -n 5
# or
python phoenix_operator.py query --host http://localhost:5001 "core architecture overview" -n 5
```

## 4) Ingest

### A) From paths (directories/files)
```bash
python phoenix_cli.py ingest --path ./docs --recursive
# or
python phoenix_operator.py ingest --host http://localhost:5001 --path ./docs --recursive
```

### B) Upload files via multipart
```bash
python phoenix_cli.py ingest --files ./a.md ./b.pdf --prefix mydrop
# or
python phoenix_operator.py ingest --host http://localhost:5001 --files ./a.md ./b.pdf --prefix mydrop
```

### C) Inline document
```bash
python phoenix_cli.py ingest --text "hello sovereign" --id inline-1 --meta '{"path":"inline:inline-1"}'
# or
python phoenix_operator.py ingest --host http://localhost:5001 --text "hello sovereign" --id inline-1 --meta '{"path":"inline:inline-1"}'
```

> Metadata always includes a `path` (inline, file, or upload) so sources are traceable in query results.

## Security

If `API_KEY` is set on the server, clients must send `X-API-Key: <key>`. The CLI and operator read `API_KEY` from your environment and include it automatically.

## Notes

- Supported file types by default: `.txt, .md, .markdown, .pdf, .docx`
- You can expand extractors if needed. For PDFs/DOCX the server uses best-effort extraction via `pypdf` and `python-docx`.
- The API returns cosine-distance-like scores from Chroma so you can rank/threshold on the client side.
```

