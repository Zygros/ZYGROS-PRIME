import os, json, requests
from dotenv import load_dotenv
load_dotenv()
WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")
PAYMENT_URL = os.getenv("PAYMENT_URL")
QR = os.getenv("ASSET_QR","assets/ascension_kit_qr.png")

def post_message(content: str):
    if not WEBHOOK:
        raise SystemExit("DISCORD_WEBHOOK_URL missing in .env")
    data = {"content": content.replace("{PAYMENT_URL}", PAYMENT_URL)}
    r = requests.post(WEBHOOK, json=data, timeout=20)
    r.raise_for_status()
    print("Posted to Discord webhook.")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="messages/hook.txt")
    args = ap.parse_args()
    with open(args.template, "r", encoding="utf-8") as f:
        content = f.read()
    post_message(content + f"\n\n{PAYMENT_URL}")
