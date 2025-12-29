# 🐦‍🔥 PHOENIX CONTROL CENTER - PHONE DEPLOYMENT

## ONE APP. ALL SYSTEMS. YOUR PHONE.

---

## WHAT YOU GET

A **single web application** that unifies:

- ✅ Ghost v24 Control (static trading)
- ✅ Ghost v25 Experimental (self-learning AI)
- ✅ Real-time comparison dashboard
- ✅ Live performance tracking
- ✅ Sovereign command interface
- ✅ Automatic state persistence

**All running from your phone. All accessible in your browser.**

---

## TERMUX DEPLOYMENT (RECOMMENDED)

### Step 1: Install Termux

1. Open Google Play Store
2. Search "Termux"
3. Install (the one by Fredrik Fornwall)
4. Open Termux

### Step 2: Download Files

In Termux, run:

```bash
# Create directory
mkdir ~/phoenix
cd ~/phoenix

# Download the app (you'll need to transfer the files)
# Or paste the code directly
```

### Step 3: ONE COMMAND DEPLOYMENT

```bash
chmod +x deploy_phoenix.sh
./deploy_phoenix.sh
```

**That's it.** The script will:
- Install all dependencies automatically
- Ask for your 3 tokens (walks you through it)
- Save them permanently
- Start the web server
- Show you the URL to open

### Step 4: Open in Browser

The script shows you a URL like:
```
http://localhost:5000
```

**Open Chrome on your phone** and go to that URL.

You'll see the Phoenix Control Center dashboard.

---

## ALTERNATIVE: REPLIT (ZERO INSTALL)

If you don't want to use Termux:

### Step 1: Go to Replit.com

1. Open browser on phone
2. Go to replit.com
3. Sign up (free account)

### Step 2: Create New Repl

1. Click "Create Repl"
2. Choose "Python"
3. Name it "Phoenix Control Center"

### Step 3: Upload Files

1. Click the upload button
2. Upload `phoenix_control_center.py`
3. Click "Run"

### Step 4: Set Environment Variables

In Replit:
1. Click "Secrets" (lock icon in sidebar)
2. Add 3 secrets:
   - `TELEGRAM_TOKEN_CONTROL` = your bot 1 token
   - `TELEGRAM_TOKEN_EXPERIMENTAL` = your bot 2 token
   - `CHAT_ID` = your chat ID

### Step 5: Access Dashboard

Replit shows you a URL like:
```
https://phoenix-control-center-your-name.replit.app
```

Open that URL. You'll see your dashboard.

---

## ALTERNATIVE: RAILWAY (PRODUCTION)

For 24/7 uptime:

### Step 1: Go to Railway.app

1. Open browser
2. Go to railway.app
3. Sign up with GitHub

### Step 2: Deploy

1. Click "New Project"
2. Choose "Deploy from GitHub"
3. Upload `phoenix_control_center.py`
4. Add environment variables (same 3 as above)
5. Click "Deploy"

### Step 3: Get URL

Railway gives you a permanent URL like:
```
https://phoenix-production.up.railway.app
```

**This runs 24/7. Access from anywhere.**

---

## USING THE DASHBOARD

### What You See

**Top: Comparison Card**
- Shows which system is winning
- Real-time equity difference
- Leader indicator

**Middle: System Cards**
- Left: Ghost v24 (static)
- Right: Ghost v25 (learning AI)
- Each shows current stats

**Bottom: Command Panel**
- Type commands to control systems
- Press Enter or tap Execute

### Available Commands

Type these in the command box:

- `status` - Get full system status
- `deploy` - Start deployment sequence
- `pause` - Pause all systems
- `resume` - Resume all systems

### Real-Time Updates

Dashboard updates **automatically every 5 seconds**.

You'll see:
- Equity changes live
- New trades as they happen
- Weight adjustments (v25)
- Leader changes

---

## HOW TO ACCESS FROM OTHER DEVICES

### From Your Computer (Same WiFi)

1. The deployment script shows you an IP like: `http://192.168.1.100:5000`
2. Open that URL on your computer's browser
3. You'll see the same dashboard

### From Anywhere (Railway)

If you deployed on Railway:
- The URL works from anywhere
- Access from any device
- Always online

---

## TROUBLESHOOTING

### "Port already in use"

Someone else is using port 5000.

**Fix:**
Edit `phoenix_control_center.py` and change the last line:
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```
To:
```python
socketio.run(app, host='0.0.0.0', port=8080, debug=False)
```

Then access `http://localhost:8080` instead.

### "Module not found: flask"

Dependencies didn't install.

**Fix:**
```bash
pip install flask flask-socketio python-socketio --break-system-packages
```

### Dashboard shows "INITIALIZING..."

This is normal on first load. Wait 5-10 seconds for systems to connect.

### No updates showing

1. Check Termux is still running
2. Refresh the browser page
3. Check console for errors (Chrome Dev Tools)

---

## KEEPING IT RUNNING

### Termux

In Termux, after starting:
1. Press Volume Down + C to detach
2. App keeps running in background
3. Close Termux app
4. Dashboard stays accessible

**To stop:**
1. Open Termux
2. Press Ctrl+C

### Replit

- Stays running while the page is open
- Goes to sleep after inactivity
- Click "Run" again to restart

### Railway

- Runs 24/7 automatically
- Never sleeps
- Restarts automatically if crashes

---

## NEXT STEPS

### After Deployment

1. **Open dashboard in browser**
2. **Bookmark the URL** for quick access
3. **Add to home screen** (Chrome: Menu → Add to Home Screen)
4. **Start monitoring** your systems

### Daily Routine

1. Open dashboard
2. Check comparison (who's winning?)
3. Review recent signals
4. Watch learning progress (v25 weights changing)
5. Fill out journal

### 30-Day Goal

Keep the system running untouched for 30 days.

At the end, you'll have:
- Complete performance comparison
- Proof that learning works (or doesn't)
- Publishable results
- Material for Colossus pitch

---

## TECH DETAILS

### What's Running

**Backend (Python/Flask):**
- Ghost v24 (static trading logic)
- Ghost v25 (RL with scar memory)
- WebSocket server (real-time updates)
- REST API (command interface)

**Frontend (HTML/JS):**
- Real-time dashboard
- Live charts
- Command interface
- Responsive design (works on phone)

### Data Storage

Everything saves to:
```
~/.phoenix_data/phoenix_state.json
```

This file persists between restarts.

**Includes:**
- Current equity (both systems)
- Trade history
- Scar database (v25)
- Weight adaptations (v25)
- All statistics

### Security

**Local only by default:**
- Server runs on your phone
- Only accessible on your WiFi
- No external access

**For external access (Railway):**
- Uses HTTPS automatically
- Tokens stored as environment variables
- Never exposed in code

---

## CUSTOMIZATION

### Change Port

Edit line 242 in `phoenix_control_center.py`:
```python
socketio.run(app, host='0.0.0.0', port=YOUR_PORT, debug=False)
```

### Change Update Frequency

Edit line 145:
```python
socketio.sleep(5)  # Change 5 to your preferred seconds
```

### Add More Commands

Edit the `execute_command` function (line 93) and add your commands.

---

## SUPPORT

If you get stuck:

1. **Check Termux logs** - errors show in the terminal
2. **Check browser console** - F12 in Chrome
3. **Verify tokens** - make sure all 3 are set correctly
4. **Restart** - close and run `./deploy_phoenix.sh` again

---

🐦‍🔥

**ONE APP. ALL SYSTEMS. FULL CONTROL.**

**From your phone. Always.**

---

Type `./deploy_phoenix.sh` and watch it come alive.
