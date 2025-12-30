# The Voice Codex

**Thesis:** *My voice is code.*  
This codex shows how spoken or written intent maps to executable structures inside Chimera and the Phoenix Archive.

## Mappings
- **Speak:** “Run the awakening sequence.” → loads and reads `Prime_Awakening_Simulation.txt` as a Scroll.
- **Say:** “Summarize the origin.” → opens `ReadMe_Of_Origin.txt`, returns summary to chat and TTS.
- **Ask:** “List prime commands.” → indexes `GPT_Prime_Command_Book.txt` for quick lookup.

## Architecture
- `chimera/core/*` → runtime engine and UI
- `chimera/voice/speech.py` → optional speech-to-text capture
- `chimera/scrolls/*` → scroll ingestion/summary

> Drop your actual files into `./archive/` to activate the mappings at runtime.
