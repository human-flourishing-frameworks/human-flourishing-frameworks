#!/usr/bin/env powershell
<#
Manual Render Deployment Trigger
Opens the Render dashboard and guides you through manual sync
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Render Manual Deploy Required" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Auto-deploy doesn't appear to be enabled." -ForegroundColor Yellow
Write-Host "We need to manually trigger a redeploy." -ForegroundColor Yellow
Write-Host ""

Write-Host "Steps:" -ForegroundColor Green
Write-Host "1. Opening Render dashboard in your browser..." -ForegroundColor White
Write-Host ""

$dashboard = "https://dashboard.render.com"
Write-Host "   $dashboard" -ForegroundColor Cyan
Write-Host ""

Write-Host "2. In the dashboard:" -ForegroundColor Green
Write-Host "   - Find 'human-flourishing-frameworks' service" -ForegroundColor White
Write-Host "   - Click it to open service details" -ForegroundColor White
Write-Host "   - Click 'Manual Sync' button (top right)" -ForegroundColor White
Write-Host "   - Wait 2-3 minutes for deployment" -ForegroundColor White
Write-Host ""

Write-Host "3. To enable auto-deploy in future:" -ForegroundColor Green
Write-Host "   - Go to Settings → Auto-Deploy" -ForegroundColor White
Write-Host "   - Toggle ON" -ForegroundColor White
Write-Host ""

Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process $dashboard

Write-Host ""
Write-Host "After deployment, check:" -ForegroundColor Cyan
Write-Host "  https://human-flourishing-frameworks.onrender.com" -ForegroundColor White
Write-Host ""
