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

    # 1. Post Official Rules to #rules
    rules_ch = discord.utils.get(guild.text_channels, name="rules")
    if rules_ch:
        rules_embed = discord.Embed(
            title="📜 APEX UNIVERSE — OFFICIAL SERVER RULES",
            description="Welcome to **Apex Universe**! To maintain a competitive, fun, and respectful environment, all members must abide by the following community standards.\n",
            color=discord.Color.from_rgb(230, 126, 34)
        )
        rules_embed.add_field(
            name="1️⃣ Respect & Conduct",
            value="Treat all players with respect. Zero tolerance for harassment, hate speech, racism, sexism, or toxic bullying.",
            inline=False
        )
        rules_embed.add_field(
            name="2️⃣ No Cheating / Exploiting",
            value="Using hacks, cheats, scripts, engine exploits, or cronus/strike-packs will result in an immediate permanent ban.",
            inline=False
        )
        rules_embed.add_field(
            name="3️⃣ Channel Etiquette & LFG",
            value="Keep conversations relevant to the designated channels. Use `#looking-for-squad` and game lobbies for squad search.",
            inline=False
        )
        rules_embed.add_field(
            name="4️⃣ Controlled Self-Promotion",
            value="Do not spam streams, YouTube videos, or other Discord servers in general chats. Use `#self-promo` or `#content-creators`.",
            inline=False
        )
        rules_embed.add_field(
            name="5️⃣ Voice Channel Comms",
            value="No mic spam, soundboards in comms channels, ear-rape, or background screaming. Respect squad callouts.",
            inline=False
        )
        rules_embed.set_footer(text="Enforced by Apex Universe Staff Team • Break rules at your own risk")
        await rules_ch.send(embed=rules_embed)
        print("  + Sent rules embed to #rules", flush=True)

    # 2. Post LFG Format to #looking-for-squad
    lfg_ch = discord.utils.get(guild.text_channels, name="looking-for-squad")
    if lfg_ch:
        lfg_embed = discord.Embed(
            title="🎯 SQUAD SEARCH (LFG) GUIDELINES",
            description="Looking for teammates? Copy and paste the template below to find players quickly!\n",
            color=discord.Color.blue()
        )
        lfg_embed.add_field(
            name="📋 Standard LFG Template",
            value="```yaml\nGame: Warzone / Valorant / Apex / Mobile\nRegion: NA / EU / IN / ASIA\nSquad Size: Need 1 / Need 2\nMode / Rank: Ranked (Diamond+) / Casual\nMic Required: Yes / No\nGamertag: YourTag#1234\n```",
            inline=False
        )
        lfg_embed.add_field(
            name="💡 Pro-Tip",
            value="Hop into an empty **Warzone Lobby** or **Comms** voice channel and post the channel name in your message!",
            inline=False
        )
        msg = await lfg_ch.send(embed=lfg_embed)
        try:
            await msg.pin()
        except:
            pass
        print("  + Sent LFG template to #looking-for-squad", flush=True)

    # 3. Post Loadout Guide to #loadouts-and-meta
    loadout_ch = discord.utils.get(guild.text_channels, name="loadouts-and-meta")
    if loadout_ch:
        loadout_embed = discord.Embed(
            title="🔫 WARZONE META LOADOUT TEMPLATE",
            description="Share your top weapon builds and tuning with the community!\n",
            color=discord.Color.dark_grey()
        )
        loadout_embed.add_field(
            name="📝 Loadout Post Format",
            value="```yaml\nWeapon: [e.g. Superi 46 / KASTOV LSW]\nRole: Primary AR / Close-Range SMG / Sniper\nMuzzle: ...\nBarrel: ...\nOptic: ...\nUnderbarrel / Stock: ...\nMagazine: ...\nPerks: Double Time, Sleight of Hand, High Alert\n```",
            inline=False
        )
        loadout_embed.set_footer(text="Upload attachments screenshots alongside your build!")
        msg = await loadout_ch.send(embed=loadout_embed)
        try:
            await msg.pin()
        except:
            pass
        print("  + Sent Loadout guide to #loadouts-and-meta", flush=True)

    # 4. Post Verification Prompt to #verify-here
    verify_ch = discord.utils.get(guild.text_channels, name="verify-here")
    if verify_ch:
        verify_embed = discord.Embed(
            title="🛡️ APEX UNIVERSE MEMBER VERIFICATION",
            description="Welcome to **Apex Universe**!\n\nTo prevent raids and keep our community secure, please verify your account to unlock full channel access.\n\nClick the button below or react to gain the **Verified Member** role.",
            color=discord.Color.green()
        )
        verify_embed.set_footer(text="Apex Universe Verification System")
        await verify_ch.send(embed=verify_embed)
        print("  + Sent Verification prompt to #verify-here", flush=True)

    print("\nEmbed templates successfully deployed!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
