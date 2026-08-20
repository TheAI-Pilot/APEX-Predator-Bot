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
intents.members = True

client = discord.Client(intents=intents)

# Target Role Blueprint
ROLE_BLUEPRINT = [
    {"name": "Head Admin", "color": 0xE74C3C, "hoist": True, "perms": {"administrator": True}},
    {"name": "Admin", "color": 0x1ABC9C, "hoist": True, "perms": {"manage_guild": True, "manage_roles": True, "manage_channels": True, "ban_members": True, "kick_members": True, "manage_messages": True, "manage_webhooks": True}},
    {"name": "Moderator", "color": 0x9B59B6, "hoist": True, "perms": {"ban_members": True, "kick_members": True, "moderate_members": True, "manage_messages": True, "manage_threads": True, "mute_members": True, "deafen_members": True, "move_members": True}},
    {"name": "Helper / Coach", "color": 0x3498DB, "hoist": True, "perms": {"manage_threads": True, "attach_files": True, "embed_links": True}},
    {"name": "OG / Founder", "color": 0xF1C40F, "hoist": True, "perms": {}},
    {"name": "Tournament Participant", "color": 0xE67E22, "hoist": True, "perms": {}},
    {"name": "Event Winner", "color": 0xF39C12, "hoist": True, "perms": {}},
    {"name": "Verified Member", "color": 0x2ECC71, "hoist": True, "perms": {}},
    {"name": "Warzone Player", "color": 0x34495E, "hoist": False, "perms": {}},
    {"name": "Valorant Player", "color": 0xFA4454, "hoist": False, "perms": {}},
    {"name": "Apex Player", "color": 0xDA292A, "hoist": False, "perms": {}},
    {"name": "Mobile Player", "color": 0x95A5A6, "hoist": False, "perms": {}},
    {"name": "Quarantine", "color": 0x7F8C8D, "hoist": False, "perms": {}}
]

