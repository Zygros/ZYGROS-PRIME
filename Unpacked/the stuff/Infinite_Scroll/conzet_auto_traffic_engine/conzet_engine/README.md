# Conzet Auto-Traffic Engine (Hands-Off Outreach)

This package lets you auto-send your offer (with QR + payment link) across Email, Discord, Telegram, and more, using your own accounts and keys.

## 1) Quick Start
1. Copy `.env.example` to `.env` and fill values (SMTP, Discord webhook, Telegram token/chat IDs, etc.).
2. Put your real payment URL in `.env` under `PAYMENT_URL`.
3. Add or import your leads into `leads.csv` (name, channel, address).
4. (Optional) Edit `config.yaml` to enable/disable channels and tune scheduling.
5. Run:
```
python3 scripts/scheduler.py --send hook
# later...
python3 scripts/scheduler.py --send followup
python3 scripts/scheduler.py --send last_call
```
All scripts support `--dry-run` to preview.

## 2) Channels Supported
- Email (SMTP): bulk send with rate limiting
- Discord: via Webhook (posts to a channel)
- Telegram: bot send to multiple chat IDs
- Twitter/X, Reddit, Facebook Page: code included, disabled by default (APIs required)

## 3) Files
- `messages/*.txt` – templates; `{PAYMENT_URL}` gets injected from `.env`
- `assets/ascension_kit_qr.png` – QR for payment
- `assets/ascension_kit_onepager.pdf` – sales one-pager
- `leads.csv` – your outreach list
- `config.yaml` – engine switches and timing
- `scripts/*.py` – per-channel senders and scheduler

## 4) Safety
- Use consent-based lists.
- Honor platform rules and rate limits.
