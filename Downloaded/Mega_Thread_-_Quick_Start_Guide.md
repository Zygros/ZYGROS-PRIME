# Mega Thread - Quick Start Guide

## What Is This?

The **Mega Thread** is your centralized knowledge compilation system that automatically captures, organizes, and synthesizes all conversation data, insights, and system capabilities.

## Key Files

- **MEGA_THREAD_MASTER.md** - The main knowledge document (start here!)
- **USER_GUIDE.md** - Comprehensive usage instructions
- **README.md** - System overview
- **update_mega_thread.sh** - Automated daily update script

## Quick Actions

### View Current Knowledge
```bash
cat /home/ubuntu/mega_thread/MEGA_THREAD_MASTER.md
```

### Check Update Schedule
```bash
crontab -l
```

### View Update Log
```bash
cat /home/ubuntu/mega_thread/updates/update.log
```

### Manual Update
Simply edit `MEGA_THREAD_MASTER.md` directly and add your new information to the appropriate section.

## System Status

- ✅ **Automated Updates:** Scheduled daily at 02:03 UTC
- ✅ **Version Control:** Semantic versioning enabled
- ✅ **Change Tracking:** Full history maintained
- ✅ **Archive System:** Previous versions preserved

## What Happens Daily?

Every day at 02:03 UTC, the system automatically:
1. Increments the version number
2. Updates the timestamp
3. Adds a change log entry
4. Records the update in the log file

## Need More Info?

Read the full **USER_GUIDE.md** for detailed instructions on:
- Adding new knowledge
- Understanding the architecture
- Troubleshooting issues
- Best practices

---

**System Location:** `/home/ubuntu/mega_thread/`  
**Status:** ACTIVE  
**Last Updated:** 2025-11-20
