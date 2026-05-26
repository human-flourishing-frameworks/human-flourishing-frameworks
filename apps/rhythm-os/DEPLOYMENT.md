# Rhythm OS Deployment Guide

## Quick Deploy (5 minutes)

### Prerequisites
```powershell
# Check Python version (need 3.8+)
python --version

# Check git
git --version
```

### Step 1: Clone Repository
```bash
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks/apps/rhythm-os
```

### Step 2: Install Dependencies
```bash
pip install flask flask-cors discord.py pynacl
```

### Step 3: Set Discord Token
```powershell
# If you have an encrypted token:
$tokenFile = "C:\Users\alexp\AppData\Roaming\Lantern\discord-bot-token.secure.xml"
$secureString = Import-Clixml -Path $tokenFile
$token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($secureString))
$env:DISCORD_BOT_TOKEN = $token

# Or set directly:
$env:DISCORD_BOT_TOKEN = "your_bot_token_here"
```

### Step 4: Verify Music Library
```bash
ls ~/.lantern/sounds/
# Should show 27+ audio files (.mp3, .ogg, .wav, .flac, .m4a)
```

### Step 5: Start Server
```bash
python server.py
```

### Step 6: Open Dashboard
```
http://localhost:5000
```

---

## Deployment Models

### Model 1: Family A (Personal)

**Use Case**: Single family in van/bus/intentional community

**Hardware**:
- 1 PC (Windows 10+, 4GB RAM, 10GB storage)
- Starlink or LTE connection
- Discord account on family's server

**Setup**:
```powershell
cd C:\rhythm-os
python server.py
```

**Access**: 
- Local network: `http://192.168.1.100:5000` (replace with your IP)
- Web browser on any device on network

**Music Library**: ~/.lantern/sounds/ (27 CC-licensed tracks)

**Cost**: $0 (open source)

**Scaling**: Works for 1-10 people

---

### Model 2: Community (Intentional)

**Use Case**: 5-20 person community sharing music + AI

**Hardware**:
- 1-3 PCs running Rhythm OS
- Shared network (WiFi + Ethernet)
- Shared Discord server

**Setup**:
```bash
# PC 1 (primary)
python server.py

# PC 2-3 (optional, for redundancy)
python server.py --port 5001 --mode replica
```

**Access**:
- Dashboard on shared network
- Discord commands available to all members
- Web UI for librarians to manage curation

**Music Library**: Shared ~/.lantern/sounds/ 
- Add/remove tracks via curator UI
- AI suggests what to add (via Claude)

**Cost**: $0-50/month (optional: Starlink backup)

**Scaling**: Supports 5-20 active users

---

### Model 3: Foundry (Distributed)

**Use Case**: 20 operators × 20 PCs = 40-unit AI augmentation

**Hardware**:
- 20 computers (diverse OS)
- Founder's coordinator server (small VPS)
- Consent-bounded resource sharing

**Setup**:

```bash
# Coordinator (founder's machine)
python server.py --mode coordinator

# Each operator's machine
python server.py --mode agent \
  --coordinator-url http://founder.example.com:5000 \
  --operator-id "alice-01"
```

**Consent Model**:
- Each operator opt-in to sharing:
  - Idle GPU hours
  - Storage space
  - Network bandwidth
  - API quota (when not in use)
- Revocable at any time
- No reach-back once revoked

**Access**:
- Founder: Master dashboard with all 20 machines
- Operators: Personal dashboard + settings
- Revenue share: 10-15% of foundry revenue

**Cost**: 
- Operators: Free (get $290/mo in software + training)
- Founder: $50-200/mo coordinator (VPS + monitoring)

**Scaling**: Supports 40+ concurrent work items

---

## Configuration Files

### `.lantern/config.json`
```json
{
  "mode": "family",
  "discord_bot_token": "ENCRYPTED",
  "music_library": "~/.lantern/sounds",
  "state_dir": "~/.lantern/state",
  "settings": {
    "auto_play": true,
    "loop_mode": "all",
    "parental_control": false,
    "starlink_optimized": true,
    "offline_mode": true
  }
}
```

### `.lantern/consent.json` (Foundry only)
```json
{
  "resources": {
    "gpu_hours_per_day": 8,
    "storage_gb": 100,
    "bandwidth_percent": 50,
    "api_quota_percent": 30
  },
  "revoked_until": "2026-05-31T00:00:00Z",
  "last_updated": "2026-05-26T01:30:00Z"
}
```

---

## Verification Steps

### 1. Server Running
```bash
# Should see:
# [+] Loading music library...
# [+] Loaded 27 tracks from ~/.lantern/sounds/
# [+] Starting web server on http://127.0.0.1:5000
```

### 2. Web Dashboard
```bash
curl http://localhost:5000/
# Should return HTML dashboard
```

### 3. API Health
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "healthy", ...}
```

### 4. Discord Bot
```bash
# Should see in Discord:
# [+] Bot ready: Rhythm OS#1234
# [+] Found Lounge: Lounge
# [+] Connected to Lounge
```

### 5. Music Library
```bash
curl http://localhost:5000/api/playlist
# Should return: {"total_tracks": 27, "tracks": [...]}
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `flask: command not found` | Run `pip install flask` |
| `ModuleNotFoundError: discord` | Run `pip install discord.py` |
| `DISCORD_BOT_TOKEN not set` | Set env var: `$env:DISCORD_BOT_TOKEN = "..."` |
| `[Errno 48] Address already in use` | Change port: `python server.py --port 5001` |
| `No tracks loaded` | Check `~/.lantern/sounds/` has audio files |
| `Bot can't connect to Discord` | Verify bot has join + speak permissions |

---

## Monitoring

### Log Files
```bash
# Web server logs (stdout)
# Discord bot logs
tail -f ~/.lantern/state/rhythm-os.jsonl

# Analytics
curl http://localhost:5000/api/analytics
```

### Health Checks
```bash
# Every 5 minutes
curl http://localhost:5000/api/health

# Full status
curl http://localhost:5000/api/status
```

### Alerts (Future)
- Discord bot disconnected > 1 min
- Music library empty
- Web server down > 2 min
- Starlink latency > 500ms

---

## Scaling Checklist

### From Family to Community
- [ ] Add 2nd PC with agent mode
- [ ] Set up shared network storage
- [ ] Create shared Discord channel
- [ ] Add moderator to curator UI
- [ ] Test load with 10 concurrent users

### From Community to Foundry
- [ ] Deploy coordinator server
- [ ] Create consent form + UI
- [ ] Onboard 5 test operators
- [ ] Set up resource monitoring
- [ ] Establish revenue share process
- [ ] Create operator dashboard

---

## Support

**Documentation**: See README.md

**Issues**: Report on GitHub

**Discord**: Join server for real-time support

**Email**: alex.place.7@gmail.com

---

## License

- **Core**: Source-available (Apache 2.0)
- **Foundry**: Commercial (paid operators)
- **Kids**: AGPL (parental review required)

---

**Deployed**: 2026-05-26  
**Status**: Production (Family A)  
**Version**: 0.1  
**TRL**: 4 (Lab-validated → Field-ready)
