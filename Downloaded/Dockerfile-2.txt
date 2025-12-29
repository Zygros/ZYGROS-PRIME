FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY phoenix_node_genesis.py .
COPY phoenix_operator.py .
COPY phoenix_cli.py .

# Set environment defaults
ENV CHROMA_PERSIST_DIR=/data/chroma_store \
    COLLECTION_NAME=sovereign-archive \
    API_PORT=5001 \
    HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

# Create data directory
RUN mkdir -p /data

# Expose API port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/api/status || exit 1

# Run the application
CMD ["python", "phoenix_node_genesis.py"]
