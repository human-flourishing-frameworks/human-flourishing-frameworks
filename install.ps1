# Human Flourishing Frameworks - Windows Node Installer
# Run as Administrator: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "`n" + "="*80 -ForegroundColor Cyan
Write-Host "  HUMAN FLOURISHING FRAMEWORKS - WINDOWS NODE INSTALLER" -ForegroundColor Cyan
Write-Host "="*80 + "`n" -ForegroundColor Cyan

# Check for admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "This installer requires Administrator privileges." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    exit 1
}

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$depsOK = $true

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Install from: https://git-scm.com/download/win" -ForegroundColor Red
    $depsOK = $false
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Install from: https://www.python.org/downloads/" -ForegroundColor Red
    $depsOK = $false
}

if (-not $depsOK) {
    Write-Host "`nPlease install missing dependencies and try again." -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies OK`n" -ForegroundColor Green

# Setup directories
$nodeDir = "$env:USERPROFILE\.hff-node"
if (-not (Test-Path $nodeDir)) {
    New-Item -ItemType Directory -Path $nodeDir | Out-Null
    Write-Host "Created node directory: $nodeDir" -ForegroundColor Green
}

Push-Location $nodeDir

# Clone or update repo
if (Test-Path "frameworks") {
    Write-Host "Updating existing installation..." -ForegroundColor Yellow
    Push-Location frameworks
    git pull origin master 2>&1 | Out-Null
    Pop-Location
} else {
    Write-Host "Cloning Human Flourishing Frameworks..." -ForegroundColor Yellow
    git clone https://github.com/alex-place/human-flourishing-frameworks.git frameworks 2>&1 | Out-Null
}

Push-Location frameworks

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate venv
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q Flask==2.3.0 numpy==1.24.0 requests==2.31.0
Write-Host "Dependencies installed" -ForegroundColor Green

# Create data directory
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host "Data directory created" -ForegroundColor Green
}

# Create config
$config = @{
    node_name = "windows-node-$(Get-Random -Minimum 1000 -Maximum 9999)"
    network = "human-flourishing-global"
    api_port = 5000
    heartbeat_interval = 30
    sync_enabled = $true
    central_server = "https://human-flourishing-frameworks.herokuapp.com"
    data_dir = "./data"
    mode = "local"
} | ConvertTo-Json

$config | Out-File -FilePath ".hff-config.json" -Encoding UTF8
Write-Host "Configuration created" -ForegroundColor Green

# Create startup batch file
@'
@echo off
call venv\Scripts\activate.bat
echo.
echo ================================================================================
echo   HUMAN FLOURISHING FRAMEWORKS - LOCAL NODE
echo ================================================================================
echo.
echo Dashboard: http://localhost:5000
echo.
echo Starting node...
echo.
python dashboard_app.py
'@ | Out-File -FilePath "start-node.cmd" -Encoding ASCII

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

Pop-Location
Pop-Location

Write-Host "`n" + "="*80 -ForegroundColor Green
Write-Host "  INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "="*80 + "`n" -ForegroundColor Green

Write-Host "Your local node is ready!" -ForegroundColor Cyan
Write-Host "`nTo start your node:" -ForegroundColor Yellow
Write-Host "  cd $nodeDir\frameworks" -ForegroundColor White
Write-Host "  .\start-node.ps1" -ForegroundColor White
Write-Host "`nAccess your dashboard:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host "`nConnect to global network:" -ForegroundColor Yellow
Write-Host "  https://human-flourishing-frameworks.herokuapp.com" -ForegroundColor White
Write-Host "`nYour node syncs with the global network every 30 seconds." -ForegroundColor Green
Write-Host ""
