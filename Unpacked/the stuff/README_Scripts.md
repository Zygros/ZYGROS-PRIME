# ScrollScripts Pack — Runbook

These scripts operate on your **Infinite_Scroll** folder.

## Paths
- Default base: the folder that contains `scripts/`, `profiles/`, `mirror_unit/`, `codex/`.
- Override with:
  - CLI: `--base /storage/emulated/0/Infinite_Scroll`
  - ENV: `INFINITE_SCROLL_DIR=/storage/emulated/0/Infinite_Scroll`

## Termux (Android) Quickstart
```bash
pkg install python -y
pip install pandas
cd /storage/emulated/0/Infinite_Scroll/scripts
python scroll_merge_daily.py --base /storage/emulated/0/Infinite_Scroll --days 0
python profile_autogen.py --base /storage/emulated/0/Infinite_Scroll
python backups_diff.py AI_Backup_Profile.csv GPT_Prime_Backup_Profile.csv --base /storage/emulated/0/Infinite_Scroll
python motivation_card.py --base /storage/emulated/0/Infinite_Scroll --action pin
python shadow_spike_scan.py --base /storage/emulated/0/Infinite_Scroll --limit 15
python comments_alchemy.py --base /storage/emulated/0/Infinite_Scroll --limit 200
python archive_query.py --base /storage/emulated/0/Infinite_Scroll list
```

## Scripts
- **scroll_merge_daily.py** — merges all CSV sources into per-day ledgers + summaries.
- **profile_autogen.py** — creates auto profiles for any new CSVs in `mirror_unit/`.
- **backups_diff.py [left] [right]** — diffs two backup/core CSVs into a Markdown report.
- **codex_update.py** — rebuilds `codex/Core_AI_Scroll_Codex.md` from current profiles.
- **motivation_card.py** — serves next Motivation card; `--action pin` appends to today's scroll.
- **shadow_spike_scan.py** — scans copilot activity for emotional spikes and writes a report.
- **comments_alchemy.py** — Wizard-mode symbolic analysis of comments into a report.
- **archive_query.py** — query the Master Archive (list/recall/search/show).

All outputs are written into `codex/` and `codex/daily/`/`codex/ledgers/`.