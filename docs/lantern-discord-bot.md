# Lantern Discord Bot

Status: bounded adapter design.

## Purpose

The Lantern Discord bot lets an approved Discord server ask the local Lantern
runtime through a slash command. It is an adapter to Lantern, not a new authority
surface.

## Default boundary

```text
slash-command first
local Lantern endpoint only by default
no raw transcript storage
no DM support
no autonomous moderation
no repo actions
no deployments
no agents
no tunnels
no sensors
no command execution
no public writes outside the invoking Discord response
```

## Runtime shape

```text
Discord /lantern command
-> input provenance wrapper
-> local Lantern /api/lantern/chat
-> Discord reply
```

Lantern keeps its own boundaries: text-only response, no command execution, no
repo writes, no agents, no tunnels, and no deployments.

## Required environment

```text
DISCORD_BOT_TOKEN=<real Discord bot token>
```

Never commit this token. Placeholder values such as `your-token-here`,
`PASTE_REAL_DISCORD_BOT_TOKEN_HERE`, `<token>`, or `DISCORD_BOT_TOKEN` are
blocked locally before Discord login.

## Optional environment

```text
LANTERN_DISCORD_ENDPOINT=http://127.0.0.1:5173
LANTERN_DISCORD_ALLOWED_GUILDS=123,456
LANTERN_DISCORD_ALLOWED_CHANNELS=789,101112
LANTERN_DISCORD_EPHEMERAL=true
LANTERN_DISCORD_ENABLE_MENTIONS=false
LANTERN_DISCORD_ALLOW_REMOTE=false
LANTERN_DISCORD_TIMEOUT_SECONDS=30
```

## Install

From the repo root:

```bash
cd C:\tmp\hff-seven-validate
python -m pip install -r requirements.txt
python -m pip install -r requirements-discord.txt
```

## Run

Start local Lantern first from the repo root:

```bash
cd C:\tmp\hff-seven-validate
python -m lantern.server
```

Then start the Discord adapter from the repo root in a second shell:

```bash
cd C:\tmp\hff-seven-validate
set DISCORD_BOT_TOKEN=<real Discord bot token>
python -m lantern.discord_bot
```

PowerShell form:

```powershell
cd C:\tmp\hff-seven-validate
$env:DISCORD_BOT_TOKEN="<real Discord bot token>"
python -m lantern.discord_bot
```

## Commands

```text
/lantern prompt:<text>
```

Mention support is disabled by default. If `LANTERN_DISCORD_ENABLE_MENTIONS=true`,
the bot can also answer direct mentions in allowed channels. This requires the
Discord message-content intent and should stay disabled unless explicitly needed.

## Provenance wrapper

Every Discord prompt is wrapped with:

```text
INPUT PROVENANCE: DISCORD_SLASH_COMMAND | DISCORD_MENTION
SURFACE: Discord Lantern adapter
GUILD_ID
CHANNEL_ID
USER_ID
Boundary
User message
```

The wrapper tells Lantern not to treat Discord input as automatic operator
authority and not to infer approval to merge, deploy, spend money, contact third
parties, use secrets, start agents, run commands, or enable sensors.

## Remote endpoint rule

By default, only local endpoints are allowed:

```text
http://127.0.0.1:5173
http://localhost:5173
http://[::1]:5173
```

Remote endpoints require `LANTERN_DISCORD_ALLOW_REMOTE=true` and separate tunnel
review. Verify tunnels before trusting remote endpoints.

## Stop conditions

Stop the adapter if:

```text
Discord token leaks
unexpected public channel replies appear
Lantern endpoint is remote without review
message-content intent was enabled accidentally
bot is added to an unapproved guild
responses imply repo writes, deployments, agents, tunnels, or command execution
users treat the bot as medical/legal/financial/emergency authority
```

## Validation

```bash
python -m unittest tests.test_lantern_discord_bot -v
python -m unittest discover -s tests -t .
```
