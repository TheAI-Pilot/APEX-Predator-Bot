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

    pred_ch = discord.utils.get(guild.text_channels, name="predator-chat")
    if pred_ch:
        print("  + #predator-chat verified and ready in [STAFF ONLY]", flush=True)
    else:
        print("  - #predator-chat not found")

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
