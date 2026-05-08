# Human Flourishing Frameworks - Installation Guide

**Auto-updating nodes. Zero manual updates. Production-ready.**

---

## Quick Start (Choose One)

### 1. **Cloud Deploy (Easiest - No Installation)**
```
👉 https://human-flourishing-frameworks.onrender.com
```
Live dashboard. Deploy in 30 seconds. Automatically updates.

### 2. **pip (Python Package Manager)**
```bash
pip install human-flourishing-frameworks
hff-node
```
Automatic updates every 6 hours.

### 3. **npm (Node Package Manager)**
```bash
npm install -g human-flourishing-frameworks
hff-node
```
Automatic updates every 6 hours.

### 4. **Docker (Container)**
```bash
docker pull human-flourishing-frameworks/human-flourishing-frameworks:latest
docker run -p 5000:5000 human-flourishing-frameworks/human-flourishing-frameworks
```
Auto-pulls latest image. Automatic updates.

### 5. **From Source (Developers)**
```bash
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks
pip install -r requirements.txt
python app.py
```
Automatic `git pull` updates every hour.

---

## Installation Details

### **pip (Recommended for Python)**

```bash
# Install
pip install human-flourishing-frameworks

# Start
hff-node

# Check for updates manually
hff-update

# Dashboard
http://localhost:5000
```

**Auto-updates:** Every 6 hours  
**Management:** Handled by pip  
**Backup:** Automatic (git)

---

### **npm (Recommended for JavaScript/Web)**

```bash
# Install globally
npm install -g human-flourishing-frameworks

# Start
hff-node

# Update manually (if needed)
npm update -g human-flourishing-frameworks

# Dashboard
http://localhost:5000
```

**Auto-updates:** Every 6 hours  
**Management:** Handled by npm  
**Backup:** Automatic (git)

---

### **Docker (Recommended for Teams/Production)**

```bash
# Pull latest image
docker pull alex-place/human-flourishing-frameworks:latest

# Run with auto-update
docker run -d \
  -p 5000:5000 \
  -e AUTO_UPDATE=true \
  --restart always \
  alex-place/human-flourishing-frameworks:latest

# Or use docker-compose
docker-compose up -d

# Dashboard
http://localhost:5000
```

**Auto-updates:** Container restart pulls latest image  
**Management:** Docker  
**Backup:** Automatic (git, persistent volumes)

---

### **From Source (Developers)**

```bash
# Clone
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks

# Install dependencies
pip install -r requirements.txt

# Start
python app.py

# Manual update
git pull origin master
```

**Auto-updates:** Enabled by default (git pull every hour)  
**Management:** git  
**Backup:** Automatic

---

## What Gets Updated

Every 6 hours (or on manual trigger), the system automatically:

✅ **Checks GitHub for new version**  
✅ **Downloads latest code**  
✅ **Verifies integrity** (SHA-256)  
✅ **Backs up current version**  
✅ **Applies update**  
✅ **Restarts service**  
✅ **Zero downtime** (rolling update)

---

## Configuration

### **Auto-Update Control**

```bash
# Enable auto-update (default)
export AUTO_UPDATE=true

# Disable auto-update
export AUTO_UPDATE=false

# Change check interval (seconds)
export UPDATE_CHECK_INTERVAL=3600
```

### **Network Settings**

```bash
# Port
export PORT=5000

# Central server (for adoption tracking)
export CENTRAL_SERVER=https://human-flourishing-frameworks.onrender.com

# Node name
export NODE_NAME=my-node

# Platform
export PLATFORM=docker
```

---

## Verify Installation

```bash
# Check if running
curl http://localhost:5000/health

# View dashboard
open http://localhost:5000

# Check adoption stats
curl http://localhost:5000/api/adoption/stats

# Check resilience
curl http://localhost:5000/api/resilience/status

# Check update status
curl http://localhost:5000/api/updates/status
```

---

## System Requirements

| Method | Python | Node | RAM | Disk |
|--------|--------|------|-----|------|
| pip | 3.9+ | — | 256MB | 500MB |
| npm | — | 14+ | 256MB | 500MB |
| Docker | 3.11 | — | 512MB | 1GB |
| Source | 3.9+ | — | 256MB | 1GB |
| Cloud | — | — | Managed | Managed |

---

## Troubleshooting

### **Update Failed**
```bash
# Check update status
curl http://localhost:5000/api/updates/status

# Manual backup
git branch backup-$(date +%Y%m%d)

# Manual update
git pull origin master
```

### **Port Already in Use**
```bash
# Use different port
export PORT=5001
hff-node
```

### **Connection Issues**
```bash
# Check Render deployment
curl https://human-flourishing-frameworks.onrender.com/health

# Disable central server sync
export CENTRAL_SERVER=http://localhost:5000
```

---

## Advanced

### **Self-Hosted Updates**
```bash
# Run your own update server
export UPDATE_SERVER=https://your-server.com
```

### **Offline Mode**
```bash
# Run without central server
export AUTO_UPDATE=false
export CENTRAL_SERVER=http://localhost:5000
```

### **Production Deployment**
```bash
# Use systemd (Linux)
sudo cp systemd/hff-node.service /etc/systemd/system/
sudo systemctl enable hff-node
sudo systemctl start hff-node
```

---

## Getting Help

- **Docs:** https://github.com/alex-place/human-flourishing-frameworks
- **Issues:** https://github.com/alex-place/human-flourishing-frameworks/issues
- **Live Chat:** Discord (TBD)
- **Email:** alex.place.7@gmail.com

---

**Status:** All methods automatically update. No manual intervention needed.
