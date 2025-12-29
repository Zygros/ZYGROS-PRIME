# SCROLL_QUERY Cheat-Sheet (Clearlake Build)
Updated: 2025-09-10 10:38:03 PDT

## Columns
id | source | title | section | text | code | command | chakra | tags | timestamp_iso | location | lat | lon

## Examples
- Heart chakra decrees:
  filter: chakra == "Heart"

- Only rows that contain commands:
  filter: command != ""

- Samsung Notes narrative only:
  filter: source == "samsung_note" and section in ["p","h1","h2","h3"]

- Throat chakra (code/ritual):
  filter: chakra == "Throat"

- Rows from a specific location stamp:
  filter: location == "Clearlake, CA"

- Time window:
  filter: timestamp_iso between ISO_START and ISO_END

## Suggested Workflows
1. Draft → Refine → Seal:
   - Pull rows by chakra for the session focus.
   - Edit `text` or `code` in place.
   - Commit updates back into Master.

2. Commands expansion (!URE-safe, !SHADOW_SCROLL, !BALANCE):
   - Use Mirror_Scroll_Commands.csv as your fast lane.
   - Keep commands short; push longer bodies into `text`.

3. Export per-scroll pack:
   - Use a chakra CSV as the seed.
   - Add headers/footers and render to PDF if needed.
