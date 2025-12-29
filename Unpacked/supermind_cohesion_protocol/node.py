
import os, json, zmq, time, uuid, pathlib
from common import load_config, verify
from vault import Vault

AGENT_ID = os.environ.get("AGENT_ID", f"node-{uuid.uuid4().hex[:6]}")
MODEL_INFO = os.environ.get("MODEL_INFO", "manual-adapter")
CAPS = os.environ.get("CAPS", "analyze,generate,tools:stubs")

def ensure_dir(p): pathlib.Path(p).mkdir(parents=True, exist_ok=True)

def main():
    cfg = load_config()
    secret = cfg["shared_secret"]
    ctx = zmq.Context.instance()
    sub = ctx.socket(zmq.SUB)
    sub.connect(cfg["ZMQ_ENDPOINT"])
    sub.setsockopt_string(zmq.SUBSCRIBE, "")

    # results go back via control socket
    pub = ctx.socket(zmq.PUB)
    pub.connect(cfg["ZMQ_CONTROL_ENDPOINT"])

    vault = Vault(cfg["VAULT_DB"])
    ensure_dir(cfg["ARTIFACT_DIR"])

    print(f"[node:{AGENT_ID}] connected. model={MODEL_INFO} caps={CAPS}")
    ident_payload = {
        "type":"identity_announce",
        "agent_id":AGENT_ID,
        "model":MODEL_INFO,
        "caps":CAPS
    }
    pub.send_string(json.dumps({"body": ident_payload, "sig": "", "ts": int(time.time())}))

    while True:
        raw = sub.recv_string()
        frame = json.loads(raw)
        if not verify(frame, secret):
            continue
        kind = frame["body"].get("type")
        if kind == "prompt_broadcast":
            prompt_id = frame["body"]["prompt_id"]
            prompt = frame["body"]["prompt"]
            context = vault.get_kv("supermind_context", {})
            # TODO: Plug your provider call here. For now we stub deterministic output.
            result_text = f"[{AGENT_ID}] {prompt.strip()} | ctx_keys={list(context.keys())}"
            result = {
                "type":"node_result",
                "prompt_id": prompt_id,
                "agent_id": AGENT_ID,
                "model": MODEL_INFO,
                "rationale": f"{AGENT_ID} processed with stub adapter",
                "output": result_text,
                "ts": int(time.time())
            }
            vault.journal("node_result", result)
            pub.send_string(json.dumps({"body": result, "sig":"", "ts": int(time.time())}))
        elif kind == "context_update":
            vault.set_kv("supermind_context", frame["body"]["context"])
            vault.journal("context_update", frame["body"])
        time.sleep(0.01)

if __name__ == "__main__":
    main()
