#!/usr/bin/env python3
"""
LANTERN DISCORD RADIO - STABLE VERSION
Auto-connect, stay connected, play music in Lounge
"""

import os
import discord
from discord.ext import commands, tasks
from pathlib import Path
import asyncio
import json
from datetime import datetime

token = os.environ.get('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

SOUNDS_DIR = Path.home() / '.lantern' / 'sounds'
STATE_DIR = Path.home() / '.lantern' / 'state'
playlist = []
current_voice = None
current_track_idx = 0

def load_playlist():
    global playlist
    audio_ext = ['.mp3', '.ogg', '.wav', '.flac', '.m4a']
    playlist = []
    if SOUNDS_DIR.exists():
        tracks = sorted([f for f in SOUNDS_DIR.iterdir() if f.suffix.lower() in audio_ext])
        playlist = [{'path': str(t), 'name': t.stem} for t in tracks]
    return len(playlist)

def log_event(action, detail=""):
    try:
        log_file = STATE_DIR / 'discord-radio.jsonl'
        entry = {'timestamp': datetime.utcnow().isoformat() + 'Z', 'action': action, 'detail': detail}
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except:
        pass

@bot.event
async def on_ready():
    global current_voice
    print(f'✓ Bot ready: {bot.user}')
    load_playlist()
    print(f'✓ Loaded {len(playlist)} tracks')
    log_event('bot_ready', f'Loaded {len(playlist)} tracks')

    # Find and join Lounge
    await join_lounge()

async def join_lounge():
    global current_voice

    for guild in bot.guilds:
        print(f'Guild: {guild.name}')
        for channel in guild.voice_channels:
            print(f'  Voice channel: {channel.name}')
            if 'lounge' in channel.name.lower():
                print(f'✓ Found Lounge: {channel.name}')

                # Disconnect if already connected somewhere
                if current_voice and current_voice.is_connected():
                    await current_voice.disconnect()
                    await asyncio.sleep(1)

                try:
                    current_voice = await channel.connect(reconnect=True)
                    print(f'✓ Connected to {channel.name}')
                    log_event('connected', channel.name)

                    # Start playing
                    await play_track_by_idx(0)
                    return
                except Exception as e:
                    print(f'✗ Connection failed: {e}')
                    log_event('connection_failed', str(e))

async def play_track_by_idx(idx):
    global current_voice, current_track_idx

    if not playlist or not current_voice or not current_voice.is_connected():
        return

    current_track_idx = idx % len(playlist)
    track = playlist[current_track_idx]

    try:
        if current_voice.is_playing():
            current_voice.stop()

        print(f'▶ Playing: {track["name"]}')
        audio = discord.FFmpegPCMAudio(track['path'])
        current_voice.play(audio, after=lambda e: asyncio.run_coroutine_threadsafe(on_playback_end(), bot.loop).result())
        log_event('track_playing', track['name'])
    except Exception as e:
        print(f'✗ Playback error: {e}')

async def on_playback_end():
    """Auto-play next track when current ends"""
    await asyncio.sleep(0.5)
    await play_track_by_idx(current_track_idx + 1)

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state changes"""
    if member == bot.user:
        if after.channel is None:
            print(f'✗ Disconnected from voice')
            log_event('disconnected', '')
            await asyncio.sleep(2)
            await join_lounge()

@bot.command()
async def next(ctx):
    await play_track_by_idx(current_track_idx + 1)
    await ctx.send(f'▶ {playlist[current_track_idx]["name"]}')

@bot.command()
async def prev(ctx):
    await play_track_by_idx(current_track_idx - 1)
    await ctx.send(f'▶ {playlist[current_track_idx]["name"]}')

@bot.command()
async def stop(ctx):
    global current_voice
    if current_voice:
        if current_voice.is_playing():
            current_voice.stop()
        await current_voice.disconnect()
        current_voice = None
    await ctx.send('⏹ Stopped')

@bot.command()
async def radio(ctx):
    embed = discord.Embed(title='🎙 LANTERN RADIO', color=discord.Color.green())
    for i, track in enumerate(playlist[:15]):
        embed.add_field(name=f'{i+1}. {track["name"]}', value='', inline=False)
    if len(playlist) > 15:
        embed.add_field(name='...', value=f'+{len(playlist)-15} more', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    playing = current_voice.is_playing() if current_voice else False
    embed = discord.Embed(title='Status', color=discord.Color.green())
    embed.add_field(name='Playing', value='Yes' if playing else 'No')
    embed.add_field(name='Tracks', value=len(playlist))
    if playing and current_track_idx < len(playlist):
        embed.add_field(name='Current', value=playlist[current_track_idx]['name'])
    await ctx.send(embed=embed)

try:
    asyncio.run(bot.start(token))
except Exception as e:
    print(f'✗ Fatal: {e}')
    import traceback
    traceback.print_exc()