# Target Category & Channel Structure
CATEGORY_BLUEPRINT = [
    {
        "name": "🛡️ STAFF ONLY",
        "staff_only": True,
        "channels": [
            {"name": "staff-chat", "type": "text", "topic": "Private discussions for server staff"},
            {"name": "mod-logs", "type": "text", "topic": "Automated moderation action logs"},
            {"name": "audit-logs", "type": "text", "topic": "Server audit trail for joins, leaves, and edits"},
            {"name": "ticket-logs", "type": "text", "topic": "Archived tickets and support transcripts"}
        ]
    },
    {
        "name": "🚪 START HERE",
        "read_only": True,
        "channels": [
            {"name": "welcome", "type": "text", "topic": "Welcome greeting and server intro"},
            {"name": "rules", "type": "text", "topic": "Official server rules and community standards"},
            {"name": "roles", "type": "text", "topic": "Self-assign your game and notification roles"},
            {"name": "announcements", "type": "text", "topic": "Major server announcements and tournaments"},
            {"name": "verify-here", "type": "text", "topic": "Click to verify and unlock full server access"}
        ]
    },
    {
        "name": "💬 COMMUNITY HUB",
        "channels": [
            {"name": "general-chat", "type": "text", "topic": "Main community conversation"},
            {"name": "warzone-chat", "type": "text", "topic": "General Warzone banter, updates, and memes"},
            {"name": "clips-and-highlights", "type": "text", "topic": "Share your best gaming clips and clutch moments"},
            {"name": "looking-for-squad", "type": "text", "topic": "Cross-game LFG. Format: Game | Region | Time | Rank | Mic"},
            {"name": "gamer-tags", "type": "text", "topic": "Share your Activision / Riot / PSN / Xbox IDs"},
            {"name": "self-promo", "type": "text", "topic": "Share your streams, YouTube videos, and content"},
            {"name": "memes-and-media", "type": "text", "topic": "Memes, screenshots, and funny gaming content"}
        ]
    },
    {
        "name": "🔫 WARZONE",
        "channels": [
            {"name": "warzone-lobby", "type": "text", "topic": "Primary LFG lobby for Call of Duty: Warzone squads"},
            {"name": "loadouts-and-meta", "type": "text", "topic": "Top tier weapon builds, meta attachments, and tuning"},
            {"name": "warzone-strats", "type": "text", "topic": "Rotation tactics, map guides, and game strategy"},
            {"name": "warzone-clips", "type": "text", "topic": "Warzone squad wipes, snipes, and highlights"},
            {"name": "warzone-events", "type": "text", "topic": "Custom Warzone tournaments and community scrims"},
            {"name": "Warzone Lobby 1", "type": "voice", "user_limit": 4},
            {"name": "Warzone Lobby 2", "type": "voice", "user_limit": 4},
            {"name": "Warzone Lobby 3", "type": "voice", "user_limit": 4},
            {"name": "Warzone Lobby 4", "type": "voice", "user_limit": 4},
            {"name": "Warzone Comms 1", "type": "voice", "user_limit": 4},
            {"name": "Warzone Comms 2", "type": "voice", "user_limit": 4},
            {"name": "Warzone Stage", "type": "stage"}
        ]
    },
    {
        "name": "🎯 VALORANT",
        "channels": [
            {"name": "valorant-lobby", "type": "text", "topic": "Valorant competitive & unrated LFG"},
            {"name": "valorant-strats", "type": "text", "topic": "Agent lineups, crosshair codes, and execute strats"},
            {"name": "valorant-clips", "type": "text", "topic": "Valorant aces and clutch plays"},
            {"name": "Valorant 1", "type": "voice", "user_limit": 5},
            {"name": "Valorant 2", "type": "voice", "user_limit": 5},
            {"name": "Valorant 3", "type": "voice", "user_limit": 5},
            {"name": "Valorant 4", "type": "voice", "user_limit": 5}
        ]
    },
    {
        "name": "🔺 APEX LEGENDS",
        "channels": [
            {"name": "apex-lobby", "type": "text", "topic": "Apex Legends Ranked & Trios LFG"},
            {"name": "apex-strats", "type": "text", "topic": "Legend combos, ring rotations, and weapon rankings"},
            {"name": "apex-clips", "type": "text", "topic": "Apex champion squad clips and squad wipes"},
            {"name": "Apex 1", "type": "voice", "user_limit": 3},
            {"name": "Apex 2", "type": "voice", "user_limit": 3},
            {"name": "Apex 3", "type": "voice", "user_limit": 3},
            {"name": "Apex 4", "type": "voice", "user_limit": 3}
        ]
    },
    {
        "name": "📱 MOBILE GAMING",
        "channels": [
            {"name": "mobile-lobby", "type": "text", "topic": "COD Mobile, Warzone Mobile & BGMI squad search"},
            {"name": "mobile-chat", "type": "text", "topic": "Mobile loadouts, sensitivity, and layout sharing"},
            {"name": "Mobile Squad 1", "type": "voice", "user_limit": 4},
            {"name": "Mobile Squad 2", "type": "voice", "user_limit": 4},
            {"name": "Mobile Squad 3", "type": "voice", "user_limit": 4},
            {"name": "Mobile Squad 4", "type": "voice", "user_limit": 4}
        ]
    },
    {
        "name": "🏆 EVENTS & TOURNAMENTS",
        "channels": [
            {"name": "events-hub", "type": "text", "topic": "Community tournaments calendar and general FAQs"},
            {"name": "tournaments", "type": "text", "topic": "Official tournament brackets, rules, and signups"},
            {"name": "custom-lobbies", "type": "text", "topic": "Custom match room codes, passwords, and schedules"},
            {"name": "Event Stage", "type": "stage"}
        ]
    },
    {
        "name": "🎥 STREAMS & CONTENT",
        "channels": [
            {"name": "stream-notifications", "type": "text", "topic": "Live Twitch and YouTube stream alerts"},
            {"name": "content-creators", "type": "text", "topic": "Verified creator showcase and socials"},
            {"name": "youtube-videos", "type": "text", "topic": "New video drops, guides, and montages"}
        ]
    },
    {
        "name": "🤖 BOT COMMANDS & UTILS",
        "channels": [
            {"name": "bot-commands", "type": "text", "topic": "Bot spam and slash command interactions"},
            {"name": "music-requests", "type": "text", "topic": "Song requests and queue management"},
            {"name": "ticket-support", "type": "text", "topic": "Open a support ticket for staff assistance"}
        ]
    },
    {
        "name": "📊 SERVER STATS",
        "channels": [
            {"name": "📊 Members: 70", "type": "voice", "user_limit": 0}
        ]
    }
]

