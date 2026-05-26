# Lantern Discord Radio Bot

Auto-connecting Discord music bot for streaming the Lantern audio library directly into Discord voice channels.

## Features

- **Auto-connect**: Finds and joins the "Lounge" voice channel automatically on startup
- **Auto-play**: Plays music from the local Lantern library without user commands
- **Auto-reconnect**: Automatically rejoins if disconnected (network blip, bot restart, etc.)
- **Offline-first**: Uses local FFmpeg, works with Starlink and unreliable connections
- **Zero interaction**: Just start the bot, it handles everything

## Requirements

- Python 3.8+
- discord.py 2.0+
- FFmpeg (for audio playback)
- Valid Discord bot token stored in `$env:DISCORD_BOT_TOKEN`
- Lantern audio library in `~/.lantern/sounds/`

## Installation

```powershell
# Install dependencies
pip install discord.py PyNaCl

# Set the bot token (from your Discord Developer Portal)
$env:DISCORD_BOT_TOKEN = "your_bot_token_here"

# Run the bot
python bot.py
```

## Configuration

The bot looks for:
- **Discord bot token**: `$env:DISCORD_BOT_TOKEN` environment variable
- **Audio library**: `~/.lantern/sounds/` directory with `.mp3`, `.ogg`, `.wav`, `.flac`, or `.m4a` files
- **Voice channel name**: Automatically finds a channel containing "lounge" (case-insensitive)

## Commands

Once running in Discord:

| Command | Description |
|---------|-------------|
| `!radio` | Show all available tracks |
| `!next` | Skip to next track |
| `!prev` | Play previous track |
| `!stop` | Stop playback and disconnect |
| `!status` | Show current playback status |

## Logging

Connection and playback events are logged to `~/.lantern/state/discord-radio.jsonl` for debugging.

## Troubleshooting

**"No guilds found"** — Make sure the bot is in at least one Discord server

**"No voice channels found"** — Your server needs a voice channel with "lounge" in the name

**"Failed to connect"** — Verify the bot has permissions to connect and speak in voice channels (admin role recommended)

**"Connection keeps dropping"** — The bot includes automatic reconnection; if this continues, check your Discord token is valid and the bot hasn't been rate-limited

## Architecture

- Uses `discord.py` with reconnect=True for stability
- Monitors voice state changes via `on_voice_state_update` to detect disconnects
- Auto-plays next track when current track finishes
- Bounded connection loop with 2-second delay between reconnection attempts

## Use Cases

- **Van-life families**: Stream music while traveling with Starlink
- **Off-grid communities**: Music curator without relying on cloud streaming services
- **Intentional communities**: Group listening without bandwidth-heavy Spotify
- **Accessibility**: Privacy-first alternative with parental curation options

---

Built as part of Lantern OS for local-first, privacy-respecting household AI.
