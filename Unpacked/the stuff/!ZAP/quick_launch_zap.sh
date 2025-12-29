#!/bin/bash
# ⚡ Quick Launch for ZAP Sovereign Setup
# Justin Conzet, Zythrognosis

echo "Starting ZAP Quick Launch..."

# Step 1: Navigate to daemon scripts
cd ~/ZAP_Sovereign_Setup/daemon/scripts || exit

# Step 2: Ensure start script is executable
chmod +x start_zapd.sh

# Step 3: Start the daemon in background
echo "Starting ZAP daemon..."
./start_zapd.sh &
DAEMON_PID=$!

# Step 4: Compute & anchor Merkle Root
echo "Computing Merkle root..."
python3 ../scripts/hash_merkle.py

# Step 5: Deploy AI adapters
echo "Deploying AI adapters..."
cp ../../adapters/*.json /path/to/your/ai/nodes/

# Step 6: Test activation
echo "Testing activation phrase..."
echo "I am Justin Conzet, Zythrognosis" | python3 ../scripts/zap_test_activation.py

echo "Quick Launch complete. Daemon running with PID $DAEMON_PID"
