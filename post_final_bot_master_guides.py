import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    # 1. Update #bot-commands with Complete Multi-Bot Cheat Sheet
    bot_ch = discord.utils.get(guild.text_channels, name="bot-commands")
    if bot_ch:
        try:
            await bot_ch.purge(limit=10)
        except:
            pass

        embed = discord.Embed(
            title="🤖 APEX UNIVERSE — MASTER BOT UTILITIES DIRECTORY",
            description="The server runs a **multi-layered, zero-conflict bot ecosystem**! Below is your command guide for all community utilities:\n",
            color=discord.Color.from_rgb(52, 152, 219)
        )
        embed.add_field(
            name="⭐ 1. MEE6 (XP & Progression Leaderboard)",
            value="• `!rank` — Inspect your chat level, progress bar, and card.\n"
                  "• `!levels` — View the top server activity leaderboard.",
            inline=False
        )
        embed.add_field(
            name="🐢 2. Carl-Bot (Tags & Community Starboard)",
            value="• `!tag <name>` — Fetch server quick-guides and tactical weapon tags.\n"
                  "• React with 5 ⭐ on any message to pin it to <#clips-and-highlights>!",
            inline=False
        )
        embed.add_field(
            name="🐺 3. Dyno Bot (Staff Hammer & Utilities)",
            value="• `?whois @user` — View account creation & join date.\n"
                  "• `?afk <reason>` — Set an AFK status notice for mentions.\n"
                  "• `?remindme <time> <task>` — Set private task reminders.",
            inline=False
        )
        embed.add_field(
            name="🎮 4. Tatsu (RPG Profiles & Squad Honor)",
            value="• `t!profile` — Inspect your RPG player card & level badge.\n"
                  "• `t!rep @user` — Award squad honor/reputation to a clutch teammate.\n"
                  "• Play mini-games (`t!daily`, `t!slots`) in <#mini-games>.",
            inline=False
        )
        embed.set_footer(text="Keep all bot commands restricted to #bot-commands & #mini-games")
        await bot_ch.send(embed=embed)
        print("  + Refreshed #bot-commands guide", flush=True)

    # 2. Update #staff-chat with Staff Moderation Cheat Sheet
    staff_ch = discord.utils.get(guild.text_channels, name="staff-chat")
    if staff_ch:
        staff_embed = discord.Embed(
            title="🛡️ STAFF BOT MODERATION COMMAND CHEAT SHEET",
            description="Staff tools for **Dyno**, **Carl-bot**, **Wick**, and **APEX PREDATOR**:\n",
            color=discord.Color.red()
        )
        staff_embed.add_field(
            name="🐺 Dyno Moderation Commands",
            value="• `?warn @user <reason>` — Issue a formal warning.\n"
                  "• `?mute @user <time> <reason>` — Timed mute.\n"
                  "• `?kick @user <reason>` / `?ban @user <reason>`\n"
                  "• `?lock` & `?unlock` — Emergency channel lockdown.\n"
                  "• `?slowmode <seconds>` — Adjust channel slowmode.",
            inline=False
        )
        staff_embed.add_field(
            name="🐢 Carl-bot Logging Commands",
            value="• `!log channel #mod-logs` — Ensure moderation actions route to #mod-logs.\n"
                  "• `!log all #audit-logs` — Route audit events to #audit-logs.\n"
                  "• `!starboard channel #clips-and-highlights 5`",
            inline=False
        )
        staff_embed.add_field(
            name="🛡️ Wick Anti-Nuke Commands",
            value="• `w!setup` — Review active anti-nuke & anti-raid modules.\n"
                  "• `w!whitelist add @APEX PREDATOR` — Whitelist core cloud bot.",
            inline=False
        )
        staff_embed.set_footer(text="Staff Operations Manual • Apex Universe")
        await staff_ch.send(embed=staff_embed)
        print("  + Sent Staff Moderation Cheat Sheet to #staff-chat", flush=True)

    print(f"\n✨ All master bot guides successfully deployed across channels!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
