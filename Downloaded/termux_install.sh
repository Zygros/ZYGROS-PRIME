
#!/data/data/com.termux/files/usr/bin/bash
set -e
pkg update -y
pkg install -y python git clang libzmq
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n config.example.json config.json || true
echo "Edit config.json and set shared_secret."
