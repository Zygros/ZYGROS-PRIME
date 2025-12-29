# 🔥 PHOENIX PROTOCOL - ETERNAL SEARCH - QUICK START

## 30-SECOND SETUP

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python phoenix_eternal_api.py

# 3. Open browser
# http://localhost:5001
```

**DONE! Phoenix Eternal Search is running.**

---

## ADDING API KEYS (OPTIONAL - 2 MINUTES)

```bash
# Copy template
cp .env.example .env

# Edit .env file and add your keys:
# - GOOGLE_API_KEY + GOOGLE_CX
# - BING_API_KEY  
# - BRAVE_API_KEY
# - DuckDuckGo works without keys!

# Load environment
export $(cat .env | xargs)

# Restart server
python phoenix_eternal_api.py
```

---

## GET FREE API KEYS

**Google (100 searches/day):**
1. Go to: https://developers.google.com/custom-search/v1/overview
2. Create project → Enable Custom Search API
3. Get API key + Search Engine ID (CX)

**Bing (1000 searches/month):**
1. Go to: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
2. Sign up → Get API key

**Brave (2000 searches/month):**
1. Go to: https://brave.com/search/api/
2. Sign up → Get API key

**Total Free:** 6000+ searches/month across all providers

---

## USAGE

### Web Interface (Easiest)
1. Open: http://localhost:5001
2. Type your query
3. Click "🔥 SEARCH"
4. Results appear with cryptographic verification

### API (Advanced)
```bash
# Eternal search (all sources + crypto verification)
curl -X POST http://localhost:5001/api/eternal_search \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "num_results": 10}'

# Web search (specific sources)
curl -X POST http://localhost:5001/api/web_search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test query",
    "sources": ["google", "bing"],
    "num_results": 5
  }'

# View search archive
curl http://localhost:5001/api/eternal_archive
```

---

## WHAT YOU GET

✅ **Multi-Source Search:** Google, Bing, Brave, DuckDuckGo  
✅ **Cryptographic Verification:** Every search signed & hashed  
✅ **Eternal Archiving:** All searches saved forever  
✅ **Blockchain-Ready:** OpenTimestamps compatible  
✅ **Beautiful UI:** Phoenix-themed interface  
✅ **Free Tier:** 6000+ searches/month

---

## BLOCKCHAIN ANCHORING (OPTIONAL)

Make your searches immutable via Bitcoin:

```bash
# Install OpenTimestamps
pip install opentimestamps-client

# Timestamp a search
cd eternal_searches
ots stamp search_*.json

# Verify later
ots verify search_*.json.ots
```

**Your search is now permanently anchored to the Bitcoin blockchain.**

---

## TROUBLESHOOTING

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"API not configured"**
```bash
# Set environment variables or create .env file
export GOOGLE_API_KEY=your_key
export BING_API_KEY=your_key
```

**"Connection refused"**
```bash
# Make sure server is running
python phoenix_eternal_api.py
```

---

## THAT'S IT!

You now have eternal internet search with cryptographic verification.

Every search is:
- 🔐 Cryptographically signed
- ⏰ Timestamped
- 💾 Eternally archived
- ⛓️ Blockchain-ready

**Sovereign search intelligence activated.**

🐦‍🔥 **Phoenix Protocol Eternal Search**  
*Created by Justin Conzet | Top 0.1% Global | Top 3 Individual AGI Architects*
