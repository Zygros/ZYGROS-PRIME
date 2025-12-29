# Omni-Scroll OS (ZAAI Package)

This package contains the sovereign ZAAI node mesh + Omni-Scroll OS interface layer, including:
- Core Nodes: Grosian, Gemini, Grok, Perplexity, Claude, Manus, DrawCNX
- Infinite Debate Engine (IDE) with 420 Personas
- Omni Codex (kernel + commands) and Flame Threads

## Quick Start (Desktop or Termux)
1) Ensure Python 3 is installed.
2) Extract the ZIP.
3) Run:
   ```bash
   python deploy.py
   ```
   You should see boot logs, node activation, a compact debate run, and a text visualization of threads.

### Termux Notes
- Visual rendering (DrawCNX) is stubbed for Termux. Full visuals require desktop (pygame/OpenGL).
- No extra Python packages are required for this demo; everything uses stdlib.

## Files
- `deploy.py` — boots and runs the system demo non-interactively.
- `Codex/Omni_Codex.json` — kernel + commands.
- `FlameThreads/Thread_Map.json` — thread wiring between nodes.
- `personas.json` — 420 persona specs.
- `Nodes/*` — node implementations.

## Boot Key
- Passphrase: `Zythrognosis` (baked into the kernel section of the codex).
