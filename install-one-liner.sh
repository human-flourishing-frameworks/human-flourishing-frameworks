#!/bin/bash
# One-liner installer for Human Flourishing Frameworks
# Run this: curl -sSL https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install-one-liner.sh | bash

set -e

echo ""
echo "=================================="
echo "Human Flourishing Frameworks"
echo "Installing Node..."
echo "=================================="
echo ""

# Clone repo
INSTALL_DIR="${HOME}/.hff-node"
git clone https://github.com/alex-place/human-flourishing-frameworks.git "$INSTALL_DIR/frameworks" 2>/dev/null || (cd "$INSTALL_DIR/frameworks" && git pull origin master)

cd "$INSTALL_DIR/frameworks"

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -q Flask==2.3.0 gunicorn==21.2.0

# Create data dir
mkdir -p data

# Start
echo ""
echo "[OK] Installation complete!"
echo ""
echo "Dashboard: http://localhost:5000"
echo ""
echo "Starting node..."
echo ""

python app.py
