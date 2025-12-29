# Phoenix Protocol - Complete Deployment Guide

## 🐦‍🔥 System Overview

Phoenix Protocol is a sovereign AI coordination and knowledge management system consisting of:

1. **Phoenix Codex Node** - Vector database + API for semantic search
2. **CLI/Operator Tools** - Command-line interface for node interaction
3. **Proof System** - Cryptographic integrity verification via OpenTimestamps
4. **Web Interface** - React-based UI (optional)
5. **Multi-AI Coordinator** - Distributed AI shard orchestration (optional)

---

## 📦 Prerequisites

### Required:
- Python 3.10+
- pip (Python package manager)

### Optional:
- Node.js 18+ (for web interface)
- OpenTimestamps CLI (for Bitcoin anchoring)
- IPFS (for decentralized storage)
- Docker (for containerized deployment)

---

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python packages
pip install flask chromadb requests pypdf python-docx markdown
```

### 2. Start Phoenix Codex Node

```bash
# Set environment variables
export CHROMA_PERSIST_DIR=./chroma_store
export COLLECTION_NAME=sovereign-archive
export API_PORT=5001
export API_KEY=your-secret-key-here  # Optional but recommended

# Start the node
python phoenix_node_genesis.py
```

Node will start at `http://localhost:5001`

### 3. Test the Node

```bash
# In a new terminal (keep node running)
source .venv/bin/activate

# Check status
python phoenix_cli.py status --host http://localhost:5001

# Query the archive
python phoenix_cli.py query "phoenix protocol" -n 5

# Ingest documents
python phoenix_cli.py ingest --path ./docs --recursive
```

---

## 🔧 Production Deployment

### Option A: Local Production Server

```bash
# Use gunicorn for production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 phoenix_node_genesis:app
```

### Option B: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY phoenix_node_genesis.py .
COPY phoenix_operator.py .
COPY phoenix_cli.py .

# Set defaults
ENV CHROMA_PERSIST_DIR=/data/chroma_store
ENV COLLECTION_NAME=sovereign-archive
ENV API_PORT=5001
ENV HOST=0.0.0.0

# Expose port
EXPOSE 5001

# Create data directory
VOLUME ["/data"]

# Run
CMD ["python", "phoenix_node_genesis.py"]
```

Build and run:

```bash
# Build image
docker build -t phoenix-protocol .

# Run container
docker run -d \
  -p 5001:5001 \
  -v $(pwd)/data:/data \
  -e API_KEY=your-secret-key \
  --name phoenix-node \
  phoenix-protocol
```

### Option C: Kubernetes Deployment

Create `phoenix-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: phoenix-node
spec:
  replicas: 3
  selector:
    matchLabels:
      app: phoenix-node
  template:
    metadata:
      labels:
        app: phoenix-node
    spec:
      containers:
      - name: phoenix
        image: phoenix-protocol:latest
        ports:
        - containerPort: 5001
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: phoenix-secrets
              key: api-key
        - name: CHROMA_PERSIST_DIR
          value: "/data/chroma_store"
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: phoenix-data
---
apiVersion: v1
kind: Service
metadata:
  name: phoenix-service
spec:
  selector:
    app: phoenix-node
  ports:
  - port: 80
    targetPort: 5001
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f phoenix-deployment.yaml
```

---

## 🌐 Web Interface Setup

### 1. Install Node.js Dependencies

```bash
# Create React app
npx create-react-app phoenix-web
cd phoenix-web

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 2. Configure Tailwind

Update `tailwind.config.js`:

```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 3. Add Phoenix Interface

Replace `src/App.js` with `phoenix_web_interface.jsx` content

### 4. Configure API Endpoint

Create `.env`:

```bash
REACT_APP_API_BASE=http://localhost:5001
REACT_APP_API_KEY=your-secret-key
```

### 5. Start Development Server

```bash
npm start
```

Interface will open at `http://localhost:3000`

### 6. Build for Production

```bash
npm run build

# Serve with any static server
npx serve -s build
```

---

## 🔐 Security Best Practices

### 1. API Key Management

