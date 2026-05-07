#!/bin/bash
################################################################################
# Human Flourishing Frameworks - Universal Node Installer
# Works on: macOS, Linux, Windows (WSL)
# Creates a local node that connects to the global network
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "================================================================================"
echo "  HUMAN FLOURISHING FRAMEWORKS - LOCAL NODE INSTALLER"
echo "================================================================================"
echo -e "${NC}"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo -e "${YELLOW}Detected OS: $OS${NC}"
echo ""

# Check for required tools
echo -e "${YELLOW}Checking dependencies...${NC}"

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 not found. Please install $1 first.${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 found${NC}"
        return 0
    fi
}

DEPS_OK=true
check_command git || DEPS_OK=false
check_command python3 || DEPS_OK=false

if [ "$DEPS_OK" = false ]; then
    echo -e "${RED}Please install missing dependencies and try again.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Setting up Human Flourishing Frameworks node...${NC}"
echo ""

# Create installation directory
NODE_DIR="$HOME/.hff-node"
if [ ! -d "$NODE_DIR" ]; then
    mkdir -p "$NODE_DIR"
    echo -e "${GREEN}✓ Created node directory: $NODE_DIR${NC}"
else
    echo -e "${GREEN}✓ Node directory exists: $NODE_DIR${NC}"
fi

cd "$NODE_DIR"

# Clone or update repository
if [ -d "frameworks" ]; then
    echo -e "${YELLOW}Updating existing installation...${NC}"
    cd frameworks
    git pull origin master
    cd ..
else
    echo -e "${YELLOW}Cloning Human Flourishing Frameworks...${NC}"
    git clone https://github.com/alex-place/human-flourishing-frameworks.git frameworks
fi

cd frameworks

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q Flask==2.3.0 numpy==1.24.0 requests==2.31.0
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create data directory
mkdir -p data
echo -e "${GREEN}✓ Data directory created${NC}"

# Create local config
cat > .hff-config.json << 'EOF'
{
  "node_name": "local-node",
  "network": "human-flourishing-global",
  "api_port": 5000,
  "heartbeat_interval": 30,
  "sync_enabled": true,
  "central_server": "https://human-flourishing-frameworks.herokuapp.com",
  "data_dir": "./data",
  "mode": "local"
}
EOF
echo -e "${GREEN}✓ Configuration created${NC}"

# Create startup script
cat > start-node.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
echo "Starting Human Flourishing Frameworks local node..."
echo "Dashboard: http://localhost:5000"
echo ""
python dashboard_app.py
EOF
chmod +x start-node.sh

cat > start-node.cmd << 'EOF'
@echo off
call venv\Scripts\activate.bat
echo Starting Human Flourishing Frameworks local node...
echo Dashboard: http://localhost:5000
echo.
python dashboard_app.py
EOF

echo ""
echo -e "${GREEN}================================================================================${NC}"
echo -e "${GREEN}  INSTALLATION COMPLETE${NC}"
echo -e "${GREEN}================================================================================${NC}"
echo ""
echo -e "${CYAN}Your local node is ready!${NC}"
echo ""
echo "To start your node:"
echo -e "  ${YELLOW}cd $NODE_DIR/frameworks${NC}"
echo -e "  ${YELLOW}./start-node.sh${NC}"
echo ""
echo "Access your dashboard:"
echo -e "  ${YELLOW}http://localhost:5000${NC}"
echo ""
echo "Connect to global network:"
echo -e "  Central: https://human-flourishing-frameworks.herokuapp.com${NC}"
echo ""
echo -e "${GREEN}Your node will sync with the global network every 30 seconds.${NC}"
echo ""