async def rebuild_server(guild):
    print(f"\n=======================================================", flush=True)
    print(f"🚀 STARTING RECONSTRUCTION FOR: {guild.name} (ID: {guild.id})", flush=True)
    print(f"=======================================================\n", flush=True)

    # 1. Sync Roles
    print("--- 🏷️ 1. REBUILDING ROLE HIERARCHY ---", flush=True)
    existing_roles = {r.name.lower(): r for r in guild.roles}
    created_roles = {}

    for r_def in ROLE_BLUEPRINT:
        r_name = r_def["name"]
        perms = discord.Permissions.none()
        for p_name, p_val in r_def["perms"].items():
            if hasattr(perms, p_name):
                setattr(perms, p_name, p_val)

        if r_name.lower() in existing_roles:
            role = existing_roles[r_name.lower()]
            try:
                await role.edit(
                    color=discord.Color(r_def["color"]),
                    hoist=r_def["hoist"],
                    permissions=perms
                )
                print(f"  [UPDATED] @{role.name}", flush=True)
                created_roles[r_name] = role
            except Exception as e:
                print(f"  [ERROR UPDATING] @{r_name}: {e}", flush=True)
                created_roles[r_name] = role
        else:
            try:
                role = await guild.create_role(
                    name=r_name,
                    color=discord.Color(r_def["color"]),
                    hoist=r_def["hoist"],
                    permissions=perms
                )
                print(f"  [CREATED] @{role.name}", flush=True)
                created_roles[r_name] = role
            except Exception as e:
                print(f"  [ERROR CREATING] @{r_name}: {e}", flush=True)

    admin_role = created_roles.get("Admin") or discord.utils.get(guild.roles, name="Admin")
    mod_role = created_roles.get("Moderator") or discord.utils.get(guild.roles, name="Moderator")

    # 2. Reconstruct Categories & Channels
    print("\n--- 📁 2. REBUILDING CATEGORIES & CHANNELS ---", flush=True)

    for cat_def in CATEGORY_BLUEPRINT:
        cat_name = cat_def["name"]
        
        # Check if category exists
        cat = discord.utils.get(guild.categories, name=cat_name)
        
        # Determine Category Permissions
        overwrites = {}
        if cat_def.get("staff_only"):
            overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
            if admin_role:
                overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True)
        elif cat_def.get("read_only"):
            overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=True)
            if admin_role:
                overwrites[admin_role] = discord.PermissionOverwrite(send_messages=True)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(send_messages=True)

        if not cat:
            try:
                cat = await guild.create_category(cat_name, overwrites=overwrites)
                print(f"\n📂 [CREATED CATEGORY] {cat.name}", flush=True)
            except Exception as e:
                print(f"\n📂 [ERROR CATEGORY] {cat_name}: {e}", flush=True)
                continue
        else:
            print(f"\n📂 [EXISTING CATEGORY] {cat.name}", flush=True)
            if overwrites:
                try:
                    await cat.edit(overwrites=overwrites)
                except:
                    pass

        # Create Channels inside Category
        for ch_def in cat_def.get("channels", []):
            ch_name = ch_def["name"]
            ch_type = ch_def.get("type", "text")
            ch_topic = ch_def.get("topic", "")

            # Check if channel exists under this category or globally
            existing_ch = discord.utils.get(cat.channels, name=ch_name.lower()) or discord.utils.get(guild.channels, name=ch_name.lower())

            if existing_ch and existing_ch.category != cat:
                try:
                    await existing_ch.edit(category=cat)
                    print(f"   ├── [MOVED] #{existing_ch.name} -> {cat.name}", flush=True)
                    continue
                except:
                    pass

            if existing_ch:
                print(f"   ├── [EXISTS] #{existing_ch.name}", flush=True)
                continue

            try:
                if ch_type == "text":
                    new_ch = await guild.create_text_channel(
                        name=ch_name,
                        category=cat,
                        topic=ch_topic
                    )
                    print(f"   ├── [CREATED TEXT] #{new_ch.name}", flush=True)
                elif ch_type == "voice":
                    user_limit = ch_def.get("user_limit", 0)
                    new_ch = await guild.create_voice_channel(
                        name=ch_name,
                        category=cat,
                        user_limit=user_limit
                    )
                    print(f"   ├── [CREATED VOICE] 🔊 {new_ch.name} (limit: {user_limit})", flush=True)
                elif ch_type == "stage":
                    new_ch = await guild.create_stage_channel(
                        name=ch_name,
                        category=cat,
                        topic=ch_topic
                    )
                    print(f"   ├── [CREATED STAGE] 🎙️ {new_ch.name}", flush=True)
            except Exception as e:
                print(f"   ├── [ERROR CHANNEL] {ch_name}: {e}", flush=True)

        await asyncio.sleep(1) # slight cooldown to prevent rate limiting

    print("\n=======================================================", flush=True)
    print("✨ SERVER RECONSTRUCTION COMPLETED SUCCESSFULLY!", flush=True)
    print("=======================================================\n", flush=True)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    if not client.guilds:
        print("No guilds found.")
        await client.close()
        return

    target_guild = client.guilds[0]
    await rebuild_server(target_guild)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
