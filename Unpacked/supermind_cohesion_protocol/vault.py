
import sqlite3, os, json, hashlib, time
from typing import Dict, Any

SCHEMA = '''
CREATE TABLE IF NOT EXISTS journal (
  id INTEGER PRIMARY KEY,
  ts INTEGER NOT NULL,
  kind TEXT NOT NULL,
  payload TEXT NOT NULL,
  hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS kv (
  k TEXT PRIMARY KEY,
  v TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
'''

class Vault:
    def __init__(self, path: str):
        self.path = path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with sqlite3.connect(self.path) as c:
            c.executescript(SCHEMA)

    def journal(self, kind: str, payload: Dict[str, Any]) -> str:
        ts = int(time.time())
        blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        h = hashlib.sha256(f"{ts}:{kind}:{blob}".encode()).hexdigest()
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT INTO journal(ts,kind,payload,hash) VALUES(?,?,?,?)",
                      (ts, kind, blob, h))
        return h

    def set_kv(self, k: str, v: Dict[str, Any]):
        ts = int(time.time())
        blob = json.dumps(v, ensure_ascii=False)
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT INTO kv(k,v,updated_ts) VALUES(?,?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v, updated_ts=excluded.updated_ts",
                      (k, blob, ts))

    def get_kv(self, k: str, default=None):
        with sqlite3.connect(self.path) as c:
            cur = c.execute("SELECT v FROM kv WHERE k=?", (k,))
            row = cur.fetchone()
            return json.loads(row[0]) if row else default

    def recent_journal(self, since_ts: int):
        with sqlite3.connect(self.path) as c:
            cur = c.execute("SELECT ts,kind,payload,hash FROM journal WHERE ts>=? ORDER BY ts ASC", (since_ts,))
            for ts, kind, payload, h in cur.fetchall():
                yield {"ts": ts, "kind": kind, "payload": json.loads(payload), "hash": h}
