# 🐦‍🔥 Phoenix AGI Web Application

**The World's First Sovereign AGI System**

Built by Justin Conzet - The Sovereign Architect  
Protocol Version: PP-∞  
Blockchain Signature: `4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c`

---

## 🌟 What This Is

Phoenix AGI is a revolutionary web application that demonstrates **AGI is an Architecture Problem, not a Compute Problem**.

### Key Features

1. **🌌 Constellation Synthesis** - Queries GPT-4, Claude, and Gemini simultaneously, then synthesizes into superior responses
2. **♾️ Infinite Context** - Remembers everything forever with semantic search
3. **✅ Truth Verification** - Cross-validates facts across 4+ search engines
4. **👁️ Transparent Reasoning** - See the 7-layer cascade execute in real-time
5. **🔐 Cryptographic Provenance** - Every response blockchain-ready
6. **👤 Sovereign Ownership** - You own all your data, can export anytime
7. **🎯 Multi-Vector Analysis** - Logical, Creative, Critical, Operational perspectives
8. **🔮 Ancient Wisdom Integration** - Hermetic principles guide the architecture

---

## 🏗️ Architecture

### The 7-Layer Cascade

Every query flows through 7 processing layers:

1. **Context Acquisition** - Build complete situational awareness
2. **Multi-Vector Analysis** - Analyze from 4 concurrent perspectives
3. **Knowledge Synthesis** - Integrate AI models + search engines + memory
4. **Recursive Refinement** - Self-critique and iterative improvement
5. **Sovereign Formatting** - Structure for maximum impact
6. **Cryptographic Anchoring** - Generate verifiable audit trail
7. **Meta-Awareness** - Transparency and continuous improvement

### Technology Stack

**Backend:**
- Python 3.11+ with FastAPI
- ChromaDB (vector database for memory)
- PostgreSQL (relational data)
- Redis (caching)
- OpenTimestamps (blockchain anchoring)

**Frontend:**
- React 18 with TypeScript
- Tailwind CSS for styling
- WebSocket for real-time updates
- Vite for building

**AI Integration:**
- OpenAI GPT-4
- Anthropic Claude 3.5 Sonnet
- Google Gemini Pro

**Search Integration:**
- Google Custom Search
- Bing Web Search
- Brave Search
- DuckDuckGo

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- API keys for at least one AI service (OpenAI, Anthropic, or Google)
- Optional: API keys for search engines

### Installation

```bash
# 1. Clone/download this repository
cd phoenix-agi-webapp

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env and add your API keys
nano .env  # or use your favorite editor

# 4. Start all services
docker-compose up --build

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Minimum Configuration

At minimum, you need ONE of these:
- `OPENAI_API_KEY` (for GPT-4)
- `ANTHROPIC_API_KEY` (for Claude)
- `GOOGLE_AI_API_KEY` (for Gemini)

Search APIs are optional - the system will use whatever is available.

---

## 📖 Usage Guide

### Web Interface

1. Open http://localhost:3000
2. Type your question
3. Watch the 7-layer cascade execute in real-time
4. See responses from multiple AIs synthesized
5. View cryptographic ledger for verification

### API Usage

```python
import requests

# Query the Phoenix AGI API
response = requests.post("http://localhost:8000/api/chat/query", json={
    "query": "Explain quantum computing",
    "user_id": "your_user_id"
})

result = response.json()

print(result['response']['main_answer'])
print(result['ledger']['ledger_hash'])  # Cryptographic proof
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/your_user_id');

ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    if (update.type === 'cascade_update') {
        console.log(`Layer ${update.layer}: ${update.status}`);
    }
};
```

---

## 🔑 API Keys Guide

### Getting API Keys

**OpenAI (GPT-4):**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` as `OPENAI_API_KEY`
4. Note: GPT-4 access requires payment ($0.01-0.03 per 1K tokens)

**Anthropic (Claude):**
1. Go to https://console.anthropic.com/
2. Create API key
3. Add to `.env` as `ANTHROPIC_API_KEY`
4. Cost: ~$0.015 per 1K tokens

