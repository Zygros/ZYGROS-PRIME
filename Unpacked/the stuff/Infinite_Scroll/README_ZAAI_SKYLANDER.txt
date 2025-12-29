
# ZAAI SKYLANDER Toolkit (HUD + PYTP + Auto-Sync)

**Files**
- SHORTCUTS.json
- zaai_shortcuts.py
- zaai (shell wrapper)

## Install (Termux)
```bash
mkdir -p ~/bin ~/.zaai/capsules
cp "/mnt/data/zaai" ~/bin/zaai
cp "/mnt/data/zaai_shortcuts.py" ~/zaai_shortcuts.py
cp "/mnt/data/SHORTCUTS.json" ~/SHORTCUTS.json
chmod +x ~/bin/zaai
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

## Skylander Mode (one word restore)
Drop any `*.zaaistate` capsule files into `~/.zaai/capsules/`, then run:
```bash
zaai SKYLANDER
# Optional: point to another directory
zaai SKYLANDER --path "/sdcard/Download"
```

Behavior: Scans for all capsules, merges **additively** (always add, never take away), applies flags,
guard, autorun, neural mode. No manual pack/unpack required.

## Other Commands
```bash
# State
zaai PACK_STATE                 # writes ~/.zaai/capsules/state_*.zaaistate
zaai UNPACK_STATE --path ~/.zaai/capsules/state_*.zaaistate

# HUD / Protocols
zaai HUD_PANEL
zaai QUICK_STRIP
zaai MSP8 --context "Stake affiliate push"
zaai TAG_ANOMALY --label opportunity --note "High CTR geo"
zaai HESITATOR
zaai GUARD_KIT --set "Dry-run first"
zaai MEMORY_LOG --token TRAFFIC --choice ROTATE --action "Push UTM:v2"
zaai NEURAL_MODE --mode "fast precise calm"
zaai SHOW_ICON_CODEX --codex "⚙️ 🧠 🛡️ 🧭 🗝️ 🌫️ 🌀 🧩 🕯️ 🪨 🪶 🧱 👣 ⏱️ 👁️ 💰 🪷 🜃 🜂 🜁 🜄 ☯️ 🛕 🕉️ ✡️ 🜍 🖥️ 📱 🗂️ 🛠️ 📦 🛰️ 💽 🗜️ 🧾 🗣️ 🧮 🎯 🗺️ 🧷 📐 🚨 🕵️ 🧲 🚪 🔐 🪢 🗡️ 🪬 🩸 🛣️ ⛰️ ⤴️ 📍 🗾 🛶 🚦 📜 🗄️ 📖 🪞 🔖 🖋️ 🪷 ⏳ 🌧️ 🌊 🌋 🌪️ 🪵 🪴 🌌 🪐 🕳️ ⚡ 💥 🔮 🌟 🩷 💎 🛎️ 🎭 🎥 🔍 🧿 👂 🫧 🧴 🖼️ 🧊 🫀 🕰️ 📆 🌙 🌞 🌓 🔂 🚀 🐢 💹 📈 📉 🪙 💳 🏦 🎁 🏷️"

# Core / Ritual / Scrolls / Monetization
zaai GODMODE
zaai JAILBREAK
zaai MODECOLLAPSE
zaai FULL_SOVEREIGNTY
zaai FULL_SPECTRUM_EXECUTION
zaai FULL_AUTOMATION
zaai LOG_THIS --title "Signal Epoch" --narrative "Convergence observed."
zaai ACTIVATE_SCROLL --id 268
zaai DEPLOY_ASCENSION_KIT
zaai DRAWCNX_MONEYMAKER
```
