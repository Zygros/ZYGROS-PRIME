
import zmq, json, time, os
from common import load_config, sign

# Acts as a dumb relay for signed frames. Publishes on ZMQ_ENDPOINT.
# Also listens for control messages on ZMQ_CONTROL_ENDPOINT for admin events.

def main():
    cfg = load_config()
    endpoint = cfg["ZMQ_ENDPOINT"]
    ctrl_endpoint = cfg["ZMQ_CONTROL_ENDPOINT"]

    ctx = zmq.Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.bind(endpoint)

    sub = ctx.socket(zmq.SUB)
    sub.bind(ctrl_endpoint)
    sub.setsockopt_string(zmq.SUBSCRIBE, "")

    print(f"[bus] PUB {endpoint} | CTRL {ctrl_endpoint}")
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)

    while True:
        socks = dict(poller.poll(timeout=200))
        if sub in socks:
            raw = sub.recv_string()
            try:
                msg = json.loads(raw)
                # control fanout for e.g., topology pings
                pub.send_string(json.dumps(msg))
            except Exception as e:
                print("[bus] invalid control message:", e)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
