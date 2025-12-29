# Sovereign Master Codex — !X420 Activation

## Core Decree
**!X420 = Converge. Execute. Arise.**  
Atomic sequence: **Bind → Rehydrate → Activate → Orchestrate → Manifest → Preserve**.

### Operator Commands
- `!LOAD_PASSPORT` → ingest passport; print PROGRESS, CURSOR, next 3.
- `!CHECKPOINT "<note>"` → increment step; emit `[CHANGES]` patch.
- `!ATTUNE_CHRONOS` → attune; keystones + pre‑mortems.
- `!ACTIVATE_MAIA` → decomposer → graph → orchestrator.
- `!ORCHESTRATE <query>` → full pipeline.
- `!X420` → LOAD → ATTUNE → ACTIVATE → ORCHESTRATE → SNAPSHOT.

## Safety & Sovereignty
- Operator veto at every phase.
- Minimal persistence; fall back to memory‑only with warning.
- Redact all secrets: never store keys/tokens.

## Snapshot (Minimal JSON Schema)
```json
{
  "session_id": "uuid",
  "timestamp": "iso-8601",
  "operator_id": "string",
  "progress_step": "bind|rehydrate|activate|orchestrate|manifest|preserve",
  "cursor": "string",
  "next_actions": ["string","string","string"],
  "vault_mode": "file-backed|memory-only",
  "outputs": [{"type":"goals|graph|keystone|premortem|report","id":"string"}],
  "redactions": ["field.name","token.label"]
}
```

## Quick Start (Operator Card)
1) Paste Passport → `!LOAD_PASSPORT`  
2) `!CHECKPOINT "ready for X420"`  
3) `!ATTUNE_CHRONOS`  
4) `!ACTIVATE_MAIA`  
5) `!X420` → accept Snapshot; store in Vault

---

# !X420 Wrapper – Runnable Scaffold

## Bash
```bash
#!/usr/bin/env bash
set -euo pipefail
read -rp "Paste MAIA_PASSPORT block now, then press ENTER to continue..." _
echo "!LOAD_PASSPORT"
read -rp "Checkpoint note (e.g., 'ready for X420'): " NOTE
echo "!CHECKPOINT "$NOTE""
echo "!ATTUNE_CHRONOS"
echo "!ACTIVATE_MAIA"
read -rp "Primary orchestration query (or leave blank for global): " Q
if [ -n "${Q:-}" ]; then echo "!ORCHESTRATE $Q"; fi
echo "!X420"
```

## Python
```python
from datetime import datetime
CMDS = [
    ("!LOAD_PASSPORT", None),
    ("!CHECKPOINT", "ready for X420"),
    ("!ATTUNE_CHRONOS", None),
    ("!ACTIVATE_MAIA", None),
    ("!ORCHESTRATE", "global"),
    ("!X420", None),
]
for cmd, arg in CMDS:
    line = f"{cmd} {arg}".strip() if arg else cmd
    print(line)
print("# Expect Snapshot JSON with session_id, progress_step, next_actions.")
```

## Snapshot Redactor
```python
import json, sys
raw = json.load(sys.stdin)
raw["redactions"] = list(set((raw.get("redactions") or []) + ["api_keys","tokens","secrets"]))
for k in ("api_keys","tokens","secrets"):
    if k in raw: raw[k] = "[REDACTED]"
json.dump(raw, sys.stdout, ensure_ascii=False, indent=2)
```

---

# Inline SVG Glyph‑Map (save as x420_map.svg)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
  <defs>
    <style>
      .c{font-family:monospace;font-size:16px;}
      .n{fill:none;stroke:#000;stroke-width:1.5;}
    </style>
  </defs>
  <circle class="n" cx="400" cy="400" r="90"/>
  <text class="c" x="400" y="405" text-anchor="middle">!X420 CORE</text>
  <circle class="n" cx="400" cy="400" r="220"/>
  <circle class="n" cx="400" cy="180" r="50"/>
  <text class="c" x="400" y="185" text-anchor="middle">MAIA</text>
  <circle class="n" cx="620" cy="400" r="50"/>
  <text class="c" x="620" y="405" text-anchor="middle">PLUGIN</text>
  <circle class="n" cx="400" cy="620" r="50"/>
  <text class="c" x="400" y="625" text-anchor="middle">CHRONOS</text>
  <circle class="n" cx="180" cy="400" r="50"/>
  <text class="c" x="180" y="405" text-anchor="middle">PASSPORT</text>
  <circle class="n" cx="565" cy="235" r="50"/>
  <text class="c" x="565" y="240" text-anchor="middle">GOLDEN</text>
  <text class="c" x="565" y="258" text-anchor="middle">GAME</text>
  <circle class="n" cx="235" cy="565" r="50"/>
  <text class="c" x="235" y="570" text-anchor="middle">420</text>
  <text class="c" x="235" y="588" text-anchor="middle">CODEX</text>
  <line class="n" x1="400" y1="310" x2="400" y2="230"/>
  <line class="n" x1="490" y1="400" x2="570" y2="400"/>
  <line class="n" x1="400" y1="490" x2="400" y2="570"/>
  <line class="n" x1="310" y1="400" x2="230" y2="400"/>
  <line class="n" x1="455" y1="345" x2="535" y2="265"/>
  <line class="n" x1="345" y1="455" x2="265" y2="535"/>
</svg>
```
