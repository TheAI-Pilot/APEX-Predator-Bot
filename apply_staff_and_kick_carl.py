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

CARL_BOT_ID = 235148962103951360

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    # 1. Kick Carl-bot
    carl_member = guild.get_member(CARL_BOT_ID)
    if carl_member:
        try:
            await carl_member.kick(reason="Server optimization: removed redundant command bot")
            print("  [KICKED] Carl-bot removed from the server.", flush=True)
        except Exception as e:
            print(f"  [ERROR KICKING CARL] {e}", flush=True)
    else:
        print("  [CARL-BOT NOT IN SERVER]", flush=True)

    # 2. Check and assign Tactical Enforcer role
    mod_role = discord.utils.get(guild.roles, name="🛡️ Tactical Enforcer")
    head_admin_role = discord.utils.get(guild.roles, name="⭐ Task Force Director")

    print(f"\n🏷️ Roles: Mod Role = {mod_role}, Head Admin = {head_admin_role}")

    # Let's ensure server owner has full roles
    owner = guild.get_member(guild.owner_id)
    if owner:
        roles_to_give = [r for r in [mod_role, head_admin_role] if r and r not in owner.roles]
        if roles_to_give:
            try:
                await owner.add_roles(*roles_to_give, reason="Owner Staff Roles")
                print(f"  + Added staff roles to owner {owner.name}", flush=True)
            except Exception as e:
                print(f"  - Could not add roles to owner: {e}", flush=True)

    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
