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
intents.members = True

client = discord.Client(intents=intents)

async def apply_server_blueprint(guild, blueprint):
    """
    Blueprint format:
    {
        "roles": [{"name": "Admin", "color": 0xFF0000, "permissions": ["administrator"]}],
        "categories": [
            {
                "name": "WELCOME & RULES",
                "channels": [{"name": "welcome", "type": "text", "topic": "Welcome channel"}]
            }
        ]
    }
    """
    print(f"Applying blueprint to guild: {guild.name}")
    
    # Process Roles
    created_roles = {}
    if "roles" in blueprint:
        for r_data in blueprint["roles"]:
            perms = discord.Permissions.none()
            if "administrator" in r_data.get("permissions", []):
                perms.administrator = True
            if "manage_guild" in r_data.get("permissions", []):
                perms.manage_guild = True
            if "manage_channels" in r_data.get("permissions", []):
                perms.manage_channels = True
            if "manage_messages" in r_data.get("permissions", []):
                perms.manage_messages = True

            role = await guild.create_role(
                name=r_data["name"],
                color=discord.Color(r_data.get("color", 0x99AAB5)),
                permissions=perms,
                hoist=r_data.get("hoist", True)
            )
            created_roles[r_data["name"]] = role
            print(f"  + Created Role: @{role.name}")

    # Process Categories & Channels
    if "categories" in blueprint:
        for cat_data in blueprint["categories"]:
            category = await guild.create_category(cat_data["name"])
            print(f"  + Created Category: [{category.name}]")

            for ch_data in cat_data.get("channels", []):
                ch_type = ch_data.get("type", "text")
                if ch_type == "text":
                    ch = await guild.create_text_channel(
                        name=ch_data["name"],
                        category=category,
                        topic=ch_data.get("topic")
                    )
                elif ch_type == "voice":
                    ch = await guild.create_voice_channel(
                        name=ch_data["name"],
                        category=category
                    )
                print(f"    - Created Channel: #{ch.name} ({ch_type})")

    print("\nBlueprint successfully applied!")

@client.event
async def on_ready():
    print(f"Connected as {client.user}")
    if not client.guilds:
        print("Bot is not in any server. Please invite it first.")
        await client.close()
        return

    # To be called when user specifies blueprint
    await client.close()

if __name__ == "__main__":
    if not TOKEN:
        print("Missing DISCORD_TOKEN in .env")
        sys.exit(1)
    client.run(TOKEN)
