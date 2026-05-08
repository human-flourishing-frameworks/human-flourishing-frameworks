# Human Flourishing Frameworks - Downloads

## Direct Download Links

### Windows (Recommended)

**Option 1: PowerShell Installer (No Git Required)**
- Download: [`install-no-git.ps1`](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install-no-git.ps1)
- Run: `powershell -ExecutionPolicy Bypass -File install-no-git.ps1`
- Size: 7 KB
- Auto-installs Python if needed
- ⭐ Best for non-technical users

**Option 2: Windows EXE Installer (Recommended)**
- **[BUILD EXE INSTALLER](BUILD_INSTALLER.md)** — Follow steps to create `human-flourishing-frameworks-installer.exe`
- Or use: `build-installer.bat` in the repo
- Size: ~1 MB (after build)
- Professional installer experience
- **[NSIS Required](https://nsis.sourceforge.io/Download)** to build

### macOS / Linux

**Bash Installer**
- Download: [`install.sh`](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install.sh)
- Run: `bash install.sh`
- Size: 5 KB

### Docker (Any OS)

**Docker Setup**
- Files: [`Dockerfile`](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/Dockerfile) + [`docker-compose.yml`](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/docker-compose.yml)
- Run: `docker-compose up -d`

---

## Quick Links

| What You Need | Link | Size | Instructions |
|---------------|------|------|--------------|
| Windows (Easy) | [install-no-git.ps1](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install-no-git.ps1) | 7 KB | [Run in PowerShell](QUICK_START.md) |
| Windows (Pro) | [Build EXE](BUILD_INSTALLER.md) | 1 MB | [Follow guide](BUILD_INSTALLER.md) |
| Mac/Linux | [install.sh](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install.sh) | 5 KB | `bash install.sh` |
| Docker | [docker-compose.yml](https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/docker-compose.yml) | 1 KB | `docker-compose up -d` |
| Setup Help | [QUICK_START.md](QUICK_START.md) | - | Choose your method |
| Node Guide | [NODE_SETUP.md](NODE_SETUP.md) | - | Complete documentation |

---

## Installation Methods at a Glance

### Easiest: PowerShell (Windows)
```powershell
# 1. Right-click PowerShell → Run as Administrator
# 2. Paste this command:
powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install-no-git.ps1' -OutFile 'install.ps1'; & './install.ps1'"
```

### Professional: EXE Installer (Windows)
```batch
# 1. Install NSIS from https://nsis.sourceforge.io/Download
# 2. Clone repo and run:
build-installer.bat
# 3. Share the generated .EXE with users
```

### Simple: Bash (Mac/Linux)
```bash
bash <(curl -s https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install.sh)
```

### Universal: Docker
```bash
git clone https://github.com/alex-place/human-flourishing-frameworks.git
cd human-flourishing-frameworks
docker-compose up -d
```

---

## What You Get After Installation

✓ Local transparency dashboard at http://localhost:5000  
✓ Real violation data (7 documented violations)  
✓ 48,250+ affected persons tracked  
✓ Governance board voting interface  
✓ Auto-sync with global network every 30 seconds  
✓ Cryptographic verification of all data  
✓ Desktop shortcut for quick access  
✓ Automatic updates from GitHub  

---

## System Requirements

### Minimum
- Windows 7+ / macOS 10.14+ / Linux (any distro)
- 1 GB RAM
- 100 MB disk space
- Internet for first run

### Recommended
- Windows 10+ / macOS 12+ / Ubuntu 20.04+
- 2+ GB RAM
- 1 GB disk space
- Broadband internet

---

## Support

| Issue | Solution |
|-------|----------|
| **Can't run PowerShell** | Right-click PowerShell → Run as Administrator |
| **Script blocked** | Use: `powershell -ExecutionPolicy Bypass -File install-no-git.ps1` |
| **Python not found** | Installer auto-downloads it, or install from https://www.python.org |
| **Port 5000 in use** | Edit `.hff-config.json` and change port number |
| **Not syncing** | Check internet connection and firewall |

---

## Advanced Downloads

### GitHub Repository
- Full source code: https://github.com/alex-place/human-flourishing-frameworks
- Clone: `git clone https://github.com/alex-place/human-flourishing-frameworks.git`

### Pre-built Assets
- Binary releases: [GitHub Releases](https://github.com/alex-place/human-flourishing-frameworks/releases)
- Docker images: `docker pull alex-place/human-flourishing-frameworks`

### Documentation
- Complete setup: [NODE_SETUP.md](NODE_SETUP.md)
- Quick start: [QUICK_START.md](QUICK_START.md)
- Building EXE: [BUILD_INSTALLER.md](BUILD_INSTALLER.md)
- Operations: [OPERATIONS.txt](OPERATIONS.txt)

---

## Choose Your Method

**Non-Technical User?**
→ Download `install-no-git.ps1` and run

**Want Professional Installer?**
→ Build EXE with `build-installer.bat` and share

**Linux/Mac?**
→ Run `install.sh`

**Server/Docker?**
→ Use `docker-compose up -d`

---

## Ready to Deploy?

1. **Pick your method** (above)
2. **Download/run installer**
3. **Open http://localhost:5000**
4. **Node automatically syncs** with global network

**That's it!** Your local node is now part of the global Human Flourishing Frameworks network.

---

**Status:** All installers tested and ready for distribution  
**Latest:** Check [GitHub Releases](https://github.com/alex-place/human-flourishing-frameworks/releases) for pre-built binaries  
**Support:** [NODE_SETUP.md](NODE_SETUP.md) for complete documentation
