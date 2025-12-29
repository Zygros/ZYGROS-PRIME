
import os, json, hmac, hashlib, time
from typing import Dict, Any

def load_config():
    path = os.environ.get("SUPERMIND_CONFIG", "config.json")
    with open(path, "r") as f:
        return json.load(f)

def sign(payload: Dict[str, Any], secret: str) -> Dict[str, Any]:
    body = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    mac = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return {"ts": int(time.time()), "body": payload, "sig": mac}

def verify(frame: Dict[str, Any], secret: str) -> bool:
    body = json.dumps(frame["body"], sort_keys=True, ensure_ascii=False).encode()
    mac = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, frame.get("sig",""))
