Text file: README.md
Latest content with line numbers:
1	
2	# Supermind Cohesion Protocol — Reference Implementation (ZeroMQ + SQLite)
3	
4	Minimal, local-first bus + adapters so multiple AI agents can sync context, broadcast prompts, and return a merged answer.
5	
6	## Components
7	- `bus.py` — PUB server. Fan-out signed messages to all nodes.
8	- `node.py` — Subscribed worker. Identifies, fetches shared context, posts result.
9	- `synthesizer.py` — Aggregates node outputs and produces a merged answer.
10	- `vault.py` — Encrypted-hash journaling + SQLite shared state.
11	- `adapter_examples/` — Stubs to call external LLMs or local tools.
12	- `scripts/termux_install.sh` — Termux bootstrap.
13	- `scripts/termux_start.sh` — Start all services on Android.
14	
15	## Quick start
16	1) Install deps
17	```
18	python -m venv .venv && . .venv/bin/activate
19	pip install -r requirements.txt
20	```
21	2) Copy `config.example.json` to `config.json` and set `shared_secret`.
22	3) Start the bus:
23	```
24	python bus.py
25	```
26	4) Start one or more nodes (each in its own shell; set unique `AGENT_ID`):
27	```
28	AGENT_ID=chatgpt python node.py
29	AGENT_ID=gemini  python node.py
30	AGENT_ID=grok    python node.py
31	```
32	5) Start synthesizer:
33	```
34	python synthesizer.py
35	```
36	6) Send a prompt:
37	```
38	python tools/send_prompt.py "Summarize today's plan in 5 bullets."
39	```
40	
41	Outputs land in `artifacts/` as JSON and markdown.
42	
43	## Security
44	- All frames carry a unix `ts` and `HMAC-SHA256` signature of the payload using `shared_secret`.
45	- Nodes verify signatures and drop invalid frames.
46	- SQLite vault journaling records immutable hashes for audit.
47	
48	## Notes
49	- Transport: ZeroMQ (local LAN-friendly). Change `ZMQ_ENDPOINT` for remote.
50	- No external API keys included.
51	- Adapters are stubs: wire to your providers (OpenAI, Anthropic, etc).
52	- Termux scripts install Python and run services with sane defaults.
53	