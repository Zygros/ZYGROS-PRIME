
import sys, json, uuid, zmq
from common import load_config, sign

def main():
    if len(sys.argv) < 2:
        print("usage: python tools/update_context.py '{"key":"value"}'")
        sys.exit(1)
    ctx_payload = json.loads(sys.argv[1])
    cfg = load_config()
    ctx = zmq.Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.connect(cfg["ZMQ_CONTROL_ENDPOINT"])
    frame = sign({"type":"context_update","context":ctx_payload}, cfg["shared_secret"])
    pub.send_string(json.dumps(frame))
    print("ok")

if __name__ == "__main__":
    main()
