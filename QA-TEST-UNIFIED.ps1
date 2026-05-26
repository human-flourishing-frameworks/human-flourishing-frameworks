# UNIFIED QA TEST SUITE - All Systems
# Comprehensive testing for Lantern OS (Windows + Linux paths)

param(
    [string]$TestMode = "full"
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$testsPassed = 0
$testsFailed = 0

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "LANTERN QA TEST SUITE - $timestamp" -ForegroundColor Cyan
Write-Host "Mode: $TestMode" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Python
Write-Host "[*] Testing Python 3..." -ForegroundColor Yellow
$python = python --version 2>&1
if ($python -match "Python 3") {
    Write-Host "[+] PASS: Python installed" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "[-] FAIL: Python not found" -ForegroundColor Red
    $testsFailed++
}

# Test 2: Flask
Write-Host "[*] Testing Flask module..." -ForegroundColor Yellow
python -c "import flask; import flask_cors" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] PASS: Flask available" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "[-] FAIL: Flask not installed" -ForegroundColor Red
    $testsFailed++
}

# Test 3: LLM Backend
Write-Host "[*] Testing LLM backend..." -ForegroundColor Yellow
$ollama = $false
$lmstudio = $false

try {
    $r1 = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 1 -ErrorAction SilentlyContinue
    if ($r1.StatusCode -eq 200) { $ollama = $true }
} catch { }

try {
    $r2 = Invoke-WebRequest -Uri "http://127.0.0.1:1234/v1/models" -TimeoutSec 1 -ErrorAction SilentlyContinue
    if ($r2.StatusCode -eq 200) { $lmstudio = $true }
} catch { }

if ($ollama) {
    Write-Host "[+] PASS: Ollama running (port 11434)" -ForegroundColor Green
    $testsPassed++
}
elseif ($lmstudio) {
    Write-Host "[+] PASS: LM Studio running (port 1234)" -ForegroundColor Green
    $testsPassed++
}
else {
    Write-Host "[-] WARN: No LLM backend detected (will start during deployment)" -ForegroundColor Yellow
}

# Test 4: Key Scripts Present
Write-Host "[*] Testing script files..." -ForegroundColor Yellow
$scripts = @(
    "C:\Users\alexp\.lantern\MASTER-START-ALL.ps1",
    "C:\Users\alexp\.lantern\button-chat-server.py",
    "C:\Users\alexp\.lantern\local-unlimited-chat-ollama.py"
)

$missing = $false
foreach ($script in $scripts) {
    if (-not (Test-Path $script)) {
        Write-Host "  Missing: $script" -ForegroundColor Red
        $missing = $true
    }
}

if (-not $missing) {
    Write-Host "[+] PASS: All scripts present" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "[-] FAIL: Some scripts missing" -ForegroundColor Red
    $testsFailed++
}

# Test 5: Python Syntax
Write-Host "[*] Testing Python syntax..." -ForegroundColor Yellow
$pyfiles = @(
    "C:\Users\alexp\.lantern\button-chat-server.py",
    "C:\Users\alexp\.lantern\local-unlimited-chat-ollama.py"
)

$syntax_ok = $true
foreach ($file in $pyfiles) {
    if (Test-Path $file) {
        python -m py_compile $file 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Syntax error: $file" -ForegroundColor Red
            $syntax_ok = $false
        }
    }
}

if ($syntax_ok) {
    Write-Host "[+] PASS: Python syntax valid" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "[-] FAIL: Python syntax errors" -ForegroundColor Red
    $testsFailed++
}

# Test 6: State Directory
Write-Host "[*] Testing state directory..." -ForegroundColor Yellow
$stateDir = "C:\Users\alexp\.lantern\state"
if (-not (Test-Path $stateDir)) {
    New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
}

$testFile = Join-Path $stateDir "qa-test-$timestamp.txt"
try {
    "test" | Out-File -FilePath $testFile -Force
    Remove-Item $testFile -Force
    Write-Host "[+] PASS: State directory writable" -ForegroundColor Green
    $testsPassed++
} catch {
    Write-Host "[-] FAIL: Cannot write to state directory" -ForegroundColor Red
    $testsFailed++
}

# Test 7: Documentation
Write-Host "[*] Testing documentation..." -ForegroundColor Yellow
$docs = @(
    "C:\Users\alexp\.lantern\LINUX-DEPLOYMENT-GUIDE.md",
    "C:\Users\alexp\.lantern\BDE-MASTER-CONVERGENCE.md"
)

$docs_ok = $true
foreach ($doc in $docs) {
    if (-not (Test-Path $doc)) {
        Write-Host "  Missing: $doc" -ForegroundColor Yellow
        $docs_ok = $false
    }
}

if ($docs_ok) {
    Write-Host "[+] PASS: Core docs present" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "[-] WARN: Some docs missing" -ForegroundColor Yellow
}

# SUMMARY
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "RESULTS" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Passed: $testsPassed" -ForegroundColor Green
Write-Host "Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "STATUS: READY FOR DEPLOYMENT" -ForegroundColor Green
    exit 0
} else {
    Write-Host "STATUS: FIX FAILURES BEFORE DEPLOYMENT" -ForegroundColor Red
    exit 1
}
