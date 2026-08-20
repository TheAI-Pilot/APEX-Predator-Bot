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

INCENTIVE_ROLES = [
    {"name": "🔥 Daily Grinder", "color": 0xE67E22, "hoist": False},
    {"name": "💎 Community Elite", "color": 0x9B59B6, "hoist": False},
    {"name": "🎬 Clip Creator", "color": 0x1ABC9C, "hoist": False},
    {"name": "🌟 Highlight MVP", "color": 0xF1C40F, "hoist": False},
    {"name": "⚔️ Scrim Contender", "color": 0xE74C3C, "hoist": False}
]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    existing_roles = {r.name.lower(): r for r in guild.roles}

    for r_def in INCENTIVE_ROLES:
        r_name = r_def["name"]
        if r_name.lower() not in existing_roles:
            try:
                role = await guild.create_role(
                    name=r_name,
                    color=discord.Color(r_def["color"]),
                    hoist=r_def["hoist"],
                    reason="Incentive & Activity Role Creation"
                )
                print(f"  + [CREATED ROLE] @{role.name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error creating @{r_name}: {e}", flush=True)
        else:
            print(f"  [EXISTS] @{r_name}", flush=True)

    print(f"\n✨ All activity & incentive roles successfully verified on {guild.name}!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
