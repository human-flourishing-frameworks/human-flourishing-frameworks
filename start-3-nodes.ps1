#!/usr/bin/env powershell
"""
Start 3 local nodes of Human Flourishing Frameworks
Each node runs on a different port and registers independently
"""

$pythonPath = "python"
$appPath = "app.py"
$basePort = 5000

Write-Host "======================================" -ForegroundColor Green
Write-Host "Starting 3 HFF Nodes" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Start Node 1
$port1 = $basePort
$env:PORT = $port1
$env:NODE_NAME = "node-1-local"
$env:PLATFORM = "local-dev"
Write-Host "[NODE 1] Starting on port $port1..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath $pythonPath -ArgumentList $appPath -PassThru | Out-Null
Start-Sleep -Seconds 2

# Start Node 2
$port2 = $basePort + 1
$env:PORT = $port2
$env:NODE_NAME = "node-2-local"
$env:PLATFORM = "local-dev"
Write-Host "[NODE 2] Starting on port $port2..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath $pythonPath -ArgumentList $appPath -PassThru | Out-Null
Start-Sleep -Seconds 2

# Start Node 3
$port3 = $basePort + 2
$env:PORT = $port3
$env:NODE_NAME = "node-3-local"
$env:PLATFORM = "local-dev"
Write-Host "[NODE 3] Starting on port $port3..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath $pythonPath -ArgumentList $appPath -PassThru | Out-Null
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "All 3 Nodes Started Successfully!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the nodes at:" -ForegroundColor Yellow
Write-Host "  Node 1: http://localhost:5000" -ForegroundColor White
Write-Host "  Node 2: http://localhost:5001" -ForegroundColor White
Write-Host "  Node 3: http://localhost:5002" -ForegroundColor White
Write-Host ""
Write-Host "Check adoption stats at:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000/api/adoption/stats" -ForegroundColor White
Write-Host ""
Write-Host "Monitor resilience at:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000/api/resilience/status" -ForegroundColor White
Write-Host ""
Write-Host "To stop all nodes: Close the terminal windows or press Ctrl+C" -ForegroundColor Yellow
