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

    # Roles
    everyone = guild.default_role
    verified_role = discord.utils.get(guild.roles, name="🪖 Verified Operator") or discord.utils.get(guild.roles, name="Verified Member")
    warzone_role = discord.utils.get(guild.roles, name="🔫 Warzone Slayer") or discord.utils.get(guild.roles, name="Warzone Player")
    admin_role = discord.utils.get(guild.roles, name="👑 High Command") or discord.utils.get(guild.roles, name="Admin")
    head_admin_role = discord.utils.get(guild.roles, name="⭐ Task Force Director") or discord.utils.get(guild.roles, name="Head Admin")
    mod_role = discord.utils.get(guild.roles, name="🛡️ Tactical Enforcer") or discord.utils.get(guild.roles, name="Moderator")
    quarantine_role = discord.utils.get(guild.roles, name="⛓️ Gulag Inmate") or discord.utils.get(guild.roles, name="Quarantine")

    print(f"\n=======================================================", flush=True)
    print(f"🔒 SYNCHRONIZING ACCURATE PERMISSION MATRIX ON {guild.name}", flush=True)
    print(f"=======================================================\n", flush=True)

    for cat in guild.categories:
        cat_name = cat.name.upper()

        if "START HERE" in cat_name:
            # Visible to everyone, read-only
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=True, read_message_history=True),
                quarantine_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False) if quarantine_role else None
            }
            if verified_role:
                overwrites[verified_role] = discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=True, read_message_history=True)

            overwrites = {k: v for k, v in overwrites.items() if k is not None and v is not None}
            await cat.edit(overwrites=overwrites)
            print(f"  [START HERE] Configured @everyone=READ_ONLY", flush=True)

            # Sync children
            for ch in cat.channels:
                await ch.edit(sync_permissions=True)
                await asyncio.sleep(0.2)

        elif "STAFF ONLY" in cat_name:
            # Hidden from everyone, visible only to staff
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=False)
            }
            if admin_role: overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
            if head_admin_role: overwrites[head_admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
            if mod_role: overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)

            await cat.edit(overwrites=overwrites)
            print(f"  [STAFF ONLY] Configured Private to Staff", flush=True)

            for ch in cat.channels:
                await ch.edit(sync_permissions=True)
                await asyncio.sleep(0.2)

        else:
            # COMMUNITY HUB, WARZONE, EVENTS, STREAMS, BOT COMMANDS
            # Hidden from unverified @everyone, unlocked for @Verified Operator
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=False)
            }
            if verified_role:
                overwrites[verified_role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True,
                    read_message_history=True,
                    connect=True,
                    speak=True
                )
            if warzone_role:
                overwrites[warzone_role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True,
                    read_message_history=True,
                    connect=True,
                    speak=True
                )
            if admin_role: overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
            if head_admin_role: overwrites[head_admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
            if mod_role: overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
            if quarantine_role: overwrites[quarantine_role] = discord.PermissionOverwrite(send_messages=False, speak=False, add_reactions=False)

            overwrites = {k: v for k, v in overwrites.items() if k is not None and v is not None}
            await cat.edit(overwrites=overwrites)
            print(f"  [{cat.name}] Configured Gated to @Verified Operator", flush=True)

            for ch in cat.channels:
                # Special rule: Comms channels voice text chat disabled
                if "comms" in ch.name.lower() and isinstance(ch, discord.VoiceChannel):
                    ch_overwrites = dict(cat.overwrites)
                    ch_overwrites[everyone] = discord.PermissionOverwrite(send_messages=False, view_channel=False)
                    if verified_role:
                        ch_overwrites[verified_role] = discord.PermissionOverwrite(view_channel=True, send_messages=False, connect=True, speak=True)
                    await ch.edit(overwrites=ch_overwrites)
                else:
                    await ch.edit(sync_permissions=True)
                await asyncio.sleep(0.2)

    print(f"\n✨ All permissions fully synchronized! Unverified members now only see START HERE until verified!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
