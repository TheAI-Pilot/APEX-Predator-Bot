import os
import sys
import json
import asyncio
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("Error: DISCORD_TOKEN not found in .env")
    sys.exit(1)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print(f"Connected to {len(client.guilds)} guild(s).\n")

    if len(client.guilds) == 0:
        print("=" * 60)
        print("⚠️ BOT IS NOT JOINED TO ANY GUILDS/SERVERS YET!")
        print("Please invite the bot to your server using this link:")
        print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot%20applications.commands")
        print("=" * 60)
        await client.close()
        return

    for guild in client.guilds:
        print("=" * 80)
        print(f"🏛️ SERVER: {guild.name} (ID: {guild.id})")
        print(f"👑 Owner: {guild.owner} (ID: {guild.owner_id})")
        print(f"👥 Member Count: {guild.member_count}")
        print(f"✨ Boost Tier: {guild.premium_tier} ({guild.premium_subscription_count} boosts)")
        print(f"🔒 Verification Level: {guild.verification_level}")
        print("=" * 80)

        # 1. Roles Hierarchy
        print("\n--- 🏷️ ROLES HIERARCHY (Top to Bottom) ---")
        sorted_roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        for r in sorted_roles:
            color_hex = f"#{r.color.value:06x}" if r.color.value else "Default"
            key_perms = []
            if r.permissions.administrator: key_perms.append("ADMINISTRATOR")
            if r.permissions.manage_guild: key_perms.append("MANAGE_SERVER")
            if r.permissions.manage_roles: key_perms.append("MANAGE_ROLES")
            if r.permissions.manage_channels: key_perms.append("MANAGE_CHANNELS")
            if r.permissions.ban_members: key_perms.append("BAN_MEMBERS")
            if r.permissions.kick_members: key_perms.append("KICK_MEMBERS")
            if r.permissions.moderate_members: key_perms.append("TIMEOUT_MEMBERS")
            if r.permissions.manage_messages: key_perms.append("MANAGE_MESSAGES")
            
            perms_str = f" [Perms: {', '.join(key_perms)}]" if key_perms else ""
            print(f"[{r.position:02d}] @{r.name:<25} | ID: {r.id:<20} | Color: {color_hex:<8} | Members: {len(r.members):<3}{perms_str}")

        # 2. Channels & Categories Tree
        print("\n--- 📁 CHANNELS & CATEGORIES TREE ---")
        
        # Channels without category
        no_cat_channels = [c for c in guild.channels if c.category is None and not isinstance(c, discord.CategoryChannel)]
        if no_cat_channels:
            print("📂 (No Category):")
            for c in sorted(no_cat_channels, key=lambda x: x.position):
                type_str = str(c.type).replace('_', ' ').upper()
                topic_str = f" - \"{c.topic}\"" if hasattr(c, 'topic') and c.topic else ""
                print(f"   ├── #{c.name} ({type_str}, ID: {c.id}){topic_str}")

        # Categories and their children
        for cat in sorted(guild.categories, key=lambda x: x.position):
            print(f"\n📂 CATEGORY: {cat.name.upper()} (ID: {cat.id})")
            channels = sorted(cat.channels, key=lambda x: x.position)
            for c in channels:
                type_str = str(c.type).replace('_', ' ').upper()
                topic_str = f" - \"{c.topic}\"" if hasattr(c, 'topic') and c.topic else ""
                print(f"   ├── #{c.name} ({type_str}, ID: {c.id}){topic_str}")

        print("\n" + "=" * 80 + "\n")

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
