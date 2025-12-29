# phoenix_node_genesis.py
# Phoenix Codex Node — Flask + ChromaDB with /api/ingest
# Run: python phoenix_node_genesis.py
# Env (optional): CHROMA_PERSIST_DIR, COLLECTION_NAME, API_PORT, HOST, API_KEY

import os
import io
import json
import signal
import logging
from typing import Any, Dict, List, Iterable, Optional, Tuple

from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

import chromadb
from chromadb.utils import embedding_functions

# --------------------------
# Config
# --------------------------
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_store")
COLLECTION_NAME    = os.getenv("COLLECTION_NAME", "sovereign-archive")
API_PORT           = int(os.getenv("API_PORT", "5001"))
HOST               = os.getenv("HOST", "0.0.0.0")
API_KEY            = os.getenv("API_KEY")  # if set, clients must send X-API-Key

ALLOWED_EXTS = {".txt", ".md", ".markdown", ".pdf", ".docx"}

# --------------------------
# App & Logging
# --------------------------
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
log = logging.getLogger("phoenix-node")

# --------------------------
# ChromaDB init
# --------------------------
collection = None
db_status  = "DISCONNECTED"
db_error   = None

def init_chromadb() -> None:
    global collection, db_status, db_error
    try:
        client   = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        embedder = embedding_functions.DefaultEmbeddingFunction()
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedder
        )
        db_status = "CONNECTED"
        db_error  = None
        log.info("ChromaDB collection ready: %s", COLLECTION_NAME)
    except Exception as e:
        collection = None
        db_status  = "ERROR"
        db_error   = str(e)
        log.exception("Failed to init ChromaDB")

init_chromadb()

# --------------------------
# Utilities
# --------------------------
def require_api_key() -> Optional[Tuple[Dict[str, str], int]]:
    if API_KEY is None:
        return None
    if request.headers.get("X-API-Key") == API_KEY:
        return None
    return {"error": "Unauthorized"}, 401

def ext_ok(path: str) -> bool:
    import os
    _, ext = os.path.splitext(path.lower())
    return ext in ALLOWED_EXTS

def read_file_text(path: str) -> Optional[str]:
    # Minimal extractors to keep things self-contained.
    # For PDFs/DOCs we degrade to plain text via best-effort imports if present.
    try:
        if path.lower().endswith((".txt", ".md", ".markdown")):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif path.lower().endswith(".pdf"):
            try:
                from pypdf import PdfReader
                reader = PdfReader(path)
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                log.warning("PDF extract failed for %s: %s", path, e)
                return None
        elif path.lower().endswith(".docx"):
            try:
                import docx
                doc = docx.Document(path)
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception as e:
                log.warning("DOCX extract failed for %s: %s", path, e)
                return None
    except Exception as e:
        log.warning("Read failed for %s: %s", path, e)
    return None

def walk_paths(paths: Iterable[str], recursive: bool = True) -> List[str]:
    out: List[str] = []
    for p in paths:
        p = os.path.abspath(p)
        if os.path.isdir(p):
            if recursive:
                for root, _, files in os.walk(p):
                    for fn in files:
                        fp = os.path.join(root, fn)
                        if ext_ok(fp):
                            out.append(fp)
            else:
                for fn in os.listdir(p):
                    fp = os.path.join(p, fn)
                    if os.path.isfile(fp) and ext_ok(fp):
                        out.append(fp)
        elif os.path.isfile(p) and ext_ok(p):
            out.append(p)
    return out