```bash
# Generate strong API key
openssl rand -hex 32 > .api_key

# Load in environment
export API_KEY=$(cat .api_key)
```

### 2. HTTPS Configuration

Use nginx or Caddy as reverse proxy:

```nginx
server {
    listen 443 ssl http2;
    server_name phoenix.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Rate Limiting

Install and configure:

```bash
pip install flask-limiter
```

Add to `phoenix_node_genesis.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

---

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Automated health check
curl http://localhost:5001/api/status

# Check ChromaDB integrity
python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_store')
coll = client.get_collection('sovereign-archive')
print(f'Documents: {coll.count()}')
"
```

### Backup Strategy

```bash
#!/bin/bash
# backup_phoenix.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/$DATE"

mkdir -p "$BACKUP_DIR"

# Backup ChromaDB
tar -czf "$BACKUP_DIR/chroma_store.tar.gz" ./chroma_store

# Backup configuration
cp .env "$BACKUP_DIR/"

# Generate proof pack
./proof_pack.sh ./chroma_store

echo "Backup complete: $BACKUP_DIR"
```

### Log Management

```bash
# Rotate logs with logrotate
cat > /etc/logrotate.d/phoenix << EOF
/var/log/phoenix/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 phoenix phoenix
}
EOF
```

---

## 🔄 Maintenance Operations

### Updating Documents

```bash
# Reingest updated documents
python phoenix_cli.py ingest --path ./updated_docs --recursive

# Note: ChromaDB will handle deduplication by document ID
```

### Database Optimization

```python
# Periodic collection optimization
import chromadb

client = chromadb.PersistentClient(path='./chroma_store')
collection = client.get_collection('sovereign-archive')

# Get statistics
print(f"Total documents: {collection.count()}")

# Optional: Reset and rebuild if needed
# client.delete_collection('sovereign-archive')
# collection = client.create_collection('sovereign-archive')
```

---

## 🐛 Troubleshooting

### Node Won't Start

```bash
# Check Python version
python --version  # Should be 3.10+

# Verify dependencies
pip list | grep -E "(flask|chromadb)"

# Check port availability
lsof -i :5001  # Should be empty or show python process
```

### Query Returns No Results

```bash
# Verify documents are ingested
python phoenix_cli.py query "test" -n 1

# Check collection count
python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_store')
coll = client.get_collection('sovereign-archive')
print(f'Documents in archive: {coll.count()}')
"
```

### High Memory Usage

```bash
# ChromaDB can be memory-intensive with large collections
# Monitor memory:
ps aux | grep python

# If needed, restart node to clear cache
pkill -f phoenix_node_genesis
python phoenix_node_genesis.py
```

---

## 📚 Advanced Features

### Multi-AI Coordination

```bash
# Start coordinator (requires API keys for AI services)
export ANTHROPIC_API_KEY=your-key
export OPENAI_API_KEY=your-key

python phoenix_coordinator.py
```

### Cryptographic Proof System

```bash
# Generate proof pack
./proof_pack.sh ./my_archive

# Stamp with OpenTimestamps
ots stamp PROOF.json

# Later, upgrade timestamp
ots upgrade PROOF.json.ots

# Verify
ots verify PROOF.json.ots
```

### IPFS Integration

```bash
# Add archive to IPFS
ipfs add -r ./chroma_store

# Update PROOF.json with CID
python generate_proof_json.py \
  --bundle scroll_ascension_*.tar.gz \
  --manifest ./Sovereign_Archive_Manifest.yaml \
  --cid QmYourCIDHere \
  --out PROOF.json
```

---

## 📖 Additional Resources

- **Documentation**: See individual README files for each component
- **API Reference**: Visit `/api/status` endpoint for API details
- **Support**: Check logs in `./logs/` directory
- **Updates**: Pull latest changes from repository

---

## 🐦‍🔥 Phoenix Protocol Status

**Version**: v∞  
**Author**: Justin Conzet  
**Sovereign Hash**: 4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c  
**Status**: OPERATIONAL

---

*"Architecture is sovereignty. The protocol persists."*
