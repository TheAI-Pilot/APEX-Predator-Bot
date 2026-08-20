import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

CATEGORY_MAP = {
    "🚪 START HERE": "🎯 ┃ DEPLOYMENT ZONE",
    "📊 SERVER STATS": "📊 ┃ LIVE SERVER RADAR",
    "💬 COMMUNITY HUB": "💬 ┃ OPERATOR COMMONS",
    "🔫 WARZONE": "🔫 ┃ WARZONE COMBAT SECTOR",
    "🏆 EVENTS & TOURNAMENTS": "🏆 ┃ ESPORTS & ARENA",
    "🎥 STREAMS & CONTENT": "🎬 ┃ MEDIA & LIVESTREAMS",
    "🤖 BOT COMMANDS & UTILS": "🤖 ┃ BOTS & COMMAND HUB",
    "🛡️ STAFF ONLY": "🛡️ ┃ COMMAND HEADQUARTERS"
}

CHANNEL_MAP = {
    # DEPLOYMENT ZONE
    "verify-here": "🛡️・verify-here",
    "rules": "📜・combat-rules",
    "welcome": "👋・operator-welcome",
    "roles": "🏷️・specialty-roles",
    "announcements": "📢・universe-announcements",
    "server-faq": "❓・operator-faq",

    # OPERATOR COMMONS
    "general-chat": "💬・general-intel",
    "warzone-chat": "🔫・warzone-discussion",
    "gamer-tags": "🎮・gamer-tags",
    "looking-for-squad": "🔥・looking-for-squad",
    "squad-recruitment": "🛡️・clan-recruitment",
    "clips-and-highlights": "🎬・clips-and-highlights",
    "warzone-clips": "🎯・sniper-and-clutch-clips",
    "memes-and-media": "😂・memes-and-media",
    "self-promo": "🚀・creator-promo",
    "mini-games": "🕹️・mini-games",

    # WARZONE COMBAT SECTOR
    "warzone-lobby": "📡・warzone-lobby",
    "loadouts-and-meta": "💣・meta-loadouts",
    "warzone-strats": "🧠・tactical-strats",
    "warzone-events": "🎖️・warzone-operations",
    "patch-notes": "📰・official-patch-notes",

    # ESPORTS & ARENA
    "hall-of-fame": "🏆・hall-of-fame",
    "tournaments": "⚔️・kill-race-tournaments",
    "custom-lobbies": "🎯・custom-scrim-lobbies",
    "events-hub": "📅・events-hub",

    # MEDIA & LIVESTREAMS
    "stream-notifications": "🔴・stream-alerts",
    "content-creators": "🎥・featured-creators",
    "youtube-videos": "📺・youtube-drops",

    # BOTS & COMMAND HUB
    "bot-commands": "🤖・bot-terminal",
    "music-requests": "🎵・tactical-radio",
    "ticket-support": "🎫・support-desk",

    # COMMAND HEADQUARTERS
    "staff-chat": "🔒・staff-hq",
    "predator-chat": "🧠・predator-chat",
    "audit-logs": "📋・audit-radar",
    "mod-logs": "⚖️・moderation-logs",
    "ticket-logs": "📁・ticket-transcripts"
}

VOICE_MAP = {
    "Warzone Comms 1": "🎙️ Squad Comms Alpha",
    "Warzone Comms 2": "🎙️ Squad Comms Bravo",
    "Warzone Lobby 1": "🔊 Warzone Lobby Alpha",
    "Warzone Lobby 2": "🔊 Warzone Lobby Bravo",
    "Warzone Lobby 3": "🔊 Warzone Lobby Charlie",
    "Warzone Lobby 4": "🔊 Warzone Lobby Delta",
    "🔊 Duo Comms 1": "🎧 Duo Strike 1",
    "🔊 Duo Comms 2": "🎧 Duo Strike 2",
    "🔊 Trio Comms 1": "⚔️ Trio Fireteam 1",
    "🔊 Trio Comms 2": "⚔️ Trio Fireteam 2",
    "💤 AFK / Gulag Lounge": "💤 The Gulag [AFK]"
}

@client.event
async def on_ready():
    guild = client.guilds[0]
    print(f"Transforming Server: {guild.name} ({guild.id})\n", flush=True)

    # 1. Update Categories
    for cat in guild.categories:
        for old_name, new_name in CATEGORY_MAP.items():
            if old_name.lower() in cat.name.lower() or cat.name.lower() in old_name.lower():
                try:
                    await cat.edit(name=new_name)
                    print(f"✅ Category Renamed: [{old_name}] ➔ [{new_name}]", flush=True)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"❌ Error updating category {cat.name}: {e}", flush=True)

    # 2. Update Text Channels
    for ch in guild.text_channels:
        clean_name = ch.name.replace("・", "").replace("💬", "").replace("🔫", "").replace("📜", "").replace("👋", "").replace("🏷️", "").replace("📢", "").replace("❓", "").replace("🎮", "").replace("🔥", "").replace("🛡️", "").replace("🎬", "").replace("😂", "").replace("🚀", "").replace("🕹️", "").replace("💣", "").replace("🧠", "").replace("📰", "").replace("🏆", "").replace("⚔️", "").replace("🎯", "").replace("📅", "").replace("🔴", "").replace("🎥", "").replace("📺", "").replace("🤖", "").replace("🎵", "").replace("🎫", "").replace("🔒", "").replace("📋", "").replace("⚖️", "").replace("📁", "").strip("-")
        
        for old_key, new_name in CHANNEL_MAP.items():
            if old_key == clean_name or old_key in ch.name.lower():
                if ch.name != new_name:
                    try:
                        await ch.edit(name=new_name)
                        print(f"  + Text Channel Renamed: #{ch.name} ➔ #{new_name}", flush=True)
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"  - Error updating channel {ch.name}: {e}", flush=True)
                break

    # 3. Update Voice Channels
    for vc in guild.voice_channels:
        for old_v, new_v in VOICE_MAP.items():
            if old_v.lower() in vc.name.lower():
                if vc.name != new_v:
                    try:
                        await vc.edit(name=new_v)
                        print(f"  + Voice Channel Renamed: {vc.name} ➔ {new_v}", flush=True)
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"  - Error updating VC {vc.name}: {e}", flush=True)
                break

    print("\n✨ APEX UNIVERSE VISUAL MAKEOVER COMPLETE!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
