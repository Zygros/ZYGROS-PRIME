import os, requests
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_IDS = [x.strip() for x in os.getenv("TELEGRAM_CHAT_IDS","").split(",") if x.strip()]
PAYMENT_URL = os.getenv("PAYMENT_URL")

def send_message(chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="messages/hook.txt")
    args = ap.parse_args()
    with open(args.template, "r", encoding="utf-8") as f:
        text = f.read().replace("{PAYMENT_URL}", PAYMENT_URL)
    for cid in CHAT_IDS:
        send_message(cid, text + f"\n\n{PAYMENT_URL}")
    print("Sent to Telegram chat IDs.")
