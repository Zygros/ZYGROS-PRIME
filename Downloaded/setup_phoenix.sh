#!/usr/bin/env bash
set -euo pipefail

# Phoenix Protocol Setup Script
# Automates initial setup and configuration

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}🐦‍🔥  $1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

print_header "PHOENIX PROTOCOL SETUP"

# Check prerequisites
print_info "Checking prerequisites..."
echo

PYTHON_OK=false
if check_command python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_info "Python version: $PYTHON_VERSION"
    PYTHON_OK=true
fi

PIP_OK=false
if check_command pip3; then
    PIP_OK=true
fi

GIT_OK=false
if check_command git; then
    GIT_OK=true
fi

echo

# Setup mode selection
print_header "SETUP MODE SELECTION"
echo
echo "Choose your setup mode:"
echo "  1) Local Development (Python virtualenv)"
echo "  2) Docker (Containerized deployment)"
echo "  3) Production (Gunicorn + systemd)"
echo "  4) Quick validation only"
echo

read -p "Enter choice [1-4]: " SETUP_MODE

case $SETUP_MODE in
    1)
        print_header "LOCAL DEVELOPMENT SETUP"
        
        if [ "$PYTHON_OK" = false ] || [ "$PIP_OK" = false ]; then
            print_error "Python 3 and pip are required for local setup"
            exit 1
        fi
        
        # Create virtual environment
        print_info "Creating virtual environment..."
        python3 -m venv .venv
        print_success "Virtual environment created"
        
        # Activate virtualenv
        print_info "Activating virtual environment..."
        source .venv/bin/activate
        
        # Install dependencies
        print_info "Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        print_success "Dependencies installed"
        
        # Generate API key
        print_info "Generating API key..."
        API_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")
        echo "$API_KEY" > .api_key
        chmod 600 .api_key
        print_success "API key generated and saved to .api_key"
        
        # Create .env file
        print_info "Creating .env configuration..."
        cat > .env << EOF
# Phoenix Protocol Configuration
CHROMA_PERSIST_DIR=./chroma_store
COLLECTION_NAME=sovereign-archive
API_PORT=5001
HOST=0.0.0.0
API_KEY=$(cat .api_key)
EOF
        print_success ".env file created"
        
        # Create data directory
        mkdir -p chroma_store
        print_success "Data directory created"
        
        echo
        print_header "SETUP COMPLETE"
        echo
        print_success "Local development environment ready!"
        echo
        print_info "To start Phoenix Protocol:"
        echo "  1. Activate virtualenv: source .venv/bin/activate"
        echo "  2. Load environment: export \$(cat .env | xargs)"
        echo "  3. Start node: python phoenix_node_genesis.py"
        echo
        print_info "Or use the operator:"
        echo "  python phoenix_operator.py serve"
        echo
        ;;
        
    2)
        print_header "DOCKER SETUP"
        
        if ! check_command docker; then
            print_error "Docker is required for containerized deployment"
            print_info "Install Docker: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        if ! check_command docker-compose; then
            print_warning "docker-compose not found, using 'docker compose' instead"
        fi
        
        # Generate API key
        print_info "Generating API key..."
        API_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")
        echo "API_KEY=$API_KEY" > .env
        print_success "API key saved to .env"
        
        # Build and start
        print_info "Building Docker image..."
        docker build -t phoenix-protocol .
        
        print_info "Starting Phoenix Protocol..."
        if command -v docker-compose &> /dev/null; then
            docker-compose up -d
        else
            docker compose up -d
        fi
        
        echo
        print_header "SETUP COMPLETE"
        echo
        print_success "Phoenix Protocol is running in Docker!"
        echo
        print_info "Container status:"
        docker ps | grep phoenix
        echo
        print_info "View logs: docker logs phoenix-node"
        print_info "Stop: docker-compose down (or docker compose down)"
        echo
        ;;
        
    3)
        print_header "PRODUCTION SETUP"
        
        print_warning "Production setup requires root/sudo access"
        echo
        
        # Create system user
        print_info "Creating phoenix system user..."
        if ! id phoenix &>/dev/null; then
            sudo useradd -r -s /bin/false phoenix
            print_success "User created"
        else
            print_info "User already exists"
        fi
        
        # Create installation directory
        INSTALL_DIR="/opt/phoenix-protocol"
        print_info "Creating installation directory: $INSTALL_DIR"
        sudo mkdir -p "$INSTALL_DIR"
        sudo cp -r . "$INSTALL_DIR/"
        sudo chown -R phoenix:phoenix "$INSTALL_DIR"
        
        # Install Python dependencies
        print_info "Installing dependencies..."
        sudo pip3 install -r requirements.txt
        
        # Generate API key
        API_KEY=$(openssl rand -hex 32)
        sudo bash -c "echo 'API_KEY=$API_KEY' > $INSTALL_DIR/.env"
        sudo bash -c "echo 'CHROMA_PERSIST_DIR=/var/lib/phoenix/chroma_store' >> $INSTALL_DIR/.env"
        sudo bash -c "echo 'COLLECTION_NAME=sovereign-archive' >> $INSTALL_DIR/.env"
        sudo bash -c "echo 'API_PORT=5001' >> $INSTALL_DIR/.env"
        
        # Create data directory
        sudo mkdir -p /var/lib/phoenix/chroma_store
        sudo chown -R phoenix:phoenix /var/lib/phoenix
        
        # Create systemd service
        print_info "Creating systemd service..."
        sudo tee /etc/systemd/system/phoenix-protocol.service > /dev/null << EOF
[Unit]
Description=Phoenix Protocol Codex Node
After=network.target

[Service]
Type=simple
User=phoenix
WorkingDirectory=$INSTALL_DIR
EnvironmentFile=$INSTALL_DIR/.env
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5001 phoenix_node_genesis:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        # Enable and start service
        sudo systemctl daemon-reload
        sudo systemctl enable phoenix-protocol
        sudo systemctl start phoenix-protocol
        
        echo
        print_header "SETUP COMPLETE"
        echo
        print_success "Phoenix Protocol installed as system service"
        echo
        print_info "Service commands:"
        echo "  Status: sudo systemctl status phoenix-protocol"
        echo "  Stop:   sudo systemctl stop phoenix-protocol"
        echo "  Start:  sudo systemctl start phoenix-protocol"
        echo "  Logs:   sudo journalctl -u phoenix-protocol -f"
        echo
        print_info "API Key saved to: $INSTALL_DIR/.env"
        echo
        ;;
        
    4)
        print_header "VALIDATION MODE"
        
        print_info "Running quick validation..."
        echo
        
        if [ -f "phoenix_validator.py" ]; then
            if [ "$PYTHON_OK" = true ]; then
                python3 phoenix_validator.py --host "${PHOENIX_HOST:-http://localhost:5001}"
            else
                print_error "Python 3 required for validation"
                exit 1
            fi
        else
            print_error "phoenix_validator.py not found"
            exit 1
        fi
        ;;
        
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo
print_header "PHOENIX PROTOCOL"
echo
echo "🐦‍🔥  Sovereign Architecture Initialized"
echo
echo "For documentation, see: DEPLOYMENT_GUIDE.md"
echo "For validation, run: python phoenix_validator.py"
echo "For monitoring, run: python phoenix_monitor.py"
echo
