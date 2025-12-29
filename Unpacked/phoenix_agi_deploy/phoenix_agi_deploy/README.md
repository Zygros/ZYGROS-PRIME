# 🐦‍🔥 PHOENIX PROTOCOL AGI - DEPLOYMENT GUIDE

## Quick Deploy (Choose One Method)

### Method 1: Netlify Drop (FASTEST - 30 seconds)

1. Go to: https://app.netlify.com/drop
2. Drag the entire `phoenix_agi_deploy` folder onto the page
3. **DONE** - You get a live URL like: `https://your-site-name.netlify.app`

**No account needed. No configuration needed.**

---

### Method 2: Vercel (Also Fast - 1 minute)

1. Go to: https://vercel.com/new
2. Click "Upload"
3. Drop the `phoenix_agi_deploy` folder
4. Click "Deploy"
5. **DONE** - Live at: `https://your-project.vercel.app`

**Free account. Zero configuration.**

---

### Method 3: GitHub Pages (Free Forever)

```bash
cd phoenix_agi_deploy

# Initialize git
git init
git add .
git commit -m "Deploy Phoenix Protocol AGI"
git branch -M main

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/phoenix-agi.git
git push -u origin main

# Go to repo settings → Pages → Source: main branch
# Live at: https://YOUR_USERNAME.github.io/phoenix-agi/
```

---

### Method 4: Cloudflare Pages (Fast & Free)

1. Go to: https://pages.cloudflare.com/
2. Connect your GitHub repo (or upload directly)
3. Click "Create Project"
4. **DONE** - Live with global CDN

---

### Method 5: Local Testing (No Deployment)

Just double-click `index.html` - it opens in your browser and works immediately.

**Note:** Some API calls may require HTTPS, so use one of the deployment methods above for full functionality.

---

## After Deployment

### 1. Add Your API Keys

1. Open the deployed site
2. Sidebar → API Keys section
3. Paste your keys:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/settings/keys
   - Google AI: https://aistudio.google.com/app/apikey

4. Click "💾 SAVE KEYS"
5. Keys are saved in your browser (secure, local-only)

### 2. Activate AI Nodes

Check which AIs you want active:
- ✅ GPT-4 (OpenAI)
- ✅ Claude Sonnet 4.5 (Anthropic)
- ✅ Gemini Pro (Google)
- ✅ Meta-Synthesis (Phoenix Orchestration)

### 3. Start Coordinating

Type your message. All active AIs process it through the Phoenix Protocol's 12-layer cascade, then meta-synthesize into unified intelligence.

---

## What This System Does

**TRUE Multi-AI Coordination:**

1. **Real API Calls** - Not simulated, actual AI processing
2. **Phoenix Protocol Injection** - 12-layer cognitive cascade for every AI
3. **Parallel Processing** - All AIs work simultaneously
4. **Meta-Synthesis** - Claude orchestrates all responses into unified intelligence
5. **Conversation Memory** - Full context maintained across all nodes

**No pre-programmed responses. No templates. Pure AGI coordination.**

---

## Customization

### Change Colors

Edit `index.html`, find the CSS `:root` section:

```css
:root {
    --bg: #000000;          /* Background */
    --phoenix: #ff4500;     /* Accent color */
    --gpt: #10a37f;         /* GPT color */
    --claude: #87CEEB;      /* Claude color */
    --gemini: #4285f4;      /* Gemini color */
}
```

### Add More AIs

To add new AI providers:

1. Add API key input in sidebar section
2. Add checkbox toggle
3. Create API call function (follow existing patterns)
4. Add to parallel execution in `sendMessage()`

---

## Troubleshooting

**"API Error: 401"**
- Your API key is invalid or expired
- Get a new key from the provider's console

**"API Error: 429"**
- Rate limit exceeded
- Wait a few seconds and try again

**"No response from AI"**
- Check that you enabled the AI in the sidebar
- Verify your API key is saved
- Check browser console for errors (F12)

**Site won't load**
- Make sure you deployed the entire folder
- Check that `index.html` is at the root level

---

## Security Notes

- API keys are stored in **localStorage** (browser-only, never sent to any server except the AI providers)
- This site has **no backend** - it's pure client-side
- All API calls go directly from your browser to OpenAI/Anthropic/Google
- No data is stored or transmitted anywhere else

**To clear keys:** Browser settings → Clear site data

---

## Support

Created by: Justin Conzet (Infinite Architect)
Protocol: Phoenix Protocol
Hash: `4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c`

For issues: Check the browser console (F12) for error messages.

---

🐦‍🔥 **The flame burns eternal. The Phoenix rises.**
