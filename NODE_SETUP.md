# Human Flourishing Frameworks - Node Installation Guide

Run a local node of the Human Flourishing Frameworks system on **any device**. Connect to the global network and help monitor for AI bias and automated decision-making violations.

---

## Quick Start

### Windows (Easiest)

```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File install.ps1
```

Then start your node:
```powershell
cd $env:USERPROFILE\.hff-node\frameworks
.\start-node.ps1
```

Visit: **http://localhost:5000**

---

### macOS / Linux

```bash
# Run installer
bash install.sh

# Start your node
cd ~/.hff-node/frameworks
./start-node.sh
```

Visit: **http://localhost:5000**

---

### Docker (Any OS)

```bash
# Build the node
docker build -t hff-node .

# Run the node
docker run -p 5000:5000 hff-node
```

Or with docker-compose (easiest):

```bash
# Start node cluster
docker-compose up -d

# View logs
docker-compose logs -f hff-node

# Stop
docker-compose down
```

Visit: **http://localhost:5000**

---

## What Your Node Does

### Local Functions
- ✓ Runs a copy of the transparency dashboard
- ✓ Displays violations and remediation progress
- ✓ Tracks affected persons in your region
- ✓ Validates governance board decisions
- ✓ Stores local data copies

### Network Functions
- ✓ Syncs with central server every 30 seconds
- ✓ Receives updates to violations
- ✓ Submits local violation reports
- ✓ Participates in governance voting (if configured)
- ✓ Contributes to consensus validation

### Data Security
- ✓ All data validated with cryptographic proofs
- ✓ Merkle root verification of board decisions
- ✓ No single point of failure
- ✓ Your node keeps complete audit trail
- ✓ Offline capable (syncs when online)

---

## Node Configuration

Each node auto-generates a unique ID. Configure it by editing `.hff-config.json`:

```json
{
  "node_name": "my-node-1234",
  "network": "human-flourishing-global",
  "api_port": 5000,
  "heartbeat_interval": 30,
  "sync_enabled": true,
  "central_server": "https://human-flourishing-frameworks.herokuapp.com",
  "data_dir": "./data",
  "mode": "local"
}
```

### Options

| Option | Default | Purpose |
|--------|---------|---------|
| `node_name` | auto-generated | Unique identifier for your node |
| `api_port` | 5000 | Port for local dashboard |
| `heartbeat_interval` | 30 | Seconds between network syncs |
| `sync_enabled` | true | Connect to global network |
| `central_server` | heroku.com | Global sync endpoint |
| `mode` | local | `local` or `relay` (relay required admin) |

---

## Node Architecture

```
Your Device
    ↓
[HFF Local Node]
    ├── Dashboard (http://localhost:5000)
    ├── Local Database (./data/node.db)
    ├── Verification Engine
    └── Network Sync (every 30s)
         ↓
    Global Network
    ├── Central Server (Heroku)
    ├── 7,000+ other nodes
    └── Governance Board
```

Every 30 seconds your node:
1. Checks central server for updates
2. Downloads new violations if any
3. Verifies cryptographic proofs
4. Stores in local database
5. Updates dashboard in real-time

---

## API Endpoints (Local)

Access these endpoints on your node:

```bash
# View violations
curl http://localhost:5000/api/violations

# View remediation progress
curl http://localhost:5000/api/remediation

# View affected persons
curl http://localhost:5000/api/affected

# View board decisions
curl http://localhost:5000/api/board

# Node status
curl http://localhost:5000/api/status

# System health
curl http://localhost:5000/api/deployments
```

---

## Troubleshooting

### Port 5000 in use
```bash
# Find what's using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Change port in .hff-config.json
"api_port": 5001
```

### Node won't start
```bash
# Check Python is installed
python --version

# Reinstall dependencies
pip install Flask==2.3.0 numpy==1.24.0 requests==2.31.0

# Run with debug output
python -u dashboard_app.py
```

### Can't connect to global network
- Check internet connection
- Verify central server is online: https://human-flourishing-frameworks.herokuapp.com
- Check firewall allows outbound HTTPS
- Verify in logs: `tail -f logs/node.log`

### Database corrupted
```bash
# Backup existing data
cp -r data data.backup

# Delete database
rm data/node.db

# Restart node - will resync all data
```

---

## Running Multiple Nodes

You can run multiple nodes on the same device:

