#!/bin/bash

# Setup Daily Knowledge Management Automation
# Configures cron job to run the orchestrator daily at 11 PM

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ORCHESTRATOR_PATH="$PROJECT_DIR/knowledge_system/daily_orchestrator.py"
LOG_DIR="$PROJECT_DIR/knowledge_system/logs"

echo "🔥 Phoenix Protocol - Daily Knowledge Management Automation Setup 🔥"
echo ""
echo "Project Directory: $PROJECT_DIR"
echo "Orchestrator Script: $ORCHESTRATOR_PATH"
echo "Log Directory: $LOG_DIR"
echo ""

# Verify orchestrator exists
if [ ! -f "$ORCHESTRATOR_PATH" ]; then
    echo "❌ Error: Orchestrator script not found at $ORCHESTRATOR_PATH"
    exit 1
fi

# Make orchestrator executable
chmod +x "$ORCHESTRATOR_PATH"
echo "✓ Made orchestrator executable"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"
echo "✓ Ensured log directory exists"

# Create wrapper script for cron
WRAPPER_SCRIPT="$PROJECT_DIR/scripts/run_daily_extraction.sh"
cat > "$WRAPPER_SCRIPT" << 'EOF'
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
EOF

chmod +x "$WRAPPER_SCRIPT"
echo "✓ Created wrapper script: $WRAPPER_SCRIPT"

# Create crontab entry
CRON_ENTRY="0 23 * * * $WRAPPER_SCRIPT"

# Check if crontab entry already exists
if crontab -l 2>/dev/null | grep -q "$WRAPPER_SCRIPT"; then
    echo "⚠️  Cron job already exists"
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✓ Added cron job: Daily at 11:00 PM"
fi

echo ""
echo "📊 Current Crontab:"
crontab -l | grep -E "(phoenix|knowledge|extraction)" || echo "  (No matching entries found)"

echo ""
echo "✅ Automation setup complete!"
echo ""
echo "📝 Manual Commands:"
echo "  Run now:      cd $PROJECT_DIR/knowledge_system && python3 daily_orchestrator.py"
echo "  View logs:    tail -f $LOG_DIR/orchestrator_*.log"
echo "  View cron:    crontab -l"
echo "  Remove cron:  crontab -e  (then delete the line)"
echo ""
echo "🔔 The system will automatically run daily at 11:00 PM"
