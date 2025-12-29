#!/usr/bin/env python3
"""
Infinite Scroll Daily Update Script

This script facilitates the daily update process for the Infinite Scroll system.
It creates a new daily log file and provides a template for capturing the day's information.

Usage:
    python3 update_scroll.py [--date YYYY-MM-DD]
    
If no date is provided, uses the current date.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
SCROLL_DIR = Path("/home/ubuntu/infinite_scroll")
DAILY_LOGS_DIR = SCROLL_DIR / "daily_logs"

def get_date():
    """Get the date for the log file."""
    if len(sys.argv) > 2 and sys.argv[1] == "--date":
        return sys.argv[2]
    return datetime.now().strftime("%Y-%m-%d")

def create_daily_log(date_str):
    """Create a new daily log file with template structure."""
    log_file = DAILY_LOGS_DIR / f"{date_str}.md"
    
    if log_file.exists():
        print(f"Daily log for {date_str} already exists.")
        print(f"Opening: {log_file}")
        return log_file
    
    template = f"""# Daily Log: {date_str}

## Key Events

- [Add key events, tasks completed, or significant milestones here]

## New Information & Insights

- [Document novel data, discoveries, or conceptual breakthroughs here]

## System Changes

- [Record modifications to protocols, architecture, or operational procedures here]

## Protocols Updated

- [List any protocols added or modified in /core_protocols]

## Integrations Added

- [Document any new integrations in /integrations]

## Architecture Changes

- [Note any new or updated system architecture documents]

## Insights Captured

- [Reference any new insight files created in /insights]

## Notes

[Add any additional context or observations here]
"""
    
    log_file.write_text(template)
    print(f"Created new daily log: {log_file}")
    return log_file

def list_recent_logs(days=7):
    """List the most recent log files."""
    log_files = sorted(DAILY_LOGS_DIR.glob("*.md"), reverse=True)
    log_files = [f for f in log_files if f.name != "daily_log_template.md"]
    
    print(f"\nRecent logs (last {days} days):")
    for log_file in log_files[:days]:
        print(f"  - {log_file.name}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("INFINITE SCROLL - Daily Update System")
    print("=" * 60)
    
    # Ensure directories exist
    DAILY_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get date and create log
    date_str = get_date()
    log_file = create_daily_log(date_str)
    
    # Show recent logs
    list_recent_logs()
    
    print("\n" + "=" * 60)
    print("Update complete. Remember to:")
    print("1. Fill in the daily log with today's information")
    print("2. Update relevant directories (protocols, integrations, etc.)")
    print("3. Follow the principle of accumulation - add, never remove")
    print("=" * 60)

if __name__ == "__main__":
    main()
