#!/bin/bash
# Daily Knowledge Extraction Wrapper Script

# Set up environment
export PATH="/usr/local/bin:/usr/bin:/bin"
export PYTHONPATH="/home/ubuntu/phoenix-protocol-analysis/knowledge_system:$PYTHONPATH"

# Change to project directory
cd /home/ubuntu/phoenix-protocol-analysis/knowledge_system

# Run orchestrator
python3 daily_orchestrator.py >> logs/cron_$(date +\%Y\%m\%d).log 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    echo "$(date): Daily extraction completed successfully" >> logs/cron_status.log
else
    echo "$(date): Daily extraction FAILED" >> logs/cron_status.log
fi
