# Rhythm OS — Music + AI Convergence

**Unified, open-source operating system that converges music curation, AI chat, Discord orchestration, and privacy-first attestation.**

## The Convergence

Rhythm OS is the **novel package** that merges four previously separate systems:

| System | Role | Integration |
|--------|------|-------------|
| **Discord Radio Bot** | Auto-connects to voice, auto-plays music | WebSocket control via web UI |
| **Lantern Music Curator** | 27 CC-licensed tracks + AI selection | AI-driven playlist management |
| **Suzie Orchestrator** | Task routing + agent slot management | Route web requests to agents |
| **M5 Attestation** | Privacy-first cryptographic proof | Sign user actions + consent |

**Result**: A single unified operating system that families in vans, off-grid communities, and privacy-conscious users can deploy locally and control from a web browser.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors discord.py pynacl
```

### 2. Set Discord Token

```powershell
$env:DISCORD_BOT_TOKEN = "your_bot_token_here"
```

### 3. Start Rhythm OS

```bash
python server.py
```

### 4. Open Browser

```
http://localhost:5000
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         Rhythm OS Web Dashboard (Browser)           │
│  (Player, Curator, Settings, Analytics, Modules)   │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/WebSocket
                       ▼
┌─────────────────────────────────────────────────────┐
│           Rhythm OS Web API (Flask)                 │
│  /api/status, /api/bot/*, /api/curator/*           │
└────┬───────────────┬────────────┬──────────┬────────┘
     │               │            │          │
     ▼               ▼            ▼          ▼
 Discord         Lantern    Suzie        M5
 Bot             Curator    Orchestrator Attestation
 └─Discord   └─27 Tracks   └─Task       └─Privacy
   Lounge     └─AI Select    Routing     └─Consent
   │           │             │           │
   └─ Internet Archive       │           │
      Integration            ▼           │
                        (MCP Boundary)   │
                                         ▼
                                    (Future)
                            Foundry Resource Pool
```

## Features

### 🎵 Music Curation
- 27 CC-licensed recordings (Xeno-Canto, IMSLP, Wikimedia)
- Mix of nature sounds (whales, birds, frogs) + classical (Mozart, Bach)
- Zero cloud dependency
- Parental review optional

### 🤖 AI Integration
- **Lantern Chat**: Claude AI for questions + learning
- **Music Curator**: Smart playlist selection
- **Suzie Orchestrator**: Route requests to agents
- **M5 Attestation**: Cryptographic proof of actions
- **MCP Connectors**: 3 connected (GitHub, Asana, Linear)

### 🎮 Control Methods
- **Web Dashboard** (recommended): Full visual control
- **Discord Commands**: !next, !prev, !stop, !radio, !status
- **API Endpoints**: Programmatic control
- **Offline-First**: Works without internet (plays local library)

### 📡 Starlink-Optimized
- Tested on Starlink (avg 142ms latency)
- Auto-reconnect on network blips
- Bounded bandwidth usage
- No streaming services required

### 🔒 Privacy-First
- Zero cloud tracking
- Local music library only
- M5 attestation for consent proof
- Parental controls built-in

---

## Web Dashboard Sections

### Player
- Play/pause/next/prev controls
- Volume slider
- Now playing info with progress bar
- Queue management

### AI Integration
- Status of all Lantern modules
- Module availability
- Orchestration status

### Playlist
- All 27 tracks listed
- Active track highlighted
- Click to jump to track

### Curator
- Curation rules
- Source information
- Refresh library button
- Add Internet Archive integration

### Settings
- Auto-play toggle
- Loop mode (All/One/Off)
- Parental controls
- Offline mode
- Starlink optimization
- Discord auto-join

### Analytics
- Session uptime
- Tracks played count
- Connection latency
- System health status
- Reconnection count

---

## API Reference

### Status & Health

```bash
GET /api/status
GET /api/health
GET /api/analytics
```

### Playback Control

```bash
POST /api/bot/next
POST /api/bot/prev
POST /api/bot/pause
POST /api/bot/stop
```

### Content

```bash
GET /api/playlist
GET /api/curator/rules
GET /api/modules
```

---

## Configuration

Settings are stored in `~/.lantern/state/rhythm-os.json`:

```json
{
  "auto_play": true,
  "loop_mode": "all",
  "parental_control": false,
  "discord_auto_join": true,
  "offline_mode": true,
  "starlink_optimized": true,
  "volume": 75
}
```

---

## Logging

All events logged to `~/.lantern/state/rhythm-os.jsonl`:

```json
{"timestamp": "2026-05-26T01:33:05Z", "action": "bot_ready", "detail": "Loaded 27 tracks"}
{"timestamp": "2026-05-26T01:33:06Z", "action": "track_playing", "detail": "Mozart — Eine kleine Nachtmusik"}
{"timestamp": "2026-05-26T01:33:25Z", "action": "track_skipped", "detail": "next"}
```

---

## Deployment Models

### Family A: Personal
- 1 computer per family
- Local-only music library
- Discord voice for family members
- No foundry resource sharing

### Community: Intentional
- 5-20 people sharing library
- Shared Discord server
- Opt-in resource contribution
- Revenue share (future)

### Foundry: Distributed
- 20 operators × 20 computers
- Aggregate compute + storage
- Consent-bounded resource pool
- Professional deployment

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot doesn't connect | Check `DISCORD_BOT_TOKEN` env var |
| No music plays | Verify `~/.lantern/sounds/` has audio files |
| Web UI won't load | Ensure Flask server running on :5000 |
| Starlink latency | Enable "Starlink Optimized" in settings |

---

## Use Cases

✓ **Van-life families** — Music on the road, no streaming bills
✓ **Intentional communities** — Shared music library, offline-first
✓ **Homeschooling** — AI tutor + music for learning
✓ **Accessibility** — Privacy-first for disabled/elderly users
✓ **Foundry operators** — Distributed compute + music hosting

---

## Roadmap

- [ ] Internet Archive integration (10k+ public domain tracks)
- [ ] Vosk STT for voice control
- [ ] ParentalReview UI for K-12
- [ ] MCP server for Rhythm OS (marketplace distribution)
- [ ] Mobile app (iOS/Android)
- [ ] Foundry resource pool (Revenue share)

---

## Architecture Decision Records (ADRs)

### ADR-1: Web-First Interface
**Decision**: Use Flask + HTML5 instead of desktop app
**Rationale**: Browser-based = cross-platform (Windows/Mac/Linux), no install friction
**Trade-off**: Slightly higher latency vs. universal accessibility

### ADR-2: Local Music Only
**Decision**: 27 CC-licensed tracks, no cloud streaming
**Rationale**: Works offline, zero data tracking, Starlink-friendly
**Trade-off**: Smaller library vs. privacy + reliability

### ADR-3: Discord as Transport
**Decision**: Use Discord voice channel as the playback medium
**Rationale**: Family members already on Discord, no extra app
**Trade-off**: Requires Discord server access vs. unified experience

### ADR-4: Suzie Orchestration
**Decision**: Route all requests through Suzie task queue
**Rationale**: Single bottleneck for resource limits + consent checking
**Trade-off**: Slightly more latency vs. safety + observability

---

## Patent Pending

**Novel aspects**:
1. **Convergence model**: First OS to unify music curation + AI orchestration + privacy attestation
2. **Starlink optimization**: Auto-detected latency bounds for off-grid deployment
3. **Consent-bounded resource pool**: Operators explicitly grant compute/storage per-item
4. **Privacy-first M5**: Cryptographic proof of parental review without cloud logging

---

## License

- **Core**: Source-available (view, modify, deploy)
- **Commercial**: Paid foundry tier for revenue-share operators
- **Kids Edition**: AGPL (parental-controlled)

---

## Contact & Support

**Founder**: Alex Place  
**Email**: alex.place.7@gmail.com  
**Status**: Production (Family A) — 2026-05-26  
**Version**: 0.1 (TRL 4)

---

**Built with ❤️ for families living offline-first, on Starlink, in vans, and in intentional communities.**
