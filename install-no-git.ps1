# Human Flourishing Frameworks - Windows Node Installer (No Git Required)
# For users without Git installed - downloads ZIP instead
# Run as Administrator: powershell -ExecutionPolicy Bypass -File install-no-git.ps1

Write-Host "`n" + "="*80 -ForegroundColor Cyan
Write-Host "  HUMAN FLOURISHING FRAMEWORKS - WINDOWS NODE INSTALLER" -ForegroundColor Cyan
Write-Host "  (No Git Required - Downloads from GitHub)" -ForegroundColor Cyan
Write-Host "="*80 + "`n" -ForegroundColor Cyan

# Check for admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "This installer requires Administrator privileges." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host "`nTo run as Administrator:" -ForegroundColor Yellow
    Write-Host "  1. Right-click PowerShell" -ForegroundColor White
    Write-Host "  2. Select 'Run as Administrator'" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    exit 1
}

# Check for Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonFound = $false
$pythonPath = ""

# Check common Python installation locations
$pythonPaths = @(
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Program Files\Python312\python.exe",
    "C:\Program Files\Python311\python.exe",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe"
)

foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $pythonPath = $path
        $pythonFound = $true
        Write-Host "Found Python at: $pythonPath" -ForegroundColor Green
        break
    }
}

# Try to find Python in PATH
if (-not $pythonFound) {
    try {
        $pythonVersion = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonPath = (Get-Command python).Source
            $pythonFound = $true
            Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
        }
    } catch {
        $pythonFound = $false
    }
}

# Python not found - offer to install
if (-not $pythonFound) {
    Write-Host "`nPython 3.9+ is not installed." -ForegroundColor Red
    Write-Host "`nWould you like to download and install Python now? (Y/n)" -ForegroundColor Yellow
    $choice = Read-Host

    if ($choice -ne 'n' -and $choice -ne 'N') {
        Write-Host "`nDownloading Python 3.12..." -ForegroundColor Yellow
        $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
        $pythonInstallerPath = "$env:TEMP\python-installer.exe"

        try {
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath -ErrorAction Stop
            Write-Host "Running Python installer..." -ForegroundColor Yellow
            & $pythonInstallerPath /quiet InstallAllUsers=1 PrependPath=1
            Write-Host "Python installed! Please run this script again." -ForegroundColor Green
            exit 0
        } catch {
            Write-Host "Failed to download Python." -ForegroundColor Red
            Write-Host "Please install Python manually from: https://www.python.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

# Setup directories
$nodeDir = "$env:USERPROFILE\.hff-node"
if (-not (Test-Path $nodeDir)) {
    New-Item -ItemType Directory -Path $nodeDir | Out-Null
    Write-Host "Created node directory: $nodeDir" -ForegroundColor Green
}

Push-Location $nodeDir

# Download repository as ZIP
Write-Host "`nDownloading Human Flourishing Frameworks..." -ForegroundColor Yellow

$zipUrl = "https://github.com/alex-place/human-flourishing-frameworks/archive/refs/heads/master.zip"
$zipPath = "$nodeDir\hff-repo.zip"

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -ErrorAction Stop
    Write-Host "Downloaded successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to download repository. Check your internet connection." -ForegroundColor Red
    exit 1
}

# Extract ZIP
Write-Host "Extracting files..." -ForegroundColor Yellow
Expand-Archive -Path $zipPath -DestinationPath $nodeDir -Force

# Move extracted folder
$extractedFolder = Get-ChildItem -Directory "$nodeDir\human-flourishing-frameworks-*" | Select-Object -First 1
if ($extractedFolder) {
    if (Test-Path "$nodeDir\frameworks") {
        Remove-Item "$nodeDir\frameworks" -Recurse -Force
    }
    Rename-Item -Path $extractedFolder.FullName -NewName "frameworks"
    Remove-Item $zipPath -Force
    Write-Host "Files extracted" -ForegroundColor Green
}

Push-Location frameworks

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    & $pythonPath -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate venv and install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
$activateScript = ".\venv\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    pip install -q Flask==2.3.0 numpy==1.24.0 requests==2.31.0
    Write-Host "Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Create data directory
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host "Data directory created" -ForegroundColor Green
}

# Create config
$nodeId = "windows-node-$(Get-Random -Minimum 10000 -Maximum 99999)"
$config = @{
    node_name = $nodeId
    network = "human-flourishing-global"
    api_port = 5000
    heartbeat_interval = 30
    sync_enabled = $true
    central_server = "https://human-flourishing-frameworks.herokuapp.com"
    data_dir = "./data"
    mode = "local"
} | ConvertTo-Json

$config | Out-File -FilePath ".hff-config.json" -Encoding UTF8
Write-Host "Configuration created (Node ID: $nodeId)" -ForegroundColor Green

# Create startup batch file
@"
@echo off
call venv\Scripts\activate.bat
echo.
echo ================================================================================
echo   HUMAN FLOURISHING FRAMEWORKS - LOCAL NODE
echo ================================================================================
echo.
echo Node ID: $nodeId
echo Dashboard: http://localhost:5000
echo.
echo Starting node...
echo.
python dashboard_app.py
pause
"@ | Out-File -FilePath "start-node.cmd" -Encoding ASCII

# Create startup PowerShell script
@'
# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

Write-Host "`n" + "="*80 -ForegroundColor Cyan
Write-Host "  HUMAN FLOURISHING FRAMEWORKS - LOCAL NODE" -ForegroundColor Cyan
Write-Host "="*80 + "`n" -ForegroundColor Cyan

Write-Host "Dashboard: http://localhost:5000" -ForegroundColor Yellow
Write-Host "`nStarting node...`n" -ForegroundColor Yellow

python dashboard_app.py
'@ | Out-File -FilePath "start-node.ps1" -Encoding UTF8

# Create desktop shortcut
Write-Host "Creating desktop shortcut..." -ForegroundColor Yellow

$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\Human Flourishing Node.lnk"
$startScript = "$PWD\start-node.cmd"

$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $startScript
$shortcut.WorkingDirectory = $PWD
$shortcut.Description = "Human Flourishing Frameworks - Local Node"
$shortcut.Save()

Write-Host "Desktop shortcut created" -ForegroundColor Green

Pop-Location
Pop-Location

# Show completion message
Write-Host "`n" + "="*80 -ForegroundColor Green
Write-Host "  INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "="*80 + "`n" -ForegroundColor Green

Write-Host "Your local node is ready!" -ForegroundColor Cyan
Write-Host "`nTo start your node, use any of these methods:" -ForegroundColor Yellow
Write-Host "  1. Double-click: $desktopPath\Human Flourishing Node.lnk" -ForegroundColor White
Write-Host "  2. Run in PowerShell: cd $nodeDir\frameworks; .\start-node.ps1" -ForegroundColor White
Write-Host "  3. Run in Command Prompt: cd $nodeDir\frameworks; start-node.cmd" -ForegroundColor White

Write-Host "`nAccess your dashboard:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000" -ForegroundColor White

Write-Host "`nConnect to global network:" -ForegroundColor Yellow
Write-Host "  https://human-flourishing-frameworks.herokuapp.com" -ForegroundColor White

Write-Host "`nYour node syncs with the global network every 30 seconds." -ForegroundColor Green
Write-Host ""
