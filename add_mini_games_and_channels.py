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

    comm_cat = discord.utils.get(guild.categories, name="💬 COMMUNITY HUB")
    if comm_cat:
        if not discord.utils.get(comm_cat.text_channels, name="mini-games"):
            try:
                mg_ch = await guild.create_text_channel(
                    name="mini-games",
                    category=comm_cat,
                    topic="Tatsu Economy (t!profile, t!daily, t!slots) & TriviaBot Gaming Arenas (trivia start)"
                )
                mg_embed = discord.Embed(
                    title="🎮 COMMUNITY MINI-GAMES & TRIVIA ARENA",
                    description="Welcome to the **Apex Universe Gaming Arena**! Relax between Warzone matches with RPG profiles, economy games, and gaming trivia.\n",
                    color=discord.Color.from_rgb(155, 89, 182)
                )
                mg_embed.add_field(
                    name="🎲 Tatsu Economy & Profile",
                    value="• `t!profile` — View your RPG player card & level badge.\n"
                          "• `t!daily` — Claim your daily coin reward.\n"
                          "• `t!slots` & `t!gamble <amount>` — Play economy mini-games.\n"
                          "• `t!rep @user` — Award squad reputation to a teammate!",
                    inline=False
                )
                mg_embed.add_field(
                    name="🧠 TriviaBot Competitions",
                    value="• `trivia start gaming` — Start a multiplayer video game quiz tournament.\n"
                          "• `trivia categories` — View available trivia topics.\n"
                          "• `trivia stats` — Check server leaderboard & high scores.",
                    inline=False
                )
                mg_embed.set_footer(text="Keep all bot gaming and economy spam in #mini-games!")
                await mg_ch.send(embed=mg_embed)
                print("  + Created and Populated #mini-games in [COMMUNITY HUB]", flush=True)
            except Exception as e:
                print(f"  - Error creating #mini-games: {e}", flush=True)
        else:
            print("  #mini-games already exists.")

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
