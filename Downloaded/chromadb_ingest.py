
# chromadb_ingest.py
# Ingest a local folder (e.g., your exported Dropbox bundle) into ChromaDB.
# Requirements:
#   pip install chromadb pypdf python-docx markdown
# Usage:
#   python chromadb_ingest.py --path /path/to/folder --collection sovereign-archive
import argparse, os, hashlib, pathlib
from typing import List, Tuple
import chromadb
from chromadb.utils import embedding_functions

# Optional parsers (install if needed)
def read_text(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def read_md(path):
    return read_text(path)

def read_pdf(path):
    try:
        from pypdf import PdfReader
        r = PdfReader(path)
        return "\n".join([p.extract_text() or "" for p in r.pages])
    except Exception as e:
        return f"[PDF parse error: {e}]"

def read_docx(path):
    try:
        from docx import Document
        d = Document(path)
        return "\n".join([p.text for p in d.paragraphs])
    except Exception as e:
        return f"[DOCX parse error: {e}]"

def detect_and_read(path):
    ext = pathlib.Path(path).suffix.lower()
    if ext in ['.txt']:
        return read_text(path)
    if ext in ['.md']:
        return read_md(path)
    if ext in ['.pdf']:
        return read_pdf(path)
    if ext in ['.docx']:
        return read_docx(path)
    return ""  # skip unknown binaries

def sha256_of_bytes(b: bytes) -> str:
    import hashlib
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def sha256_of_text(t: str) -> str:
    return sha256_of_bytes(t.encode('utf-8'))

def gather_files(root: str) -> List[str]:
    keep = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in ['.txt','.md','.pdf','.docx']:
                keep.append(os.path.join(dirpath, fn))
    return keep

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', required=True)
    ap.add_argument('--collection', default='sovereign-archive')
    ap.add_argument('--persist_dir', default='./chroma_store')
    args = ap.parse_args()

    client = chromadb.PersistentClient(path=args.persist_dir)
    embedder = embedding_functions.DefaultEmbeddingFunction()  # swap for OpenAI or others if configured
    coll = client.get_or_create_collection(name=args.collection, embedding_function=embedder)

    files = gather_files(args.path)
    ids, docs, metas = [], [], []
    for i, fpath in enumerate(sorted(files)):
        txt = detect_and_read(fpath)
        if not txt.strip():
            continue
        doc_id = sha256_of_text(f"{fpath}:{len(txt)}")
        ids.append(doc_id)
        docs.append(txt[:200000])  # safety cap
        metas.append({"path": fpath})

        # batch insert every 64
        if len(ids) and len(ids) % 64 == 0:
            coll.add(ids=ids, documents=docs, metadatas=metas)
            ids, docs, metas = [], [], []

    if ids:
        coll.add(ids=ids, documents=docs, metadatas=metas)

    print(f"Ingested {len(files)} files into collection '{args.collection}'.")

if __name__ == "__main__":
    main()
