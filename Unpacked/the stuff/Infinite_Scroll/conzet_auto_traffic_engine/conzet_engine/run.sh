#!/usr/bin/env bash
set -euo pipefail

if [ ! -f ".env" ]; then
  echo "Missing .env. Copy .env.example to .env and fill credentials."
  exit 1
fi

python3 scripts/scheduler.py --send hook --subject "You’re on the list — act now"
sleep 2
echo "Scheduled follow-up: run again when ready:"
echo "python3 scripts/scheduler.py --send followup --subject 'Still want in? Doors closing'"
echo "python3 scripts/scheduler.py --send last_call --subject 'LAST CALL — closing now'"
