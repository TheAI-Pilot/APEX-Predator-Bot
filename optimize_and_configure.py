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

CATEGORY_ORDER = [
    "🚪 START HERE",
    "📊 SERVER STATS",
    "💬 COMMUNITY HUB",
    "🔫 WARZONE",
    "🏆 EVENTS & TOURNAMENTS",
    "🎥 STREAMS & CONTENT",
    "🤖 BOT COMMANDS & UTILS",
    "🛡️ STAFF ONLY"
]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    # Ensure general-chat allows @everyone so Discord Community check passes
    general_ch = discord.utils.get(guild.text_channels, name="general-chat")
    if general_ch:
        await general_ch.set_permissions(guild.default_role, view_channel=True, send_messages=True)
        print("  [ENABLED] @everyone send messages in #general-chat for Community Onboarding", flush=True)

    start_here_cat = discord.utils.get(guild.categories, name="🚪 START HERE")
    if not start_here_cat:
        start_here_cat = await guild.create_category("🚪 START HERE")

    # Handle Rules
    all_rules = [c for c in guild.text_channels if c.name == "rules"]
    if len(all_rules) > 1:
        # Move the community channel into START HERE and delete the duplicate
        for r_ch in all_rules:
            if r_ch.category is None:
                await r_ch.edit(category=start_here_cat)
                print(f"  [MOVED] #{r_ch.name} (Community) into [🚪 START HERE]", flush=True)
            else:
                try:
                    await r_ch.delete()
                    print(f"  [DELETED] Duplicate #{r_ch.name}", flush=True)
                except Exception as e:
                    print(f"  [CANNOT DELETE] #{r_ch.name}: {e}", flush=True)
    elif len(all_rules) == 1:
        await all_rules[0].edit(category=start_here_cat)

    # Handle Announcements
    all_announcements = [c for c in guild.text_channels if c.name == "announcements"]
    if len(all_announcements) > 1:
        for a_ch in all_announcements:
            if a_ch.category is None:
                await a_ch.edit(category=start_here_cat)
                print(f"  [MOVED] #{a_ch.name} (Community) into [🚪 START HERE]", flush=True)
            else:
                try:
                    await a_ch.delete()
                    print(f"  [DELETED] Duplicate #{a_ch.name}", flush=True)
                except Exception as e:
                    print(f"  [CANNOT DELETE] #{a_ch.name}: {e}", flush=True)
    elif len(all_announcements) == 1:
        await all_announcements[0].edit(category=start_here_cat)

    # 2. Reorder Categories
    print("\nReordering Categories (START HERE at Top, STAFF ONLY at Bottom)...", flush=True)
    for idx, cat_name in enumerate(CATEGORY_ORDER):
        cat = discord.utils.get(guild.categories, name=cat_name)
        if cat:
            try:
                await cat.edit(position=idx)
                print(f"  Position [{idx}]: Category {cat.name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  Error moving [{cat_name}]: {e}", flush=True)

    # 3. Warzone Voice Limits to 4
    print("\nSetting Warzone Voice Limits to exactly 4...", flush=True)
    wz_cat = discord.utils.get(guild.categories, name="🔫 WARZONE")
    if wz_cat:
        for v_ch in wz_cat.voice_channels:
            try:
                overwrites = v_ch.overwrites
                if "comms" in v_ch.name.lower():
                    overwrites[guild.default_role] = discord.PermissionOverwrite(send_messages=False)
                await v_ch.edit(user_limit=4, overwrites=overwrites)
                print(f"  [VOICE LIMIT: 4] 🔊 {v_ch.name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  Error setting limit on {v_ch.name}: {e}", flush=True)

    # 4. Clean rules embed in #rules
    rules_ch = discord.utils.get(guild.text_channels, name="rules")
    if rules_ch:
        try:
            await rules_ch.purge(limit=10)
        except:
            pass

        rules_embed = discord.Embed(
            title="📜 APEX UNIVERSE — OFFICIAL SERVER RULES",
            description="Welcome to **Apex Universe**! Please review and follow our community standards.\n",
            color=discord.Color.from_rgb(26, 188, 156)
        )
        rules_embed.add_field(
            name="1️⃣ Respect & Professional Conduct",
            value="Treat all members with respect. Zero tolerance for harassment, toxicity, or hate speech.",
            inline=False
        )
        rules_embed.add_field(
            name="2️⃣ Zero Tolerance for Cheating",
            value="Using hacks, wallhacks, scripts, strike-packs, or cronus results in an immediate permanent ban.",
            inline=False
        )
        rules_embed.add_field(
            name="3️⃣ Clean Comms & No Spam",
            value="No mic spam or ear-rape in squad comms. Keep comms clear during ranked lobbies.",
            inline=False
        )
        rules_embed.add_field(
            name="4️⃣ Controlled Self-Promotion",
            value="No unapproved Discord server invites. Post streams and YouTube videos in `#self-promo`.",
            inline=False
        )
        rules_embed.set_footer(text="Apex Universe Administration • Enforced by Moderation Team")
        await rules_ch.send(embed=rules_embed)
        print("  + Refreshed rules embed in #rules", flush=True)

    print("\n✨ Optimization complete!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
