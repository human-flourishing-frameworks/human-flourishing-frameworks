# Human Flourishing Frameworks - Quick Start Guide

## Choose Your Installation Method

### Option 1: EXE Installer (Most User-Friendly) ⭐ RECOMMENDED

For non-technical users, a professional Windows installer.

**Installation:**
1. Download `human-flourishing-frameworks-installer.exe`
2. Double-click to run
3. Follow the wizard (Next → Next → Finish)
4. Done! Dashboard opens automatically

**Build the EXE:**
```batch
build-installer.bat
```
(Requires NSIS: https://nsis.sourceforge.io/Download)

**File:** `human-flourishing-frameworks-installer.exe` (~1 MB)

---

### Option 2: PowerShell (No Git Required)

For users without Git installed.

**Installation:**
```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File install-no-git.ps1
```

**What it does:**
- ✓ Checks for Python (installs if needed)
- ✓ Downloads repository (no Git required)
- ✓ Creates virtual environment
- ✓ Installs dependencies
- ✓ Creates desktop shortcut
- ✓ Starts node

**File:** `install-no-git.ps1`

---

### Option 3: Original Git-Based Install

For developers who already have Git.

**Installation:**
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**File:** `install.ps1`

---

### Option 4: Docker (Universal)

For any OS with Docker installed.

**Installation:**
```bash
docker-compose up -d
```

**Access:**
- Dashboard: http://localhost:5000
- Logs: `docker-compose logs -f`

**Files:** `Dockerfile`, `docker-compose.yml`

---

### Option 5: macOS/Linux

For Mac and Linux users.

**Installation:**
```bash
bash install.sh
```

**File:** `install.sh`

---

## Comparison Table

| Method | Requirements | Difficulty | Distribution | File Size |
|--------|--------------|-----------|------------------|-----------|
| **EXE** | Windows 10+ | Easiest | Single .EXE file | ~1 MB |
| **PowerShell** | Windows + PowerShell | Easy | Single .PS1 file | ~7 KB |
| **Git Install** | Git + Python | Medium | .PS1 file | ~8 KB |
| **Docker** | Docker Desktop | Medium | docker-compose.yml | ~10 KB |
| **Bash** | macOS/Linux | Medium | .SH file | ~5 KB |
| **Web Wizard** | Any browser | Easy | Single .HTML file | ~15 KB |

---

## Distribution Guide

### For Most Users: Share the EXE
```
Download: human-flourishing-frameworks-installer.exe
Action: Double-click and follow wizard
Time: 5 minutes including dependencies
```

### For Web Distribution: PowerShell Script
```
Users can run directly from web:
powershell -Command "Invoke-WebRequest -Uri 'https://your-domain.com/install-no-git.ps1' -OutFile 'install.ps1'; & './install.ps1'"
```

### For Tech Users: Docker
```
docker-compose up -d
http://localhost:5000
```

### For macOS/Linux Users: Bash Script
```
bash install.sh
http://localhost:5000
```

---

## What Gets Installed

All methods install the same thing:

✓ Python virtual environment  
✓ Flask web framework  
✓ NumPy (for predictions)  
✓ Requests (for network sync)  
✓ Local SQLite database  
✓ Configuration file  
✓ Startup scripts  
✓ Desktop shortcut  
✓ Start menu entries  

---

## System Requirements

### Minimum
- **OS:** Windows 7+ / macOS 10.14+ / Linux
- **CPU:** 1 core (any processor)
- **RAM:** 512 MB
- **Disk:** 200 MB free
- **Network:** Internet for first setup, optional after

### Recommended
- **OS:** Windows 10+ / macOS 12+ / Ubuntu 20.04+
- **CPU:** 2+ cores
- **RAM:** 2 GB+
- **Disk:** 1 GB free
- **Network:** Broadband

---

## Building the EXE Installer

### Prerequisites
1. Install NSIS from: https://nsis.sourceforge.io/Download
2. Have `installer.nsi` file (already included)

### Build Steps

**Method 1: Batch File (Easiest)**
```batch
build-installer.bat
```

**Method 2: Right-Click**
1. Right-click `installer.nsi`
2. Select "Compile NSI Script"

**Method 3: Command Line**
```bash
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

### Result
```
human-flourishing-frameworks-installer.exe
```
Ready to distribute!

---

## Installation Walkthrough: EXE

### Step 1: Download
User downloads `human-flourishing-frameworks-installer.exe`

### Step 2: Run
Double-click the EXE

### Step 3: Welcome Screen
- App name: "Human Flourishing Frameworks v1.0.0"
- Click "Next"

### Step 4: Installation Directory
- Default: `C:\Users\YourName\.hff-node`
- Click "Next"

### Step 5: Installing
Watch as the installer:
- Downloads the repository
- Checks for Python (installs if needed)
- Creates virtual environment
- Installs dependencies
- Creates configuration

### Step 6: Complete
- Click "Finish"
- Node starts automatically
- Browser opens to http://localhost:5000

### Step 7: Using the Node
- Dashboard shows live violations
- Syncs with global network every 30 seconds
- Desktop shortcut created for quick access

---

## Installation Walkthrough: PowerShell

### Step 1: Download
User downloads `install-no-git.ps1`

### Step 2: Run as Administrator
```powershell
powershell -ExecutionPolicy Bypass -File install-no-git.ps1
```

### Step 3: Script Prompts
```
[OK] Checking dependencies...
Found Python at: C:\Python312\python.exe
[OK] Creating node directory...
[OK] Downloading repository...
[OK] Extracting files...
[OK] Creating virtual environment...
[OK] Installing dependencies...
[OK] Creating configuration...
[OK] Creating shortcuts...

INSTALLATION COMPLETE

Your node is ready!
- Desktop shortcut: "Human Flourishing Node.lnk"
- Dashboard: http://localhost:5000
```

---

## Troubleshooting

### EXE Installation Issues

**"Can't run EXE"**
- Right-click → Properties → Unblock
- Run as Administrator
- Try PowerShell version instead

**"Windows Defender blocked it"**
- Right-click → Properties → Unblock
- Or add exception to Windows Defender

**"Installation hangs"**
- Check internet connection
- Check antivirus isn't blocking
- Try PowerShell version instead

### PowerShell Installation Issues

**"Script is disabled"**
```powershell
powershell -ExecutionPolicy Bypass -File install-no-git.ps1
```

**"Python download fails"**
- Check internet connection
- Install Python manually first: https://www.python.org
- Or try EXE installer (handles auto-install)

**"Permission denied"**
- Right-click PowerShell → Run as Administrator
- Try again

### General Issues

**"Port 5000 already in use"**
- Edit `.hff-config.json`
- Change `"api_port": 5000` to `"api_port": 5001`
- Restart node

**"Can't access http://localhost:5000"**
- Check firewall isn't blocking port 5000
- Ensure Python process is running
- Check console for error messages

**"Not syncing with global network"**
- Check internet connection
- Verify central server is online:
  ```
  https://human-flourishing-frameworks.herokuapp.com
  ```
- Check logs for errors

---

## Getting Help

**Documentation:**
- Full setup guide: `NODE_SETUP.md`
- Build guide: `BUILD_INSTALLER.md`
- This file: `QUICK_START.md`

**Community:**
- GitHub Issues: https://github.com/alex-place/human-flourishing-frameworks/issues
- GitHub Discussions: https://github.com/alex-place/human-flourishing-frameworks/discussions

**Contact:**
- Email: board@human-flourishing-frameworks.org

---

## Next Steps

1. **Choose installation method** (EXE recommended)
2. **Run installer or script**
3. **Open dashboard** at http://localhost:5000
4. **Node automatically syncs** with global network every 30 seconds
5. **Share with others** to grow the network

---

**Status:** All installers ready for distribution  
**Recommended:** Use the EXE installer for best user experience  
**Easy share:** PowerShell script for technical users  
**Advanced:** Docker for containers/servers

Start deploying global nodes now! 🚀
