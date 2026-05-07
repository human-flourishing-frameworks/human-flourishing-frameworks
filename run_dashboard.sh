#!/bin/bash

# Human Flourishing Frameworks - Dashboard Startup Script

echo "=================================="
echo "  TRANSPARENCY DASHBOARD"
echo "  Starting local instance..."
echo "=================================="
echo ""

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing Flask..."
    pip install flask
fi

echo ""
echo "✓ Dependencies ready"
echo ""
echo "🚀 Starting dashboard server..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   🔐 TRANSPARENCY DASHBOARD NOW LIVE"
echo ""
echo "   Open your browser to:"
echo "   👉 http://127.0.0.1:5000"
echo ""
echo "   Tabs available:"
echo "   • 🚨 Violations (real-time monitoring)"
echo "   • 📊 Remediation (healing progress)"
echo "   • 📋 Audits (retroactive verification)"
echo "   • 🗳️ Board Voting (democratic decisions)"
echo "   • 📍 Deployments (active systems)"
echo "   • 👥 Affected Persons (remediation status)"
echo "   • 🔬 Quantum Voting (entangled proofs)"
echo ""
echo "   Press CTRL+C to stop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the dashboard
python3 /tmp/dashboard_app.py
