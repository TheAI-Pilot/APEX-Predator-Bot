import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("Error: DISCORD_TOKEN not found in .env")
    sys.exit(1)

intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    print(f"\n=======================================================", flush=True)
    print(f"⚡ DEPLOYING FREE BOT FEATURE MASTER GUIDES & CONFIG", flush=True)
    print(f"=======================================================\n", flush=True)

    # 1. Post Complete Bot Directory in #bot-commands
    bot_ch = discord.utils.get(guild.text_channels, name="bot-commands")
    if bot_ch:
        try:
            await bot_ch.purge(limit=10)
        except:
            pass

        embed1 = discord.Embed(
            title="🤖 APEX UNIVERSE — BOT COMMANDS & UTILITIES MASTER GUIDE",
            description="All active bots on **Apex Universe** are configured with **zero feature overlap**! Below are the full free commands and capabilities available to all members.\n",
            color=discord.Color.from_rgb(52, 152, 219)
        )
        embed1.add_field(
            name="💎 1. Sapphire Bot (Onboarding & Roles)",
            value="• `/roles` / Reaction buttons in <#roles> for self-assigning game and ping roles.\n"
                  "• Automatic rich visual welcome cards in <#welcome>.\n"
                  "• Instant server boost celebrations in <#general-chat>.",
            inline=False
        )
        embed1.add_field(
            name="🛡️ 2. APEX PREDATOR (Moderation, AutoMod & Tickets)",
            value="• `/ticket` / Click button in <#ticket-support> to open a private staff support room.\n"
                  "• `/warn`, `/timeout`, `/kick`, `/ban`, `/purge` for staff enforcers.\n"
                  "• Real-time anti-spam, raid shield, and audit tracking in <#mod-logs> and <#audit-logs>.",
            inline=False
        )
        embed1.add_field(
            name="⭐ 3. MEE6 Bot (XP & Leveling System)",
            value="• `!rank` — Check your current chat XP level, progress bar, and server rank.\n"
                  "• `!levels` — View the top community chat leaderboard.\n"
                  "• Auto-posts live Twitch and YouTube stream alerts in <#stream-notifications>.",
            inline=False
        )
        embed1.add_field(
            name="🤖 4. Carl-Bot (Tags & Utilities)",
            value="• `!tag <tagname>` — Fetch server quick-guides and info shortcuts.\n"
                  "• Fast utility calculations, avatar inspects, and member tags.",
            inline=False
        )
        embed1.add_field(
            name="🌐 5. iTranslator (Multi-Language Squad Translation)",
            value="• React with a flag emoji (e.g. 🇪🇸, 🇫🇷, 🇩🇪, 🇮🇳, 🇯🇵) on any message to translate it.\n"
                  "• `/translate to:<language> text:<message>` — Translate text directly.",
            inline=False
        )
        embed1.set_footer(text="Keep all general bot spam in #bot-commands • Apex Universe Staff")
        await bot_ch.send(embed=embed1)
        print("  + Sent Master Bot Guide to #bot-commands", flush=True)

    # 2. Post Green-Bot Audio Controls in #music-requests
    music_ch = discord.utils.get(guild.text_channels, name="music-requests")
    if music_ch:
        try:
            await music_ch.purge(limit=10)
        except:
            pass

        embed_music = discord.Embed(
            title="🎵 GREEN-BOT — HIGH DEFINITION AUDIO CONTROLS",
            description="Listen to high-fidelity music inside any Warzone lobby or squad voice channel!\n",
            color=discord.Color.from_rgb(46, 204, 113)
        )
        embed_music.add_field(
            name="🎧 Playback Commands",
            value="• `/play <song or playlist link>` — Stream from Spotify, YouTube, or Apple Music.\n"
                  "• `/pause` & `/resume` — Control playback.\n"
                  "• `/skip` — Vote to skip the current track.\n"
                  "• `/stop` — Stop playback and disconnect the bot.",
            inline=False
        )
        embed_music.add_field(
            name="📜 Queue & Filters",
            value="• `/queue` — Display all upcoming tracks.\n"
                  "• `/volume <1-100>` — Adjust audio volume.\n"
                  "• `/filter <bassboost / nightcore / 8D>` — Apply audio effects.\n"
                  "• `/nowplaying` — View the current song information.",
            inline=False
        )
        embed_music.set_footer(text="Join a voice channel before requesting songs!")
        await music_ch.send(embed=embed_music)
        print("  + Sent Audio Guide to #music-requests", flush=True)

    # 3. Post COD Intelligence Guide in #loadouts-and-meta
    loadout_ch = discord.utils.get(guild.text_channels, name="loadouts-and-meta")
    if loadout_ch:
        try:
            await loadout_ch.purge(limit=10)
        except:
            pass

        embed_cod = discord.Embed(
            title="🔫 WARZONE INTELLIGENCE & LOADOUT COMMANDS",
            description="Leverage **Warzone Loadout Bot** & **CODBot** to look up meta weapon tunings and player stats!\n",
            color=discord.Color.from_rgb(52, 73, 94)
        )
        embed_cod.add_field(
            name="🛠️ Weapon & Meta Builds",
            value="• `/meta` — View top tier long-range & close-range meta weapons.\n"
                  "• `/gun <weapon_name>` — Inspect attachments, tuning, and recoil control stats.\n"
                  "• `/perks` — View recommended competitive perk packages.",
            inline=False
        )
        embed_cod.add_field(
            name="📊 Player & Lobby Stats",
            value="• `/stats <activision_id>` — Look up Warzone K/D, win rate, and match history.\n"
                  "• `/map` — Current Warzone map rotation schedules.",
            inline=False
        )
        sent = await loadout_ch.send(embed=embed_cod)
        try:
            await sent.pin()
        except:
            pass
        print("  + Sent Warzone Intelligence Guide to #loadouts-and-meta", flush=True)

    print(f"\n✨ All bot feature configurations and master guides successfully deployed!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
