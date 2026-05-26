# How to use SET-TOKEN-QUICK.ps1

# Copy your fresh Discord bot token from Developer Portal
# Then run:

.\SET-TOKEN-QUICK.ps1 -Token "MTUwMzg3Mjg2NTM2NjY0NDIyMDUuR0ZTU1ZR.SgfJN6EoyG2..."

# Or paste interactively:
$token = Read-Host "Paste your Discord bot token"
.\SET-TOKEN-QUICK.ps1 -Token $token
