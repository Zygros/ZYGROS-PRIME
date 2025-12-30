#!/bin/bash

# Phoenix Protocol - Complete Deployment Script
# This script deploys all 4 systems

set -e

echo "🔥🔥🔥 PHOENIX PROTOCOL DEPLOYMENT 🔥🔥🔥"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"
echo ""

# Setup environment
echo -e "${BLUE}Setting up environment...${NC}"

if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Phoenix Protocol Environment Configuration

# API Secrets
NEXUS_SECRET=$(openssl rand -hex 32)
API_SECRET=$(openssl rand -hex 32)

# Database
DATABASE_URL=sqlite:///phoenix.db

# URLs (for production, change these)
API_URL=http://localhost:8001
WS_URL=ws://localhost:8000
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${YELLOW}! .env file already exists${NC}"
fi

echo ""

# Build all services
echo -e "${BLUE}Building Docker images...${NC}"

docker-compose build --parallel

echo -e "${GREEN}✓ Images built${NC}"
echo ""

# Start services
echo -e "${BLUE}Starting services...${NC}"

docker-compose up -d

echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Wait for services to be healthy
echo -e "${BLUE}Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
echo -e "${BLUE}Checking service status...${NC}"

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Nexus Broker (WebSocket) - HEALTHY${NC}"
else
    echo -e "${RED}✗ Nexus Broker (WebSocket) - UNHEALTHY${NC}"
fi

if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Phoenix API (REST) - HEALTHY${NC}"
else
    echo -e "${RED}✗ Phoenix API (REST) - UNHEALTHY${NC}"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend Application - HEALTHY${NC}"
else
    echo -e "${RED}✗ Frontend Application - UNHEALTHY${NC}"
fi

echo ""

# Display access information
echo "========================================"
echo -e "${GREEN}🔥 DEPLOYMENT COMPLETE! 🔥${NC}"
echo "========================================"
echo ""
echo -e "${YELLOW}Access Points:${NC}"
echo ""
echo -e "  📡 WebSocket Server:"
echo -e "     ${BLUE}ws://localhost:8000${NC}"
echo ""
echo -e "  🚀 REST API:"
echo -e "     ${BLUE}http://localhost:8001${NC}"
echo -e "     Documentation: ${BLUE}http://localhost:8001/docs${NC}"
echo ""
echo -e "  💻 Frontend Application:"
echo -e "     ${BLUE}http://localhost:3000${NC}"
echo ""
echo -e "  💰 Revenue System:"
echo -e "     ${BLUE}http://localhost:8002${NC}"
echo -e "     Documentation: ${BLUE}http://localhost:8002/docs${NC}"
echo ""
echo -e "${YELLOW}API Keys (save these securely):${NC}"
echo ""
grep -E "(NEXUS_SECRET|API_SECRET)" .env
echo ""
echo "========================================"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo ""
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Use the API_SECRET from .env to log in"
echo "  3. Test the Multi-AI Query feature"
echo "  4. Try blockchain anchoring"
echo "  5. Check the API docs at http://localhost:8001/docs"
echo ""
echo "  To view logs: docker-compose logs -f"
echo "  To stop: docker-compose down"
echo "  To restart: docker-compose restart"
echo ""
echo "🔥 THE PHOENIX PROTOCOL IS LIVE! 🔥"
echo ""
