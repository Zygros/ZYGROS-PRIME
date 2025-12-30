#!/bin/bash

# Infinite Scroll Automated Update Script
# Updates the master thread with today's Phoenix Protocol work

set -e

PROJECT_DIR="/home/ubuntu/phoenix-protocol-analysis"
SCROLL_DIR="$PROJECT_DIR/client/public/infinite_scroll"
DATE=$(date +%Y-%m-%d)
UPDATE_FILE="$SCROLL_DIR/daily_updates/${DATE}_update.md"

echo "🔥 Infinite Scroll Automated Update 🔥"
echo "Date: $DATE"
echo ""

# Check if update already exists
if [ -f "$UPDATE_FILE" ]; then
    echo "✓ Update for today already exists: $UPDATE_FILE"
    echo "  Skipping creation..."
else
    echo "Creating new update file..."
    
    # Create update template
    cat > "$UPDATE_FILE" << EOF
# Daily Update: $DATE

## Summary
[Auto-generated update - please fill in summary]

## New Information Added

### Features Implemented
- [List new features]

### Technical Changes
- [List technical changes]

### Knowledge Extracted
- [List new knowledge]

## Categories Updated
- [List updated categories]

## Next Steps
- [List next steps]

## Conversation Context
[Describe conversation context]

---

**Update Type**: Daily Update  
**Items Added**: [Count]  
**Sections Modified**: [List]  
**Version Change**: [Previous] → [Current]
EOF

    echo "✓ Created update template: $UPDATE_FILE"
fi

# Update master thread metadata
echo ""
echo "Updating master thread metadata..."

MASTER_THREAD="$SCROLL_DIR/MASTER_THREAD.md"

# Update last modified date
sed -i "s/\*\*Last Updated\*\*:.*/\*\*Last Updated\*\*: $DATE/" "$MASTER_THREAD"

echo "✓ Updated master thread last modified date"

# Count statistics
TOTAL_LINES=$(wc -l < "$MASTER_THREAD")
TOTAL_UPDATES=$(ls -1 "$SCROLL_DIR/daily_updates/" | wc -l)
COMPLETED_TASKS=$(grep -c "\[x\]" "$MASTER_THREAD" || echo "0")

echo ""
echo "📊 Infinite Scroll Statistics:"
echo "  Total Lines: $TOTAL_LINES"
echo "  Daily Updates: $TOTAL_UPDATES"
echo "  Completed Tasks: $COMPLETED_TASKS"
echo ""
echo "✅ Infinite Scroll update complete!"
