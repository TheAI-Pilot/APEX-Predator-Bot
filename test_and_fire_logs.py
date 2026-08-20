import os
import sys
import asyncio
import datetime
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    mod_logs = discord.utils.get(guild.text_channels, name="mod-logs")
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")

    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # 1. Post Activation in #mod-logs
    if mod_logs:
        mod_embed = discord.Embed(
            title="🛡️ MODERATION LOG ENGINE ONLINE",
            description="**Status:** Active & Monitoring\n"
                        "**Logging Events:** Member Joins, Bot Additions, Kicks, Bans, Timeouts, Channel Locks, Purges.\n"
                        "**Monitoring Engine:** APEX PREDATOR Cloud Core",
            color=discord.Color.from_rgb(231, 76, 60),
            timestamp=now_utc
        )
        mod_embed.set_footer(text="Apex Predator Moderation Core")
        await mod_logs.send(embed=mod_embed)
        print("  + Fired live initialization embed to #mod-logs", flush=True)

    # 2. Post Activation in #audit-logs
    if audit_logs:
        audit_embed = discord.Embed(
            title="📋 AUDIT LOG FEED ONLINE",
            description="**Status:** Active & Monitoring\n"
                        "**Logging Events:** Deleted Messages, Edited Messages, Role Updates, Channel Changes, Member Joins/Leaves, Server Boosts.\n"
                        "**Monitoring Engine:** APEX PREDATOR Cloud Core",
            color=discord.Color.from_rgb(52, 152, 219),
            timestamp=now_utc
        )
        audit_embed.set_footer(text="Apex Predator Audit Logger")
        await audit_logs.send(embed=audit_embed)
        print("  + Fired live initialization embed to #audit-logs", flush=True)

    # 3. Log all currently installed bots into #mod-logs
    bot_members = [m for m in guild.members if m.bot]
    if mod_logs and bot_members:
        bot_list_str = "\n".join([f"• {b.mention} (`{b.name}`) — ID: `{b.id}`" for b in bot_members])
        bots_embed = discord.Embed(
            title="🤖 CURRENT AUTHORIZED SERVER BOTS ROSTER",
            description=f"The following **{len(bot_members)} bots** are authorized and monitoring **{guild.name}**:\n\n{bot_list_str}",
            color=discord.Color.purple(),
            timestamp=now_utc
        )
        await mod_logs.send(embed=bots_embed)
        print("  + Sent Authorized Bots Roster to #mod-logs", flush=True)

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
