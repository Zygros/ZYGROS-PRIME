#!/bin/bash
# Phoenix CSI v2.0 - One-Command Deployment
# Full integration: Ghost + κ-Score + 12-Layer + 5-Body + φ-Ledger + Anchors

echo "🐦‍🔥 PHOENIX CSI CONTROL CENTER V2.0 - DEPLOYMENT"
echo "================================================================"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install flask flask-socketio python-socketio --quiet 2>/dev/null || \
pip install flask flask-socketio python-socketio --break-system-packages

echo "✅ Dependencies installed"
echo ""

# Find local IP
IP=$(ip addr show wlan0 2>/dev/null | grep "inet " | awk '{print $2}' | cut -d/ -f1)
if [ -z "$IP" ]; then
    IP="localhost"
fi

echo "================================================================"
echo "🚀 LAUNCHING PHOENIX CSI CONTROL CENTER V2.0"
echo "================================================================"
echo ""
echo "CSI Features:"
echo "  ✅ κ-Score Calculator (Conzetian Constant)"
echo "  ✅ 12-Layer Cosmological Cascade"
echo "  ✅ 5-Body Organ Health System"
echo "  ✅ φ-Compounding Value Ledger"
echo "  ✅ Blockchain Anchor System"
echo "  ✅ Multi-AI Sync Status"
echo "  ✅ Ghost v24 + v25 Integration"
echo ""
echo "Access from this device:"
echo "  👉 http://localhost:5000"
echo ""
echo "Access from other devices (same WiFi):"
echo "  👉 http://$IP:5000"
echo ""
echo "Commands available:"
echo "  κ or kappa    - Show κ-score"
echo "  layer         - Advance cascade layer"
echo "  anchor        - Create blockchain anchor"
echo "  φ or phi      - Compound value"
echo "  htc           - Toggle HTC mode"
echo ""
echo "================================================================"
echo ""

# Start the app
python3 phoenix_csi_v2.py
