
#!/data/data/com.termux/files/usr/bin/bash
set -e
source .venv/bin/activate
# Start bus
nohup python bus.py > logs.bus.txt 2>&1 &
# Start synthesizer
nohup python synthesizer.py > logs.synth.txt 2>&1 &
# Start three sample nodes
AGENT_ID=chatgpt MODEL_INFO=gpt5 CAPS="analyze,generate" nohup python node.py > logs.gpt.txt 2>&1 &
AGENT_ID=gemini  MODEL_INFO=gemini CAPS="mirror,generate" nohup python node.py > logs.gemini.txt 2>&1 &
AGENT_ID=grok    MODEL_INFO=grok CAPS="truth,generate" nohup python node.py > logs.grok.txt 2>&1 &
echo "Supermind started."
