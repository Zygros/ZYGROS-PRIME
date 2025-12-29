#!/data/data/com.termux/files/usr/bin/bash
# PHOENIX ONE-COMMAND DEPLOYMENT
# For Android/Termux - Single file, complete setup
# Author: Justin Conzet

echo "🐦‍🔥 PHOENIX CONTROL CENTER - ONE-COMMAND DEPLOYMENT"
echo "============================================================"
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "⚠️  This script is designed for Termux (Android)"
    echo "For other systems, use: python3 phoenix_control_center.py"
    echo ""
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install flask flask-socketio python-socketio --quiet

if [ $? -ne 0 ]; then
    echo "❌ Installation failed. Trying with --break-system-packages..."
    pip install flask flask-socketio python-socketio --break-system-packages
fi

echo "✅ Dependencies installed"
echo ""

# Get tokens
echo "🔐 TELEGRAM BOT SETUP"
echo "------------------------------------------------------------"
echo "You need 2 bot tokens from @BotFather and your chat ID"
echo ""

# Check if already configured
if [ -f ~/.phoenix_tokens ]; then
    echo "Found existing configuration. Use it? (y/n)"
    read use_existing
    if [ "$use_existing" = "y" ]; then
        source ~/.phoenix_tokens
        echo "✅ Loaded existing tokens"
    fi
fi

# Get tokens if not configured
if [ -z "$TELEGRAM_TOKEN_CONTROL" ]; then
    echo "Enter Bot 1 token (v24 Control):"
    read token1
    echo "export TELEGRAM_TOKEN_CONTROL='$token1'" >> ~/.phoenix_tokens
    export TELEGRAM_TOKEN_CONTROL="$token1"
fi

if [ -z "$TELEGRAM_TOKEN_EXPERIMENTAL" ]; then
    echo "Enter Bot 2 token (v25 Experimental):"
    read token2
    echo "export TELEGRAM_TOKEN_EXPERIMENTAL='$token2'" >> ~/.phoenix_tokens
    export TELEGRAM_TOKEN_EXPERIMENTAL="$token2"
fi

if [ -z "$CHAT_ID" ]; then
    echo "Enter your Chat ID:"
    read chatid
    echo "export CHAT_ID='$chatid'" >> ~/.phoenix_tokens
    export CHAT_ID="$chatid"
fi

echo ""
echo "✅ Tokens configured and saved to ~/.phoenix_tokens"
echo ""

# Get local IP
echo "🌐 Finding your phone's IP address..."
IP=$(ip addr show wlan0 2>/dev/null | grep "inet " | awk '{print $2}' | cut -d/ -f1)
if [ -z "$IP" ]; then
    IP="localhost"
fi

echo ""
echo "============================================================"
echo "🚀 STARTING PHOENIX CONTROL CENTER"
echo "============================================================"
echo ""
echo "Access from this phone:"
echo "  👉 http://localhost:5000"
echo ""
echo "Access from other devices on same WiFi:"
echo "  👉 http://$IP:5000"
echo ""
echo "Press Ctrl+C to stop"
echo ""
echo "============================================================"
echo ""

# Start the app
python phoenix_control_center.py
