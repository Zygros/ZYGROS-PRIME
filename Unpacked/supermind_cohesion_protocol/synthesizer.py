
import os, json, time, uuid, pathlib, zmq
from common import load_config, verify
from vault import Vault

def ensure_dir(p): pathlib.Path(p).mkdir(parents=True, exist_ok=True)

def merge(outputs):
    # Simple merge: list bullet points and note disagreements by string distance
    lines = []
    for o in outputs:
        lines.append(f"- {o['agent_id']}: {o['output']}")
    summary = "\n".join(lines)
    return summary

def main():
    cfg = load_config()
    secret = cfg["shared_secret"]
    ctx = zmq.Context.instance()
    sub = ctx.socket(zmq.SUB)
    sub.connect(cfg["ZMQ_CONTROL_ENDPOINT"])
    sub.setsockopt_string(zmq.SUBSCRIBE, "")

    pub = ctx.socket(zmq.PUB)
    pub.connect(cfg["ZMQ_CONTROL_ENDPOINT"])

    vault = Vault(cfg["VAULT_DB"])
    ensure_dir(cfg["ARTIFACT_DIR"])

    window = cfg["synthesis"]["collection_window_sec"]
    max_wait = cfg["synthesis"]["max_wait_sec"]

    print("[synth] collecting node results...")

    pending = {}
    last_emit = {}

    while True:
        raw = sub.recv_string()
        try:
            frame = json.loads(raw)
        except Exception:
            continue

        body = frame.get("body", {})
        kind = body.get("type")

        if kind == "node_result":
            pid = body["prompt_id"]
            pending.setdefault(pid, []).append(body)
            # emit if window or max_wait exceeded
            ts0 = last_emit.get(pid, body["ts"])
            if (time.time() - ts0) >= window:
                outs = pending.pop(pid, [])
                merged = merge(outs)
                artifact_md = os.path.join(cfg["ARTIFACT_DIR"], f"{pid}.md")
                with open(artifact_md, "w") as f:
                    f.write("# Supermind Synthesized Answer\n\n")
                    f.write(merged + "\n")
                vault.journal("synth_out", {"prompt_id": pid, "merged_path": artifact_md, "n_parts": len(outs)})
                last_emit[pid] = time.time()
        time.sleep(0.01)

if __name__ == "__main__":
    main()
