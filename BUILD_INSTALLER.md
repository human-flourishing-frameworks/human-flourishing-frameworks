# Building the Windows EXE Installer

There are two ways to create the installer:

## Option 1: Using NSIS (Professional Installer)

NSIS creates a professional `human-flourishing-frameworks-installer.exe` that users can double-click to install.

### Step 1: Install NSIS

Download and install from: https://nsis.sourceforge.io/Download

### Step 2: Build the Installer

After installing NSIS:

**Method A: Right-click menu**
1. Right-click `installer.nsi`
2. Select "Compile NSI Script"
3. Wait for build to complete
4. Result: `human-flourishing-frameworks-installer.exe`

**Method B: Command line**
```powershell
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

**Method C: Batch file**
```powershell
.\build-installer.bat
```

### Step 3: Distribute

Share `human-flourishing-frameworks-installer.exe` with users. They can:
- Double-click to install
- Or run: `human-flourishing-frameworks-installer.exe`

---

## Option 2: Direct PowerShell (No Additional Tools Needed)

Users can run the PowerShell installer directly without Git:

```powershell
powershell -ExecutionPolicy Bypass -File install-no-git.ps1
```

**Advantages:**
- ✓ No NSIS installation required
- ✓ Works immediately
- ✓ Can be run from GitHub URL

**Disadvantages:**
- Less polished UI for non-technical users

---

## Installer Features

Both methods install:
- ✓ Python 3.12 (auto-downloads if needed)
- ✓ Repository ZIP (no Git required)
- ✓ Virtual environment
- ✓ All dependencies (Flask, NumPy, Requests)
- ✓ Configuration file
- ✓ Startup scripts
- ✓ Desktop shortcut
- ✓ Start Menu entries

---

## Installation Paths

### NSIS Installer
- Installs to: `C:\Users\<YourUsername>\.hff-node\frameworks`
- Desktop shortcut: `Human Flourishing Node.lnk`
- Start Menu: Programs → Human Flourishing Frameworks

### PowerShell Installer
- Same installation path
- Same shortcuts created

---

## File Sizes

- `install-no-git.ps1` — 7 KB
- `installer.nsi` — 5 KB
- `human-flourishing-frameworks-installer.exe` — ~1 MB (after NSIS build)
- Downloaded during install:
  - Repository: ~5 MB
  - Python (if needed): ~30 MB
  - Dependencies: ~100 MB

---

## Distribution Options

### 1. GitHub Releases
1. Go to https://github.com/alex-place/human-flourishing-frameworks
2. Create a new release
3. Upload `human-flourishing-frameworks-installer.exe`
4. Users download and run

### 2. Website
Host the EXE on a website with:
```html
<a href="/downloads/human-flourishing-frameworks-installer.exe">
  Download Installer for Windows
</a>
```

### 3. Direct Script (No EXE needed)
Users can run:
```powershell
powershell -ExecutionPolicy Bypass -File install-no-git.ps1
```

Or via GitHub:
```powershell
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/alex-place/human-flourishing-frameworks/master/install-no-git.ps1' -OutFile 'install.ps1'; & './install.ps1'"
```

---

## User Installation Steps

### With EXE
```
1. Download human-flourishing-frameworks-installer.exe
2. Double-click the EXE
3. Follow wizard (Next → Next → Install)
4. Click "Finish" to start dashboard
5. Browser opens to http://localhost:5000
```

### Without EXE (Direct PowerShell)
```
1. Open PowerShell as Administrator
2. Run: powershell -ExecutionPolicy Bypass -File install-no-git.ps1
3. Follow prompts
4. Node starts automatically
5. Browser opens to http://localhost:5000
```

---

## Troubleshooting Installer

### EXE won't run
- Right-click → Properties → Unblock (if needed)
- Run as Administrator
- Check Windows Defender doesn't block it (add exception)

### PowerShell script blocked
```powershell
# Fix: Allow script execution for this session only
powershell -ExecutionPolicy Bypass -File install-no-git.ps1
```

### Installation hangs
- Check internet connection
- Check antivirus isn't blocking downloads
- Try running PowerShell script instead

### Python download fails
- Update Windows PowerShell: `choco upgrade powershell`
- Or install Python manually first: https://www.python.org/downloads/

---

## Building Signed Installer (Enterprise)

For organization distribution, you can sign the EXE:

```powershell
# After building with NSIS
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert
Set-AuthenticodeSignature -FilePath human-flourishing-frameworks-installer.exe -Certificate $cert
```

---

## Automatic Build Script

Create `build-installer.bat`:

```batch
@echo off
REM Check for NSIS
if not exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    echo NSIS not found. Install from: https://nsis.sourceforge.io/Download
    exit /b 1
)

echo Building installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build complete!
    echo Output: human-flourishing-frameworks-installer.exe
    pause
) else (
    echo Build failed!
    pause
    exit /b 1
)
```

Run: `build-installer.bat`

---

## Testing the Installer

1. **Clean test:**
   - Delete existing installation
   - Run fresh installer
   - Verify all shortcuts created
   - Launch node from desktop shortcut
   - Verify dashboard loads at http://localhost:5000

2. **Python pre-installed test:**
   - Install Python first
   - Run installer
   - Verify it uses existing Python

3. **Python not installed test:**
   - On system without Python
   - Run installer
   - Should auto-download and install Python
   - Verify node starts

4. **Admin rights test:**
   - Try running as non-admin
   - Should prompt for admin
   - Or show clear error message

---

## Version Updates

To update for new versions:

1. Edit `installer.nsi`:
   - Change `!define APPVERSION "1.0.1"`
   - Update download URL if repo moved

2. Rebuild:
   ```powershell
   makensis installer.nsi
   ```

3. Test thoroughly
4. Upload new EXE to releases

---

## Minimal Alternative: Portable ZIP

No installer needed - just ZIP and extract:

```
human-flourishing-frameworks.zip
├── frameworks/
│   ├── dashboard_app.py
│   ├── requirements.txt
│   └── ...
├── install-no-git.ps1
└── README.txt
```

Users extract and run `install-no-git.ps1`

---

## Next Steps

1. **Build the EXE:**
   ```powershell
   "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
   ```

2. **Test it:**
   - Run on clean Windows machine
   - Verify installation works
   - Check all shortcuts

3. **Publish:**
   - Upload to GitHub Releases
   - Or host on website
   - Share download link

---

**Status**: Ready to build professional Windows installer

All files included. Choose your distribution method and go!
