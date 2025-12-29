#!/usr/bin/env python3
"""
Infinite Scroll - Master Thread Update Script
Automates the process of updating the master thread with new information
"""

import os
import json
from datetime import datetime
from pathlib import Path

class InfiniteScrollUpdater:
    def __init__(self, base_dir="/home/ubuntu/infinite_scroll"):
        self.base_dir = Path(base_dir)
        self.master_thread = self.base_dir / "MASTER_THREAD.md"
        self.daily_updates_dir = self.base_dir / "daily_updates"
        self.archives_dir = self.base_dir / "archives"
        self.knowledge_base_dir = self.base_dir / "knowledge_base"
        
    def get_current_date(self):
        """Get current date in YYYY-MM-DD format"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_current_version(self):
        """Extract current version from master thread"""
        if not self.master_thread.exists():
            return "0.0.0"
        
        with open(self.master_thread, 'r') as f:
            for line in f:
                if line.startswith("**Version**:"):
                    return line.split(":")[1].strip()
        return "0.0.0"
    
    def increment_version(self, current_version, update_type="patch"):
        """Increment version number based on update type"""
        major, minor, patch = map(int, current_version.split("."))
        
        if update_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif update_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def archive_current_version(self):
        """Create archive of current master thread"""
        if not self.master_thread.exists():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"MASTER_THREAD_{timestamp}.md"
        archive_path = self.archives_dir / archive_name
        
        with open(self.master_thread, 'r') as src:
            with open(archive_path, 'w') as dst:
                dst.write(src.read())
        
        print(f"✓ Archived current version to: {archive_name}")
    
    def create_daily_update_template(self, date):
        """Create template for daily update"""
        update_file = self.daily_updates_dir / f"{date}_update.md"
        
        if update_file.exists():
            print(f"⚠ Update file for {date} already exists")
            return update_file
        
        template = f"""# Daily Update: {date}

## Summary
[Brief description of what was added today]

## New Information Added

### Knowledge Extracted
- [New knowledge items]

### Integrations Documented
- [New or updated integrations]

### Key Insights & Decisions
- [Important decisions or insights]

### Technical Changes
- [Technical updates or modifications]

## Categories Updated
- [List sections modified in master thread]

## Next Steps
- [Upcoming tasks or priorities]

## Conversation Context
[Brief context of the conversations that generated this update]

---

**Update Type**: [Patch/Minor/Major]  
**Items Added**: [Number]  
**Sections Modified**: [List]  
**Version Change**: [Old] → [New]
"""
        
        with open(update_file, 'w') as f:
            f.write(template)
        
        print(f"✓ Created daily update template: {date}_update.md")
        return update_file
    
    def update_master_thread(self, update_content, update_type="patch"):
        """Update master thread with new information"""
        current_version = self.get_current_version()
        new_version = self.increment_version(current_version, update_type)
        current_date = self.get_current_date()
        
        # Archive current version before updating
        self.archive_current_version()
        
        # Read current master thread
        with open(self.master_thread, 'r') as f:
            content = f.read()
        
        # Update header metadata
        # Extract current date from content
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('**Last Updated**:'):
                lines[i] = f"**Last Updated**: {current_date}"
            if line.startswith('**Version**:'):
                lines[i] = f"**Version**: {new_version}"
        content = '\n'.join(lines)

        
        # Add to update log (insert before metadata section)
        update_log_entry = f"""
### {current_date} - Daily Update
{update_content}

"""
        
        # Find the update log section and insert new entry
        update_log_marker = "## Update Log\n\n"
        if update_log_marker in content:
            parts = content.split(update_log_marker)
            content = parts[0] + update_log_marker + update_log_entry + parts[1]
        
        # Write updated content
        with open(self.master_thread, 'w') as f:
            f.write(content)
        
        print(f"✓ Updated master thread: {current_version} → {new_version}")
        return new_version
    
    def extract_knowledge_to_base(self, category, content):
        """Extract and save categorized knowledge"""
        category_file = self.knowledge_base_dir / f"{category.lower().replace(' ', '_')}.json"
        
        # Load existing data
        if category_file.exists():
            with open(category_file, 'r') as f:
                data = json.load(f)
        else:
            data = {"category": category, "entries": []}
        
        # Add new entry
        entry = {
            "date": self.get_current_date(),
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        data["entries"].append(entry)
        
        # Save updated data
        with open(category_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Added entry to knowledge base: {category}")
    
    def run_interactive_update(self):
        """Run interactive update session"""
        print("=" * 60)
        print("INFINITE SCROLL - DAILY UPDATE")
        print("=" * 60)
        print()
        
        current_date = self.get_current_date()
        print(f"Date: {current_date}")
        print(f"Current Version: {self.get_current_version()}")
        print()
        
        # Create daily update template
        update_file = self.create_daily_update_template(current_date)
        
        print()
        print("Next steps:")
        print(f"1. Edit the daily update file: {update_file}")
        print("2. Fill in the new information from today's conversations")
        print("3. Run this script again with the --apply flag to update master thread")
        print()
        print(f"Command: python3 {__file__} --apply")
        
    def apply_daily_update(self):
        """Apply the daily update to master thread"""
        current_date = self.get_current_date()
        update_file = self.daily_updates_dir / f"{current_date}_update.md"
        
        if not update_file.exists():
            print(f"✗ No update file found for {current_date}")
            return
        
        with open(update_file, 'r') as f:
            update_content = f.read()
        
        # Extract summary for update log
        summary_lines = []
        in_summary = False
        for line in update_content.split('\n'):
            if line.startswith("## Summary"):
                in_summary = True
                continue
            elif line.startswith("##"):
                in_summary = False
            elif in_summary and line.strip():
                summary_lines.append(line.strip())
        
        summary = " ".join(summary_lines) if summary_lines else "Daily update applied"
        
        # Update master thread
        self.update_master_thread(summary, update_type="patch")
        
        print()
        print("✓ Daily update applied successfully!")
        print(f"✓ Master thread updated with content from {current_date}")

def main():
    import sys
    
    updater = InfiniteScrollUpdater()
    
    if "--apply" in sys.argv:
        updater.apply_daily_update()
    else:
        updater.run_interactive_update()

if __name__ == "__main__":
    main()
