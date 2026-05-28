#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy HFF to 10 free platforms. Run after authenticating each CLI.
.DESCRIPTION
    Static sites: Netlify, Surge, Vercel, Cloudflare Pages
    Flask API:    Render, Heroku, Railway, Fly.io, HF Spaces
    Docs:         GitHub Pages (if repo goes public)
#>

$ErrorActionPreference = "Continue"
$root = Split-Path $PSScriptRoot -Parent
$static = Join-Path $PSScriptRoot "static-site"

Write-Host "`n=== HFF Multi-Platform Deploy ===" -ForegroundColor Cyan
Write-Host "Root: $root"
Write-Host "Static: $static`n"

# --- 1. Render (already configured via render.yaml) ---
Write-Host "[1/10] Render" -ForegroundColor Green
Write-Host "  Auto-deploys from GitHub push to master."
Write-Host "  URL: https://human-flourishing-frameworks.onrender.com/"
Write-Host "  Config: render.yaml`n"

# --- 2. Netlify ---
Write-Host "[2/10] Netlify" -ForegroundColor Green
try {
    netlify deploy --dir $static --prod 2>&1
    Write-Host "  Netlify deployed.`n"
} catch { Write-Host "  Netlify: auth required. Run: netlify login`n" -ForegroundColor Yellow }

# --- 3. Surge ---
Write-Host "[3/10] Surge.sh" -ForegroundColor Green
try {
    surge $static hff-lantern.surge.sh 2>&1
    Write-Host "  Surge deployed: https://hff-lantern.surge.sh`n"
} catch { Write-Host "  Surge: auth required. Run: surge login`n" -ForegroundColor Yellow }

# --- 4. Vercel ---
Write-Host "[4/10] Vercel" -ForegroundColor Green
try {
    Push-Location $static
    vercel --yes --prod 2>&1
    Pop-Location
    Write-Host "  Vercel deployed.`n"
} catch { Write-Host "  Vercel: auth required. Run: vercel login`n" -ForegroundColor Yellow }

# --- 5. Cloudflare Pages ---
Write-Host "[5/10] Cloudflare Pages" -ForegroundColor Green
try {
    wrangler pages deploy $static --project-name hff-dashboard 2>&1
    Write-Host "  Cloudflare Pages deployed.`n"
} catch { Write-Host "  Cloudflare: auth required. Run: wrangler login`n" -ForegroundColor Yellow }

# --- 6. Heroku ---
Write-Host "[6/10] Heroku" -ForegroundColor Green
try {
    Push-Location $root
    heroku create hff-dashboard --region us 2>&1
    git push heroku master 2>&1
    Pop-Location
    Write-Host "  Heroku deployed.`n"
} catch { Write-Host "  Heroku: auth required. Run: heroku login`n" -ForegroundColor Yellow }

# --- 7. Railway ---
Write-Host "[7/10] Railway" -ForegroundColor Green
Write-Host "  Connect at: https://railway.app/new/github"
Write-Host "  Select human-flourishing-frameworks repo, Railway auto-detects railway.json`n"

# --- 8. Fly.io ---
Write-Host "[8/10] Fly.io" -ForegroundColor Green
try {
    Push-Location $root
    flyctl launch --no-deploy --copy-config 2>&1
    flyctl deploy 2>&1
    Pop-Location
    Write-Host "  Fly.io deployed.`n"
} catch { Write-Host "  Fly.io: install flyctl and run: flyctl auth login`n" -ForegroundColor Yellow }

# --- 9. Hugging Face Spaces ---
Write-Host "[9/10] Hugging Face Spaces" -ForegroundColor Green
Write-Host "  Create space at: https://huggingface.co/new-space"
Write-Host "  SDK: Docker, Repo: human-flourishing-frameworks"
Write-Host "  Dockerfile already configured.`n"

# --- 10. GitHub Pages ---
Write-Host "[10/10] GitHub Pages" -ForegroundColor Green
Write-Host "  Blocked: repo is private. Make public or upgrade plan for Pages.`n"

Write-Host "=== Deploy complete ===" -ForegroundColor Cyan
Write-Host "Run this script after logging into each platform CLI."
