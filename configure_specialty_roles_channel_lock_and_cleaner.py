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

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.guilds[0] # Apex Universe
    print(f"Securing channel permissions in {guild.name}...", flush=True)

    roles_ch = None
    for c in guild.text_channels:
        if "role" in c.name.lower() or "specialty" in c.name.lower():
            roles_ch = c
            break

    if roles_ch:
        # Lock channel so users can ONLY click buttons and cannot type chatter
        await roles_ch.set_permissions(guild.default_role, 
                                       view_channel=True, 
                                       read_messages=True, 
                                       read_message_history=True, 
                                       send_messages=False, 
                                       send_messages_in_threads=False,
                                       create_public_threads=False,
                                       create_private_threads=False,
                                       add_reactions=False)
        print(f"🔒 Locked #{roles_ch.name} (View & Click Buttons only).", flush=True)

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
