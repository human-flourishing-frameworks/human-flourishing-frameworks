# ADR-3: Discord Bot Architecture — Continuous Playback + Reaction Control

**Status:** Accepted  
**Date:** 2026-05-25  
**Deciders:** Founder, Operations Lead

## Context
Lantern must play ambient music in Lounge 24/7 without gaps. Users control playback via Discord reactions (👍 skip, 👎 replay, ❌ stop). System must survive disconnects and auto-reconnect.

## Decision
Implement async Discord.py bot with:
1. **music_loop task** (every 10s): Check playback state, resume if stopped
2. **on_reaction_add event:** Handle user reactions, queue advancement
3. **Auto-reconnect:** Voice client with `reconnect=True`
4. **Watchdog wrapper:** PowerShell monitors process, auto-restarts if dead

## Options Considered

### Option A: Async Discord.py with Tasks ✅ Chosen
- **Complexity:** Medium
- **Cost:** Low (event-driven)
- **Scalability:** 1 bot per guild (fine for 1 Lounge)
- **Familiarity:** Medium

**Pros:**
- Event-driven (no polling)
- Native Discord integration
- Reaction handling is native
- Built-in auto-reconnect
- <100ms reaction latency

**Cons:**
- Async/await learning curve
- Discord rate limits (manageable)

### Option B: discord.py with Polling
**Rejected:** Inefficient, high latency.

### Option C: Lavalink Audio Service
**Rejected:** Adds infrastructure, defeats local-first goal.

## Trade-off Analysis
Async Discord.py is industry standard. Event-driven reactions have <100ms latency. music_loop task handles crashes gracefully. PowerShell watchdog provides OS-level resilience.

## Consequences
- **Easier:** Instant user feedback, no playback gaps, crash recovery automatic
- **Harder:** Async debugging, Discord rate limits (implement queue)
- **Revisit:** Multi-guild expansion needs architecture refactor

## Implementation

### Core Classes
```python
class LanternRadioWithReactions:
  - _load_tracks()          # Load 28 tracks from ~/.lantern/sounds/
  - play_music()            # FFmpeg streaming at 40% volume
  - _next_track()           # Callback when track ends
  - on_reaction_add()       # Handle 👍👎❌
  - music_loop()            # Task: ensure playback never stops (every 10s)
  - _post_status()          # Update Discord embed with reactions
  - _log()                  # JSONL event logging
```

### Control Reactions
| Emoji | Action | Logic |
|-------|--------|-------|
| 👍 | Skip | `current_idx = (current_idx + 1) % len(playlist)` |
| 👎 | Replay | Re-play current track from start |
| ❌ | Stop | `voice_client.stop()` |

### Volume Settings
- **Base:** 40% (ambient, never louder than talking)
- **FFmpeg filter:** `-filter:a "volume=0.4"` (no dynamic range compression)

### Auto-Reconnect Logic
```
on_disconnect:
  - Log event to JSONL
  - Schedule reconnect (exponential backoff: 1s, 2s, 4s, 8s, max 60s)
  - Resume playback on reconnect
  - Alert watchdog if >5 failures in 5min
```

## Action Items
- [x] lantern-radio-with-reactions.py implemented (268 lines)
- [x] Reaction event handling tested locally
- [x] Auto-reconnect logic implemented
- [ ] Rate-limit queue for reaction removes
- [ ] Discord outage recovery procedure documented

---
**Evidence:** lantern-radio-with-reactions.py ready for deployment, test-lantern-local.py validates queue logic
