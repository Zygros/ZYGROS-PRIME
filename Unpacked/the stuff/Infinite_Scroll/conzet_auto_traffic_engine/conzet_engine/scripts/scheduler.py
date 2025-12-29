import os, time, csv, argparse, yaml
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open("config.yaml","r",encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_template(path: str) -> str:
    with open(path,"r",encoding="utf-8") as f:
        return f.read()

def inject_vars(text: str) -> str:
    payment_url = os.getenv("PAYMENT_URL","https://example.com/pay")
    return text.replace("{PAYMENT_URL}", payment_url)

def send_email_batch(leads_csv, template_path, subject):
    from send_email import bulk_send as email_bulk
    email_bulk(leads_csv, template_path, subject)

def send_discord(template_path):
    from post_discord import post_message
    content = inject_vars(load_template(template_path))
    post_message(content + "\n")

def send_telegram(template_path):
    from send_telegram import send_message, CHAT_IDS
    content = inject_vars(load_template(template_path))
    for cid in CHAT_IDS:
        if cid:
            try:
                send_message(cid, content)
            except Exception as e:
                print(f"Telegram error for {cid}: {e}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", choices=["hook","followup","last_call"], required=True)
    ap.add_argument("--leads", default="leads.csv")
    ap.add_argument("--subject", default="You’re on the list — act now")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    msg_file = cfg["messages"][args.send]
    content = inject_vars(load_template(msg_file))

    print(f"[Conzet Scheduler] Stage: {args.send}")
    print(content)
    if args.dry_run:
        print("Dry run; no sends performed.")
        raise SystemExit()

    if cfg["targets"]["email"]["enabled"]:
        send_email_batch(args.leads, msg_file, args.subject)

    if cfg["targets"]["discord"]["enabled"]:
        send_discord(msg_file)

    if cfg["targets"]["telegram"]["enabled"]:
        send_telegram(msg_file)

    print("Dispatch complete.")
