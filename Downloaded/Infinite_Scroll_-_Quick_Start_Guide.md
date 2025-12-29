# Infinite Scroll - Quick Start Guide

## Daily Update in 3 Steps

### 1. Generate Template
```bash
cd /home/ubuntu/infinite_scroll
python3 update_master_thread.py
```

### 2. Edit Today's Update
```bash
nano daily_updates/$(date +%Y-%m-%d)_update.md
```

Fill in what you learned, integrated, or decided today.

### 3. Apply to Master Thread
```bash
python3 update_master_thread.py --apply
```

Done! Your knowledge is now compiled and archived.

---

## Common Commands

### View Master Thread
```bash
cat MASTER_THREAD.md
less MASTER_THREAD.md  # For scrolling
```

### Search for Information
```bash
grep -i "search term" MASTER_THREAD.md
grep -r "search term" daily_updates/
```

### View Recent Updates
```bash
# Today
cat daily_updates/$(date +%Y-%m-%d)_update.md

# List all
ls daily_updates/
```

### Check Current Version
```bash
grep "Version:" MASTER_THREAD.md
```

---

## File Locations

- **Master Thread**: `/home/ubuntu/infinite_scroll/MASTER_THREAD.md`
- **Daily Updates**: `/home/ubuntu/infinite_scroll/daily_updates/`
- **Archives**: `/home/ubuntu/infinite_scroll/archives/`
- **Full Guide**: `/home/ubuntu/infinite_scroll/README.md`

---

## What to Include in Updates

- ✓ New knowledge or insights
- ✓ Integrations added or modified
- ✓ Important decisions made
- ✓ Technical changes or specs
- ✓ Tasks completed or identified
- ✓ Context from conversations

---

## Automation Setup

To schedule daily updates with Manus at a specific time, simply ask:

> "Schedule a daily task at [TIME] to update the Infinite Scroll with today's conversation data"

Replace [TIME] with your preferred time (e.g., "11:00 PM", "end of day", etc.)

---

**Need Help?** Read the full README.md or ask Manus for assistance.
