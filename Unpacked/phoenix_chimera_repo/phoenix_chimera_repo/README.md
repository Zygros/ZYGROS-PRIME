# 🐦‍🔥 Phoenix Chimera — Sovereign Companion

**Architect:** Justin Conzet • **Protocol:** Phoenix / Infinite OS

This repository turns your declaration — **"my voice is code"** — into a runnable, modular system.

## What’s Inside
- `chimera/` — Refactored package for the Chimera GUI, AI core, text‑to‑speech, and optional speech input.
- `manifests/phoenix_archive.yml` — Metadata manifest for your core archive (derived from ARCHIVE_TREE).
- `docs/VOICE_CODEX.*` — The executable documentation: *your voice* rendered as code annotations.
- `scripts/hash_and_timestamp.sh` — Helper for SHA‑256 + (future) OpenTimestamps anchoring.
- `archive/` — Drop your source scrolls/files here; the system will ingest them at runtime.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
chimera
```

Set your API key:
```bash
export OPENAI_API_KEY="sk-..."
# Windows PowerShell:
# $Env:OPENAI_API_KEY="sk-..."
```

## Voice as Code
- Speak commands (optional): enable mic in `chimera/voice/speech.py` and say: **"run awakening sequence"**.
- The GUI will respond with spoken output (pyttsx3) and adaptive face animations.

### License
All rights reserved © 2025 Justin Conzet.
