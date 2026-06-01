# LANTERN DISCORD RADIO BOT — AUTO-CONNECT & PLAY

Write-Host "========================================" -ForegroundColor Green
Write-Host "LANTERN DISCORD RADIO BOT" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Load Discord token from secure storage
$tokenFile = "C:\Users\alexp\AppData\Roaming\Lantern\discord-bot-token.secure.xml"

if (-not (Test-Path $tokenFile)) {
    Write-Host "✗ Token file not found: $tokenFile" -ForegroundColor Red
    Write-Host "Please save your Discord bot token to:" -ForegroundColor Yellow
    Write-Host "  $tokenFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To encrypt your token:" -ForegroundColor Cyan
    Write-Host '  $token = Read-Host "Discord Bot Token" -AsSecureString' -ForegroundColor White
    Write-Host "  New-Item -Path (Split-Path $tokenFile) -ItemType Directory -Force | Out-Null" -ForegroundColor White
    Write-Host "  ConvertTo-SecureString -AsPlainText -Force | Export-Clixml -Path $tokenFile" -ForegroundColor White
    exit 1
}

try {
    Write-Host "Loading encrypted bot token..." -ForegroundColor Cyan
    $secureString = Import-Clixml -Path $tokenFile
    $token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($secureString)
    )
    Write-Host "✓ Token decrypted" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to decrypt token: $_" -ForegroundColor Red
    exit 1
}

# Set environment variable
$env:DISCORD_BOT_TOKEN = $token

# Check if discord.py is installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
try {
    python -c "import discord; import discord.ext" 2>$null
    Write-Host "✓ discord.py found" -ForegroundColor Green
} catch {
    Write-Host "Installing discord.py and PyNaCl..." -ForegroundColor Yellow
    python -m pip install discord.py PyNaCl -q
    if ($?) {
        Write-Host "✓ Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Check for local audio library
$soundsDir = "$env:USERPROFILE\.lantern\sounds"
if (Test-Path $soundsDir) {
    $trackCount = @(Get-ChildItem -Path $soundsDir -Include @("*.mp3", "*.ogg", "*.wav", "*.flac", "*.m4a") -File).Count
    Write-Host "✓ Found $trackCount audio tracks" -ForegroundColor Green
} else {
    Write-Host "⚠ Audio library not found: $soundsDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting bot..." -ForegroundColor Cyan
Write-Host "Bot will:" -ForegroundColor Cyan
Write-Host "  • Auto-join Discord Lounge voice channel" -ForegroundColor White
Write-Host "  • Auto-play curated music library" -ForegroundColor White
Write-Host "  • Auto-reconnect if disconnected" -ForegroundColor White
Write-Host "  • Support !next, !prev, !stop, !radio, !status commands" -ForegroundColor White
Write-Host ""

# Run the bot
try {
    python bot.py
} catch {
    Write-Host "✗ Bot failed: $_" -ForegroundColor Red
    exit 1
}