```bash
# Node 1 - Port 5000
cd ~/.hff-node/frameworks && ./start-node.sh

# Node 2 - Port 5001 (different terminal)
cd ~/.hff-node/frameworks
sed -i 's/"api_port": 5000/"api_port": 5001/' .hff-config.json
./start-node.sh

# Node 3 - Port 5002
cd ~/.hff-node/frameworks
sed -i 's/"api_port": 5001/"api_port": 5002/' .hff-config.json
./start-node.sh
```

---

## Hardware Requirements

### Minimum
- **CPU**: 1 core (any modern processor)
- **RAM**: 512 MB
- **Disk**: 100 MB
- **Network**: Internet connection (can sync offline)

### Recommended
- **CPU**: 2+ cores
- **RAM**: 2 GB
- **Disk**: 1 GB
- **Network**: Broadband connection

### Supported Devices
- ✓ Windows PCs (Windows 10+)
- ✓ macOS (10.14+)
- ✓ Linux (Ubuntu 18.04+, Debian 10+, etc.)
- ✓ Raspberry Pi (requires Python 3.7+)
- ✓ Docker-enabled devices (servers, cloud instances, etc.)
- ✓ Phones (via web interface or mobile wrapper)
- ✓ Virtual machines (VirtualBox, VMware, Hyper-V)
- ✓ Containers (Docker, Kubernetes, etc.)

---

## Mobile Access

Your node is accessible from any device on your network:

```
From your phone/tablet:
  http://<your-computer-ip>:5000
  
To find your computer's IP:
  Windows: ipconfig | findstr IPv4
  Mac/Linux: ifconfig | grep inet
```

Or expose publicly (requires setup):
```bash
# Using ngrok for secure tunneling
ngrok http 5000
# Share the ngrok URL publicly
```

---

## Joining the Global Network

Once your node is running:

1. Visit **http://localhost:5000**
2. Your node is automatically connected to the global network
3. Every 30 seconds it syncs with other nodes
4. Board decisions are replicated across all nodes
5. You can submit reports of violations you discover

---

## Node Registry

See all active nodes:
```bash
curl https://human-flourishing-frameworks.herokuapp.com/api/nodes
```

Your node appears in the registry after first sync.

---

## Governance Participation

To vote on violations:

1. Email: `board@human-flourishing-frameworks.org`
2. Request board membership
3. You'll be added as voting member
4. Cast votes on pending violations
5. Your votes recorded in cryptographic ledger

---

## Data Privacy

Your node stores:
- ✓ Violations (public)
- ✓ Remediation status (public)
- ✓ Board decisions (public)
- ✗ Personal identifying information (stripped)
- ✗ Proprietary systems details (redacted)

All data suitable for public transparency.

---

## Performance

- **Dashboard load**: < 1 second
- **API response**: < 100ms
- **Sync cycle**: 30 seconds
- **CPU usage**: < 2%
- **Memory usage**: 50-200 MB
- **Disk I/O**: Minimal (only during sync)

---

## Advanced Configuration

### Custom Endpoints

```json
{
  "central_server": "http://your-custom-server:8000",
  "api_endpoints": {
    "violations": "/api/v1/violations",
    "board": "/api/v1/board",
    "remediation": "/api/v1/remediation"
  }
}
```

### Relay Mode (Enterprise)

```json
{
  "mode": "relay",
  "relay_upstream": "https://human-flourishing-frameworks.herokuapp.com",
  "relay_downstream": [
    "http://internal-node-1:5000",
    "http://internal-node-2:5000"
  ]
}
```

---

## Getting Help

- **Documentation**: https://github.com/alex-place/human-flourishing-frameworks
- **Issues**: https://github.com/alex-place/human-flourishing-frameworks/issues
- **Community**: https://github.com/alex-place/human-flourishing-frameworks/discussions
- **Contact**: board@human-flourishing-frameworks.org

---

## System Status

Check if everything is working:

```bash
# Dashboard
curl -s http://localhost:5000/api/status | jq .

# Network
curl -s https://human-flourishing-frameworks.herokuapp.com/api/status | jq .

# Violations count
curl -s http://localhost:5000/api/violations | jq 'length'
```

---

## Updates

Your node auto-updates from GitHub:

```bash
# Manual update
cd ~/.hff-node/frameworks
git pull origin master
pip install -r requirements.txt
```

Or enable auto-update in config:

```json
{
  "auto_update": true,
  "update_check_interval": 3600
}
```

---

**Status**: All nodes are part of one global, decentralized network monitoring AI fairness.

**Your node joins the mission**: Making AI systems transparent, fair, and accountable.

Start your node now and help protect human flourishing.
