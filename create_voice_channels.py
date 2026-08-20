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

VOICE_STRUCTURE = {
    "🔫 WARZONE": [
        {"name": "Warzone Lobby 1", "user_limit": 4},
        {"name": "Warzone Lobby 2", "user_limit": 4},
        {"name": "Warzone Lobby 3", "user_limit": 4},
        {"name": "Warzone Lobby 4", "user_limit": 4}
    ],
    "🎯 VALORANT": [
        {"name": "Valorant 1", "user_limit": 5},
        {"name": "Valorant 2", "user_limit": 5},
        {"name": "Valorant 3", "user_limit": 5},
        {"name": "Valorant 4", "user_limit": 5}
    ],
    "🔺 APEX LEGENDS": [
        {"name": "Apex 1", "user_limit": 3},
        {"name": "Apex 2", "user_limit": 3},
        {"name": "Apex 3", "user_limit": 3},
        {"name": "Apex 4", "user_limit": 3}
    ],
    "📱 MOBILE GAMING": [
        {"name": "Mobile Squad 1", "user_limit": 4},
        {"name": "Mobile Squad 2", "user_limit": 4},
        {"name": "Mobile Squad 3", "user_limit": 4},
        {"name": "Mobile Squad 4", "user_limit": 4}
    ],
    "📊 SERVER STATS": [
        {"name": "📊 Members: 70", "user_limit": 0}
    ]
}

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    for cat_name, v_channels in VOICE_STRUCTURE.items():
        cat = discord.utils.get(guild.categories, name=cat_name)
        if not cat:
            print(f"Category not found: {cat_name}", flush=True)
            continue

        for v_def in v_channels:
            v_name = v_def["name"]
            limit = v_def["user_limit"]

            existing = discord.utils.get(cat.voice_channels, name=v_name)
            if existing:
                print(f"  [EXISTS] 🔊 {v_name}", flush=True)
                continue

            try:
                ch = await guild.create_voice_channel(
                    name=v_name,
                    category=cat,
                    user_limit=limit
                )
                print(f"  [CREATED] 🔊 {ch.name} (limit: {limit}) in [{cat.name}]", flush=True)
                await asyncio.sleep(0.4)
            except Exception as e:
                print(f"  [ERROR] {v_name}: {e}", flush=True)

    print("\nAll voice channels created successfully!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
