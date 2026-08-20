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

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    # Find Wick bot in guild
    wick_member = discord.utils.get(guild.members, name="Wick")
    if not wick_member:
        for m in guild.members:
            if "wick" in m.name.lower():
                wick_member = m
                break

    mod_logs = discord.utils.get(guild.text_channels, name="mod-logs")
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")

    if wick_member:
        embed = discord.Embed(
            title="🤖 BOT INTEGRATION & JOIN LOG",
            description=f"**Bot Name:** {wick_member.mention} (`{wick_member.name}`)\n"
                        f"**Bot ID:** `{wick_member.id}`\n"
                        f"**Role:** Anti-Nuke, Anti-Raid & Guild Security\n"
                        f"**Status:** Authorized & Verified\n"
                        f"**Joined At:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            color=discord.Color.purple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=wick_member.display_avatar.url)
        embed.set_footer(text="Security & Bot Integration Alert • Apex Predator Logger")

        if mod_logs:
            await mod_logs.send(embed=embed)
            print("  + Sent Wick Bot Join Log to #mod-logs", flush=True)
        if audit_logs:
            await audit_logs.send(embed=embed)
            print("  + Sent Wick Bot Join Log to #audit-logs", flush=True)
    else:
        print("  - Wick bot not found in member cache.")

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