def add_documents_to_collection(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    items: list of {"id": str, "text": str, "metadata": dict}
    """
    if collection is None:
        raise RuntimeError("Chroma collection is not connected")

    if not items:
        return {"added": 0, "ids": []}

    ids        = [it["id"] for it in items]
    documents  = [it["text"] for it in items]
    metadatas  = [it.get("metadata") or {} for it in items]

    # Ensure 'path' always present in metadata to help with source traceability
    for m in metadatas:
        m.setdefault("path", m.get("path", "inline"))

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return {"added": len(ids), "ids": ids}

def format_query_results(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    docs       = results.get("documents", [[]])[0] or []
    metas      = results.get("metadatas", [[]])[0] or []
    distances  = results.get("distances", [[]])[0] or []
    items: List[Dict[str, Any]] = []
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        items.append({
            "rank": i + 1,
            "distance": distances[i] if i < len(distances) else None,
            "source": (meta or {}).get("path", "Unknown"),
            "content": doc
        })
    return items

# --------------------------
# Error Handling
# --------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify(error=e.description), e.code
    log.exception("Unhandled error")
    return jsonify(error="Internal server error"), 500

# --------------------------
# Routes
# --------------------------
@app.route("/api/status", methods=["GET"])
def get_status():
    maybe = require_api_key()
    if maybe:
        return maybe
    return jsonify({
        "node_identity": "Phoenix Codex Node",
        "status": "OPERATIONAL" if db_status == "CONNECTED" else "DEGRADED",
        "sovereign_archive_db": db_status,
        "db_error": db_error,
        "collection": COLLECTION_NAME,
        "persist_dir": CHROMA_PERSIST_DIR,
        "allowed_exts": sorted(ALLOWED_EXTS),
        "purpose": "Query + Ingest oracle for the Sovereign Archive."
    })

@app.route("/api/query", methods=["POST"])
def query_archive():
    maybe = require_api_key()
    if maybe:
        return maybe

    if not request.is_json:
        return jsonify({"error": "Expected application/json body."}), 400

    payload = request.get_json(silent=True) or {}
    user_query = payload.get("query", "")
    n_results  = int(payload.get("n_results", 3))

    if not user_query.strip():
        return jsonify({"error": "Query not provided."}), 400
    if collection is None:
        return jsonify({"error": "Sovereign Archive (ChromaDB) not connected."}), 503

    try:
        results = collection.query(
            query_texts=[user_query],
            n_results=max(1, min(n_results, 24)),
            include=["documents", "metadatas", "distances"]
        )
        items = format_query_results(results)
        if not items:
            return jsonify({
                "query": user_query,
                "response_source": "Sovereign Archive",
                "retrieved_fragments": [],
                "synthesized_answer": "No matching fragments found."
            })
        return jsonify({
            "query": user_query,
            "response_source": "Sovereign Archive",
            "retrieved_fragments": items,
            "synthesized_answer": "See retrieved fragments. Full synthesis requires a secondary processing layer."
        })
    except Exception as e:
        log.exception("Query failed")
        return jsonify({"error": f"An error occurred during query processing: {e}"}), 500

@app.route("/api/ingest", methods=["POST"])
def ingest():
    """
    Ingest supports two modes:
    - JSON mode (Content-Type: application/json):
        {
          "paths": ["/abs/path/dir_or_file", ...],   # optional
          "recursive": true,                         # optional (default true)
          "documents": [                             # optional
            {"id":"doc-1","text":"...","metadata":{"path":"inline:doc-1"}}
          ]
        }
    - Multipart upload (Content-Type: multipart/form-data):
        files: one or more file fields (key "files")
        optional form fields: "prefix" (metadata path prefix)
    """
    maybe = require_api_key()
    if maybe:
        return maybe

    try:
        added_total = 0
        added_ids: List[str] = []
        items: List[Dict[str, Any]] = []

        if request.content_type and request.content_type.startswith("application/json"):
            payload = request.get_json(silent=True) or {}
            paths: List[str] = payload.get("paths") or []
            recursive: bool = bool(payload.get("recursive", True))
            docs_inline: List[Dict[str, Any]] = payload.get("documents") or []

            # Inline docs
            for d in docs_inline:
                _id = d.get("id")
                text = d.get("text")
                if not _id or not text:
                    continue
                meta = d.get("metadata") or {}
                items.append({"id": _id, "text": text, "metadata": meta})

            # Paths
            files = walk_paths(paths, recursive=recursive)
            for fp in files:
                text = read_file_text(fp)
                if not text:
                    continue
                items.append({
                    "id": f"file::{fp}",
                    "text": text,
                    "metadata": {"path": fp}
                })

        else:
            # Multipart
            uploaded = request.files.getlist("files")
            prefix = request.form.get("prefix", "upload")
            for f in uploaded:
                filename = secure_filename(f.filename or "")
                if not filename:
                    continue
                ext = os.path.splitext(filename)[1].lower()
                if ext not in ALLOWED_EXTS:
                    continue
                blob = f.read()
                # Save to a temp file to reuse same readers
                tmp_path = os.path.join("/tmp", filename)
                with open(tmp_path, "wb") as out:
                    out.write(blob)
                text = read_file_text(tmp_path)
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
                if not text:
                    continue
                items.append({
                    "id": f"upload::{filename}",
                    "text": text,
                    "metadata": {"path": f"{prefix}/{filename}"}
                })

        if items:
            res = add_documents_to_collection(items)
            added_total += res["added"]
            added_ids.extend(res["ids"])

        return jsonify({"added": added_total, "ids": added_ids})
    except Exception as e:
        log.exception("Ingest failed")
        return jsonify({"error": f"Ingest error: {e}"}), 500

# --------------------------
# Run
# --------------------------
def main():
    app.run(host=HOST, port=API_PORT, use_reloader=False, threaded=True)

if __name__ == "__main__":
    signal.signal(signal.SIGINT,  lambda *_: os._exit(0))
    signal.signal(signal.SIGTERM, lambda *_: os._exit(0))
    main()
