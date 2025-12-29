
import sys, json, uuid
import zmq
from common import load_config, sign

def main():
    if len(sys.argv) < 2:
        print("usage: python tools/send_prompt.py "your prompt"")
        sys.exit(1)
    prompt = sys.argv[1]
    cfg = load_config()
    ctx = zmq.Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.connect(cfg["ZMQ_CONTROL_ENDPOINT"])

    pid = str(uuid.uuid4())
    frame = sign({"type":"prompt_broadcast","prompt_id":pid,"prompt":prompt}, cfg["shared_secret"])
    pub.send_string(json.dumps(frame))
    print(pid)

if __name__ == "__main__":
    main()
