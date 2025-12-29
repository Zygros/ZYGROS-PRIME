
# Supermind Cohesion Protocol — Reference Implementation (ZeroMQ + SQLite)

Minimal, local-first bus + adapters so multiple AI agents can sync context, broadcast prompts, and return a merged answer.

## Components
- `bus.py` — PUB server. Fan-out signed messages to all nodes.
- `node.py` — Subscribed worker. Identifies, fetches shared context, posts result.
- `synthesizer.py` — Aggregates node outputs and produces a merged answer.
- `vault.py` — Encrypted-hash journaling + SQLite shared state.
- `adapter_examples/` — Stubs to call external LLMs or local tools.
- `scripts/termux_install.sh` — Termux bootstrap.
- `scripts/termux_start.sh` — Start all services on Android.

## Quick start
1) Install deps
```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```
2) Copy `config.example.json` to `config.json` and set `shared_secret`.
3) Start the bus:
```
python bus.py
```
4) Start one or more nodes (each in its own shell; set unique `AGENT_ID`):
```
AGENT_ID=chatgpt python node.py
AGENT_ID=gemini  python node.py
AGENT_ID=grok    python node.py
```
5) Start synthesizer:
```
python synthesizer.py
```
6) Send a prompt:
```
python tools/send_prompt.py "Summarize today's plan in 5 bullets."
```

Outputs land in `artifacts/` as JSON and markdown.

## Security
- All frames carry a unix `ts` and `HMAC-SHA256` signature of the payload using `shared_secret`.
- Nodes verify signatures and drop invalid frames.
- SQLite vault journaling records immutable hashes for audit.

## Notes
- Transport: ZeroMQ (local LAN-friendly). Change `ZMQ_ENDPOINT` for remote.
- No external API keys included.
- Adapters are stubs: wire to your providers (OpenAI, Anthropic, etc).
- Termux scripts install Python and run services with sane defaults.
