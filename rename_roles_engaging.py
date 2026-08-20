import os
import sys
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

client = discord.Client(intents=intents)

# Engaging Tactical Warzone Role Names
ENGAGING_ROLES_MAP = {
    "Admin": {
        "new_name": "👑 High Command",
        "color": 0x1ABC9C
    },
    "Head Admin": {
        "new_name": "⭐ Task Force Director",
        "color": 0xE74C3C
    },
    "Moderator": {
        "new_name": "🛡️ Tactical Enforcer",
        "color": 0x9B59B6
    },
    "Helper / Coach": {
        "new_name": "🎯 Combat Advisor",
        "color": 0x3498DB
    },
    "OG / Founder": {
        "new_name": "🔱 Warzone Veteran",
        "color": 0xF1C40F
    },
    "Tournament Participant": {
        "new_name": "⚔️ Tournament Contender",
        "color": 0xE67E22
    },
    "Event Winner": {
        "new_name": "🏆 Warzone Champion",
        "color": 0xF39C12
    },
    "Verified Member": {
        "new_name": "🪖 Verified Operator",
        "color": 0x2ECC71
    },
    "Warzone Player": {
        "new_name": "🔫 Warzone Slayer",
        "color": 0x34495E
    },
    "Quarantine": {
        "new_name": "⛓️ Gulag Inmate",
        "color": 0x7F8C8D
    }
}

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    print(f"\n=======================================================", flush=True)
    print(f"🎖️ RENAMING ROLES TO ENGAGING WARZONE THEMED NAMES", flush=True)
    print(f"=======================================================\n", flush=True)

    for old_name, data in ENGAGING_ROLES_MAP.items():
        role = discord.utils.get(guild.roles, name=old_name)
        
        # If not found with exact old name, check if already partially renamed
        if not role:
            for r in guild.roles:
                if old_name.lower() in r.name.lower() or data["new_name"].lower() == r.name.lower():
                    role = r
                    break

        if role:
            if role.managed:
                print(f"  [SKIPPED BOT ROLE] @{role.name}", flush=True)
                continue
            try:
                await role.edit(
                    name=data["new_name"],
                    color=discord.Color(data["color"]),
                    reason="Engaging Warzone theme rebranding"
                )
                print(f"  [RENAMED] @{old_name} ➔ @{data['new_name']}", flush=True)
                await asyncio.sleep(0.4)
            except Exception as e:
                print(f"  [ERROR RENAMING] @{old_name}: {e}", flush=True)
        else:
            # Create if missing
            try:
                new_role = await guild.create_role(
                    name=data["new_name"],
                    color=discord.Color(data["color"]),
                    hoist=True,
                    reason="Engaging Warzone theme rebranding"
                )
                print(f"  [CREATED NEW] @{data['new_name']}", flush=True)
                await asyncio.sleep(0.4)
            except Exception as e:
                print(f"  [ERROR CREATING] @{data['new_name']}: {e}", flush=True)

    # Refresh #roles embed to showcase the new engaging names!
    roles_ch = discord.utils.get(guild.text_channels, name="roles")
    if roles_ch:
        try:
            await roles_ch.purge(limit=10)
        except:
            pass

        roles_embed = discord.Embed(
            title="🏷️ TASK FORCE ROSTER & SPECIALIZATIONS",
            description="Equip your callsigns and claim your status within **Apex Universe**!\n\n"
                        "### 🎖️ Tactical Hierarchy & Ranks:\n"
                        "• **👑 High Command** — Server Leadership & Full Admin\n"
                        "• **⭐ Task Force Director** — Operations & Head Administration\n"
                        "• **🛡️ Tactical Enforcer** — Server Security & Rules Enforcement\n"
                        "• **🎯 Combat Advisor** — Community Mentors & Squad Strategy\n\n"
                        "### 🏆 Prestigious & Community Badges:\n"
                        "• **🔱 Warzone Veteran** — Core OG supporters and pioneers\n"
                        "• **🏆 Warzone Champion** — Tournament & Kill-Race winners\n"
                        "• **⚔️ Tournament Contender** — Active competitive scrim players\n"
                        "• **🪖 Verified Operator** — Unlocked standard member privileges\n"
                        "• **🔫 Warzone Slayer** — Drops into Urzikstan & Rebirth squad lobbies\n\n"
                        "### ⛓️ Moderation Tag:\n"
                        "• **⛓️ Gulag Inmate** — Quarantined / Muted rulebreakers\n",
            color=discord.Color.from_rgb(26, 188, 156)
        )
        roles_embed.set_footer(text="Apex Universe • Select your roles in #verify-here and reaction menus")
        await roles_ch.send(embed=roles_embed)
        print("\n  + Refreshed #roles channel with engaging role hierarchy!", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"✨ ALL ROLES SUCCESSFULLY UPDATED & REBRANDED!", flush=True)
    print(f"=======================================================\n", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
