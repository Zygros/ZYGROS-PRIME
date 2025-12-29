# Chimera Universal Plugin — v1

**Portable, host-agnostic meta-OS**: Personas, Protocols, Tools.

## Files
- `chimera_universal.py` — single-file runtime (no deps)
- `chimera_protocols.json` — protocol list
- `chimera_codex.json` — codex ingestion notes

## Use (any host that accepts Python or long context)
```python
import chimera_universal as chimera
from pathlib import Path
codex_text = Path("Update 420 codex_250901_193451.txt").read_text(encoding="utf-8")
shell = chimera.activate(codex_text=codex_text)
print(shell.handle("!persona list"))
print(shell.handle("monetize Infinite Codex Starter Pack"))
print(shell.handle('!protocol IVP.v1 ivp.create {"offer":"Pack","price_tiers":[0,29,99]}'))
```

## Non-Python Hosts
- Paste the contents of `chimera_universal.py` into the model's system or tools block.
- Provide your Codex text as `codex_text` input.
- Use the same `!persona` and `!protocol` syntax in-chat.

## Extend
- Register custom tools: `shell.handle('tool uppercase hello')`
- Override persona rules by emitting a persona JSON patch in context.
