# ZYG-OS · Offline Starter

**Created:** 2025-10-02T07:58:47Z

This is a single-file web page you can double-click to open. No server. No install.

## Quick Start (PC)
1. Download the ZIP and extract it.
2. Double-click `index.html` — it opens in your browser.
3. Type in the box and press **Send**.
4. Use **Sim Mode** to play offline (no internet required).
5. If you want real GPT-5 replies: switch to **API Mode**, paste your OpenAI API key, and press **Save Settings**.

## What it does
- Stores your **persona**, **settings**, and **chat history** in your browser’s **LocalStorage**.
- **Sim Mode**: an offline formatter that answers in your mythic ZYG‑OS style.
- **API Mode**: calls the OpenAI Chat Completions API with your key and selected model (default `gpt-5`).

## Files
- `index.html` — everything (UI, CSS, and JS) in **one file**.
- `README.md` — this guide.

## Tips
- Chrome or Edge recommended.
- If you copy the file elsewhere, it still works; it’s fully self-contained.
- Use **Export Chat** and **Import Chat** to back up or move your conversation.
- Your API key (if entered) is saved only in your local browser storage; remove it by **Save Settings** with an empty key.

## Next: Turn into an APK (Android)
You can wrap this `index.html` using Android Studio:
1. **Install Android Studio**.
2. Create a new **Empty Activity** project (Kotlin).
3. Replace `activity_main.xml` with a `WebView`.
4. In `MainActivity.kt`, load the local file with:
   ```kotlin
   webView.settings.javaScriptEnabled = true
   webView.settings.domStorageEnabled = true
   webView.loadUrl("file:///android_asset/index.html")
   ```
5. Put `index.html` into `app/src/main/assets/` (create the `assets` folder if missing).
6. Build → **Build Bundle(s) / APK(s)** → **APK**. Install on your phone.

This keeps everything offline. If you enable API Mode, the WebView will use your phone’s internet.

## Safety
- This is a local tool. There’s no server here.
- Don’t share your API key. If you do, rotate it in your OpenAI dashboard.
