import os, smtplib, time, csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST=os.getenv("SMTP_HOST")
SMTP_PORT=int(os.getenv("SMTP_PORT","587"))
SMTP_USER=os.getenv("SMTP_USER")
SMTP_PASS=os.getenv("SMTP_PASS")
SMTP_FROM=os.getenv("SMTP_FROM", SMTP_USER)
PAYMENT_URL=os.getenv("PAYMENT_URL")
ASSET_QR=os.getenv("ASSET_QR","assets/ascension_kit_qr.png")
ASSET_PDF=os.getenv("ASSET_PDF","assets/ascension_kit_onepager.pdf")
RATE_PER_MINUTE=int(os.getenv("RATE_PER_MINUTE","20"))

def render_message(template_path: str) -> str:
    with open(template_path, "r", encoding="utf-8") as f:
        txt = f.read()
    return txt.replace("{PAYMENT_URL}", PAYMENT_URL)

def send_email(to_addr, subject, body, attach_qr=True, attach_pdf=True):
    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if attach_qr and os.path.exists(ASSET_QR):
        with open(ASSET_QR, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(ASSET_QR))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ASSET_QR)}"'
        msg.attach(part)

    if attach_pdf and os.path.exists(ASSET_PDF):
        with open(ASSET_PDF, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(ASSET_PDF))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ASSET_PDF)}"'
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def bulk_send(leads_csv, template_path, subject):
    body = render_message(template_path)
    with open(leads_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if row["channel"].lower() != "email":
                continue
            addr = row["address"]
            send_email(addr, subject, body)
            count += 1
            if RATE_PER_MINUTE > 0 and count % RATE_PER_MINUTE == 0:
                time.sleep(60)
    print("Email sends complete.")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--leads", default="leads.csv")
    ap.add_argument("--template", default="messages/hook.txt")
    ap.add_argument("--subject", default="You’re on the list — act now")
    args = ap.parse_args()
    bulk_send(args.leads, args.template, args.subject)
