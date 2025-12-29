\
# MAIA – Sovereign Core + Cognitive Bus (v1.3.0)

## Quickstart (Termux)
```bash
# Download files to ~/downloads or run from this zip
bash install_maia_termux.sh
maia status
maia shell
```

## CLI
- `maia shell`
- `maia process "Your query here"`
- `maia operator mode=core` / `mode=advanced`
- `maia operator dump=json` / `dump=csv`

## Files
- `maia.py` – main program
- `install_maia_termux.sh` – installer
- Logs in `~/maia/logs/maia_events_YYYYMMDD.jsonl`
- Dumps to `~/maia/maia_state_dump.json` & `~/maia/maia_beliefs.csv`
