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

TARGET_CATEGORIES = [
    "🎯 VALORANT",
    "🔺 APEX LEGENDS",
    "📱 MOBILE GAMING",
    "VALORANT",
    "APEX LEGENDS",
    "MOBILE GAMING"
]

TARGET_ROLES = [
    "Valorant Player",
    "Apex Player",
    "Mobile Player"
]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    print(f"\n🗑️ Deleting categories and channels for: VALORANT, APEX LEGENDS, MOBILE GAMING\n", flush=True)

    # 1. Delete Channels & Categories
    for cat in list(guild.categories):
        # Check if category matches
        if any(t.lower() in cat.name.lower() for t in ["valorant", "apex legends", "mobile gaming"]):
            print(f"📂 Deleting Category: [{cat.name}]", flush=True)
            for ch in list(cat.channels):
                try:
                    await ch.delete()
                    print(f"  - Deleted Channel: #{ch.name}", flush=True)
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"  - Error deleting #{ch.name}: {e}", flush=True)

            try:
                await cat.delete()
                print(f"  - Deleted Category: [{cat.name}]", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error deleting category [{cat.name}]: {e}", flush=True)

    # 2. Delete the secondary game roles to keep role list clean
    print(f"\n🏷️ Cleaning up secondary game roles...", flush=True)
    for r_name in TARGET_ROLES:
        role = discord.utils.get(guild.roles, name=r_name)
        if role and not role.managed:
            try:
                await role.delete()
                print(f"  - Deleted role: @{r_name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Could not delete role @{r_name}: {e}", flush=True)

    print(f"\n✨ Selected categories and channels successfully deleted!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
