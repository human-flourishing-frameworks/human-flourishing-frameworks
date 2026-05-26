# Get Fresh Discord Bot Token (5 Minutes)

## Your Bot ID
Your stored bot token belongs to Discord bot ID: **1503872865366442205**

## Quick Fix

1. **Go to Discord Developer Portal**
   - URL: https://discord.com/developers/applications

2. **Find and open your bot**
   - Look for bot with ID: 1503872865366442205
   - Click to open settings

3. **Get fresh token**
   - Go to **Bot** section
   - Click **Reset Token** (or **Copy** if visible)
   - Copy the 72-character token

4. **Set token in PowerShell**
   ```powershell
   .\SET-TOKEN-QUICK.ps1 -Token "paste-token-here"
   ```

5. **Close and reopen PowerShell**

6. **Verify it works**
   ```powershell
   python C:\Users\alexp\.lantern\verify-discord-token.py
   ```

7. **Start the radio**
   ```powershell
   python C:\Users\alexp\.lantern\lantern-lounge-radio.py
   ```

## Ensure Bot is in Your Server
If token still fails, make sure bot is added to your Discord server:
1. Developer Portal → OAuth2 → URL Generator
2. Scopes: ✅ bot
3. Permissions: ✅ Connect, ✅ Speak
4. Copy URL and open in browser
5. Authorize bot to your server

## Create Lounge Channel
Your Discord server needs a voice channel named **Lounge** (exact spelling).
Bot will auto-join this channel when it starts.

---
See also: SET-TOKEN-QUICK.ps1, verify-discord-token.py
