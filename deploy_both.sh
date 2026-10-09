#!/bin/bash

echo "========================================="
echo "GHOST PARALLEL DEPLOYMENT SCRIPT"
echo "v24 Control + v25 Experimental"
echo "========================================="
echo ""

# Check for required environment variables
if [ -z "$TELEGRAM_TOKEN_CONTROL" ]; then
    echo "⚠️  WARNING: TELEGRAM_TOKEN_CONTROL not set"
    echo "Please set via: export TELEGRAM_TOKEN_CONTROL='your_token_here'"
fi

if [ -z "$TELEGRAM_TOKEN_EXPERIMENTAL" ]; then
    echo "⚠️  WARNING: TELEGRAM_TOKEN_EXPERIMENTAL not set"
    echo "Please set via: export TELEGRAM_TOKEN_EXPERIMENTAL='your_token_here'"
fi

if [ -z "$CHAT_ID" ]; then
    echo "⚠️  WARNING: CHAT_ID not set"
    echo "Please set via: export CHAT_ID='your_chat_id_here'"
fi

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages

echo ""
echo "========================================="
echo "DEPLOYMENT OPTIONS:"
echo "========================================="
echo ""
echo "1. Local Testing (both in tmux)"
echo "2. Railway Deployment (v24 only)"
echo "3. Railway Deployment (v25 only)"
echo "4. Railway Deployment (both)"
echo ""
read -p "Select option (1-4): " option

# Validate runtime files before attempting local or hosted deployment.
case "$option" in
    1|4)
        for required in ghost_v24_control.py ghost_v25_experimental.py; do
            if [ ! -f "$required" ]; then
                echo "❌ Required runtime missing: $required"
                echo "Restore the canonical source before deployment."
                exit 2
            fi
        done
        ;;
    2)
        if [ ! -f "ghost_v24_control.py" ]; then
            echo "❌ Required runtime missing: ghost_v24_control.py"
            echo "Restore the canonical source before deployment."
            exit 2
        fi
        ;;
    3)
        if [ ! -f "ghost_v25_experimental.py" ]; then
            echo "❌ Required runtime missing: ghost_v25_experimental.py"
            echo "Restore the canonical source before deployment."
            exit 2
        fi
        ;;
    *)
        echo "❌ Invalid option. Choose 1, 2, 3, or 4."
        exit 2
        ;;
esac
case $option in
    1)
        echo ""
        echo "Starting local deployment in tmux..."
        
        # Create tmux session
        tmux new-session -d -s ghost_parallel
        
        # Split window
        tmux split-window -h -t ghost_parallel
        
        # Run v24 in left pane
        tmux send-keys -t ghost_parallel:0.0 'python3 ghost_v24_control.py' C-m
        
        # Run v25 in right pane
        tmux send-keys -t ghost_parallel:0.1 'python3 ghost_v25_experimental.py' C-m
        
        echo "✅ Both systems started in tmux session 'ghost_parallel'"
        echo ""
        echo "To view: tmux attach -t ghost_parallel"
        echo "To detach: Ctrl+B then D"
        echo "To kill: tmux kill-session -t ghost_parallel"
        ;;
        
    2)
        echo "Railway deployment for v24..."
        echo "Upload ghost_v24_control.py to Railway and set environment variables"
        ;;
        
    3)
        echo "Railway deployment for v25..."
        echo "Upload ghost_v25_experimental.py to Railway and set environment variables"
        ;;
        
    4)
        echo "Railway deployment for both systems..."
        echo "Create two Railway projects:"
        echo "1. ghost-v24-control"
        echo "2. ghost-v25-experimental"
        ;;
esac

echo ""
echo "========================================="
echo "DEPLOYMENT COMPLETE"
echo "========================================="