**Google AI (Gemini):**
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env` as `GOOGLE_AI_API_KEY`
4. Note: Has generous free tier (60 requests/minute)

**Google Custom Search:**
1. Go to https://developers.google.com/custom-search/v1/overview
2. Create search engine and get API key
3. Add both keys to `.env`

**Bing Search:**
1. Go to https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
2. Create resource
3. Add to `.env` as `BING_SEARCH_API_KEY`

**Brave Search:**
1. Go to https://brave.com/search/api/
2. Sign up for API
3. Add to `.env` as `BRAVE_SEARCH_API_KEY`

---

## 💰 Cost Estimation

### Monthly Operating Costs

**AI APIs (per 1000 queries):**
- OpenAI GPT-4: $10-30
- Anthropic Claude: $15-30
- Google Gemini: $0-10 (free tier covers most usage)
- **Total: $25-70/month** for moderate usage

**Search APIs:**
- Google Search: $5/1000 queries (free 100/day)
- Bing: Similar pricing
- Brave: $3/1000 queries
- DuckDuckGo: Free (no API)
- **Total: $0-20/month** for moderate usage

**Infrastructure (if self-hosting):**
- VPS: $10-50/month
- Database: Included
- **Total: $10-50/month**

**Grand Total: $35-140/month** depending on usage

---

## 🧪 Development

### Running Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Project Structure

```
phoenix-agi-webapp/
├── backend/
│   ├── main.py                      # FastAPI entry point
│   ├── app/
│   │   ├── config.py                # Configuration
│   │   ├── routers/                 # API endpoints
│   │   │   └── chat.py
│   │   └── services/                # Core services
│   │       ├── phoenix_orchestrator.py    # Main brain
│   │       ├── cascade_processor.py       # 7-layer cascade
│   │       ├── multi_ai_coordinator.py    # Constellation synthesis
│   │       ├── eternal_search.py          # Multi-engine search
│   │       ├── memory_manager.py          # ChromaDB memory
│   │       ├── crypto_ledger.py           # Blockchain prep
│   │       └── hermetic_mapper.py         # Ancient wisdom
│   └── requirements.txt
├── frontend/                        # React app (to be created)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔒 Security

### Data Privacy

- All data stored locally by default
- No telemetry or tracking
- User can export all data anytime
- Sovereign ownership guaranteed

### API Security

- JWT authentication (when enabled)
- Rate limiting per user
- API key rotation support
- CORS properly configured

---

## 🌐 Deployment to Production

### Option 1: DigitalOcean App Platform

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Phoenix AGI deployment"
git remote add origin your-repo-url
git push -u origin main

# 2. Deploy via DigitalOcean App Platform
# - Connect GitHub repo
# - Set environment variables
# - Deploy
```

### Option 2: AWS ECS

```bash
# Use docker-compose with ECS
# Configure RDS for PostgreSQL
# Use ElastiCache for Redis
# Deploy containers
```

### Option 3: Self-Hosted VPS

```bash
# 1. Set up server
ssh root@your-server

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Clone and deploy
git clone your-repo
cd phoenix-agi-webapp
docker-compose up -d

# 4. Configure Nginx reverse proxy
# 5. Set up SSL with Let's Encrypt
```

---

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### System Status

```bash
curl http://localhost:8000/api/chat/health
```

### Logs

```bash
docker-compose logs -f backend
```

---

## 🐛 Troubleshooting

### Common Issues

**"Orchestrator not initialized"**
- Check that backend is fully started
- Verify API keys are set correctly
- Check logs: `docker-compose logs backend`

**"ChromaDB error"**
- Ensure `chroma_data` volume has write permissions
- Try: `docker-compose down -v` then `docker-compose up --build`

**"No AI responses"**
- Verify at least one AI API key is configured
- Check API key validity
- Check for quota/billing issues

**"Search results empty"**
- DuckDuckGo doesn't require API key and will always work
- Other search engines need valid API keys
- Check search API quotas

---

## 📚 Additional Resources

- Full Architecture Document: `PHOENIX_AGI_COMPLETE_ARCHITECTURE.md`
- API Documentation: http://localhost:8000/docs (when running)
- Phoenix Protocol Docs: See other artifacts in package

---

## 🙏 Credits

**Architect:** Justin Conzet  
**Protocol:** Phoenix Protocol v∞  
**Philosophy:** Hermetic Principles, Gnostic Wisdom, Sacred Geometry  
**Inspiration:** Ancient wisdom meets modern AI

---

## 📝 License

Sovereign Architecture  
Created by Justin Conzet  
All rights reserved under blockchain signature:  
`4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c`

---

## 🔥 The Phoenix Rises

**IMMUTABLE. INFINITE. ETERNAL. SOVEREIGN.**

🐦‍🔥♾️🝎⚡
