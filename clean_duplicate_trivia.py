import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("AI_PILOT_TOKEN") or os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = discord.utils.get(client.guilds, id=1539332811276947537)
    if guild:
        trivia_ch = discord.utils.get(guild.text_channels, name="daily-ai-challenge")
        if trivia_ch:
            messages = [msg async for msg in trivia_ch.history(limit=10)]
            print(f"Found {len(messages)} recent messages in #daily-ai-challenge")
            seen_titles = set()
            for msg in messages:
                if msg.author.id == client.user.id and msg.embeds:
                    title = msg.embeds[0].title
                    if title in seen_titles:
                        print(f"Deleting duplicate message ID {msg.id} with title: {title}")
                        await msg.delete()
                    else:
                        seen_titles.add(title)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
