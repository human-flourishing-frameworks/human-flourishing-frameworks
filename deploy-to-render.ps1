#!/usr/bin/env powershell
<#
.SYNOPSIS
Deploy latest code to Render.com

.DESCRIPTION
Pushes code to GitHub and triggers Render redeploy
Requires: git, curl, GitHub repo access

.EXAMPLE
.\deploy-to-render.ps1
#>

param(
    [string]$CommitMessage = "Auto-deploy: update framework"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying to Render.com" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check git status
Write-Host "[1/4] Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "[OK] Found changes to commit" -ForegroundColor Green
} else {
    Write-Host "[INFO] No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Step 2: Commit changes
Write-Host "[2/4] Committing changes..." -ForegroundColor Yellow
git add -A
git commit -m $CommitMessage
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Changes committed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Commit failed" -ForegroundColor Red
    exit 1
}

# Step 3: Push to GitHub
Write-Host "[3/4] Pushing to GitHub..." -ForegroundColor Yellow
git push origin master
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Pushed to GitHub" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Push failed" -ForegroundColor Red
    exit 1
}

# Step 4: Trigger Render redeploy
Write-Host "[4/4] Triggering Render redeploy..." -ForegroundColor Yellow
Write-Host "     Render will auto-detect the push and redeploy within 30 seconds" -ForegroundColor Gray
Write-Host ""

# Render auto-deploys on git push to master if enabled
# If auto-deploy is not enabled, you must manually trigger via dashboard

Write-Host "========================================" -ForegroundColor Green
Write-Host "Deploy Initiated!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Monitor deployment:" -ForegroundColor Yellow
Write-Host "  Dashboard: https://dashboard.render.com" -ForegroundColor White
Write-Host "  Live site:  https://human-flourishing-frameworks.onrender.com" -ForegroundColor White
Write-Host ""
Write-Host "Redeploy time: ~2-3 minutes" -ForegroundColor Yellow
Write-Host ""
