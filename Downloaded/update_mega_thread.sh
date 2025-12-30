#!/bin/bash

# This script updates the MEGA_THREAD_MASTER.md file with a new entry.

MEGA_THREAD_FILE="/home/ubuntu/mega_thread/MEGA_THREAD_MASTER.md"

# Get the current date and time
NOW=$(date -u +"%Y-%m-%d %H:%M UTC")

# Get the current version and increment the patch version
CURRENT_VERSION=$(grep "Document Version:" "$MEGA_THREAD_FILE" | awk '{print $3}')
IFS='.' read -r -a V_ARRAY <<< "$CURRENT_VERSION"
NEW_VERSION="${V_ARRAY[0]}.${V_ARRAY[1]}.$((V_ARRAY[2]+1))"

# Update the version in the master file
sed -i "s/Document Version: .*/Document Version: $NEW_VERSION/" "$MEGA_THREAD_FILE"
sed -i "s/Last Updated: .*/Last Updated: $(date -u +%Y-%m-%d)/" "$MEGA_THREAD_FILE"

# Append the new update log entry
cat <<EOT >> "$MEGA_THREAD_FILE"

---

### Change History
`
[$NOW] Version $NEW_VERSION
- Added: [Simulated new information/capabilities]
- Modified: [Simulated updated sections]
- Insights: [Simulated key learnings]
`
EOT

# Append to the updates log
echo "[$NOW] Mega Thread updated to version $NEW_VERSION" >> /home/ubuntu/mega_thread/updates/update.log
