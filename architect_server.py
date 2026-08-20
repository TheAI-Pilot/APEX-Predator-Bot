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

# Target Roles Specification
TARGET_ROLES = [
    {
        "name": "Admin",
        "color": 0x1ABC9C,
        "hoist": True,
        "perms": {"administrator": True}
    },
    {
        "name": "Head Admin",
        "color": 0xE74C3C,
        "hoist": True,
        "perms": {
            "manage_guild": True,
            "manage_roles": True,
            "manage_channels": True,
            "ban_members": True,
            "kick_members": True,
            "manage_messages": True,
            "manage_webhooks": True
        }
    },
    {
        "name": "Moderator",
        "color": 0x9B59B6,
        "hoist": True,
        "perms": {
            "ban_members": True,
            "kick_members": True,
            "moderate_members": True,
            "manage_messages": True,
            "manage_threads": True,
            "mute_members": True,
            "deafen_members": True,
            "move_members": True
        }
    },
    {
        "name": "Helper / Coach",
        "color": 0x3498DB,
        "hoist": True,
        "perms": {
            "send_messages": True,
            "manage_threads": True,
            "attach_files": True,
            "embed_links": True,
            "use_external_emojis": True
        }
    },
    {
        "name": "OG / Founder",
        "color": 0xF1C40F,
        "hoist": True,
        "perms": {}
    },
    {
        "name": "Tournament Participant",
        "color": 0xE67E22,
        "hoist": True,
        "perms": {}
    },
    {
        "name": "Event Winner",
        "color": 0xF39C12,
        "hoist": True,
        "perms": {}
    },
    {
        "name": "Verified Member",
        "color": 0x2ECC71,
        "hoist": True,
        "perms": {
            "send_messages": True,
            "attach_files": True,
            "embed_links": True,
            "use_external_emojis": True,
            "read_message_history": True,
            "connect": True,
            "speak": True
        }
    },
    {
        "name": "Warzone Player",
        "color": 0x34495E,
        "hoist": False,
        "perms": {}
    },
    {
        "name": "Valorant Player",
        "color": 0xFA4454,
        "hoist": False,
        "perms": {}
    },
    {
        "name": "Apex Player",
        "color": 0xDA292A,
        "hoist": False,
        "perms": {}
    },
    {
        "name": "Mobile Player",
        "color": 0x95A5A6,
        "hoist": False,
        "perms": {}
    },
    {
        "name": "Quarantine",
        "color": 0x7F8C8D,
        "hoist": False,
        "perms": {}
    }
]

# Legacy Roles to Delete
LEGACY_ROLES_TO_DELETE = [
    "Member",
    "Apex Lobby Access",
    "Warzone Lobby Access",
    "Valorant Lobby Access",
    "Mobile Lobby Access"
]

# Exact Channel Blueprint
STRUCTURE = [
    {
        "category": "🛡️ STAFF ONLY",
        "type": "staff",
        "channels": [
            {"name": "staff-chat", "type": "text", "topic": "Private discussions for server staff"},
            {"name": "mod-logs", "type": "text", "topic": "Automated moderation action logs"},
            {"name": "audit-logs", "type": "text", "topic": "Server audit trail for joins, leaves, and edits"},
            {"name": "ticket-logs", "type": "text", "topic": "Archived tickets and support transcripts"}
        ]
    },
    {
        "category": "🚪 START HERE",
        "type": "start_here",
        "channels": [
            {"name": "welcome", "type": "text", "topic": "Welcome greeting and server intro"},
            {"name": "rules", "type": "text", "topic": "Official server rules and community standards"},
            {"name": "roles", "type": "text", "topic": "Self-assign your game and notification roles"},
            {"name": "announcements", "type": "text", "topic": "Major server announcements and tournaments"},
            {"name": "verify-here", "type": "text", "topic": "Click to verify and unlock full server access"}
        ]
    },
    {
        "category": "💬 COMMUNITY HUB",
        "type": "verified_only",
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
        "category": "🔫 WARZONE",
        "type": "game_gated",
        "game_role": "Warzone Player",
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
            {"name": "Warzone Comms 1", "type": "voice", "user_limit": 4, "text_disabled": True},
            {"name": "Warzone Comms 2", "type": "voice", "user_limit": 4, "text_disabled": True}
        ]
    },
    {
        "category": "🎯 VALORANT",
        "type": "game_gated",
        "game_role": "Valorant Player",
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
        "category": "🔺 APEX LEGENDS",
        "type": "game_gated",
        "game_role": "Apex Player",
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
        "category": "📱 MOBILE GAMING",
        "type": "game_gated",
        "game_role": "Mobile Player",
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
        "category": "🏆 EVENTS & TOURNAMENTS",
        "type": "verified_only",
        "channels": [
            {"name": "events-hub", "type": "text", "topic": "Community tournaments calendar and general FAQs"},
            {"name": "tournaments", "type": "text", "topic": "Official tournament brackets, rules, and signups"},
            {"name": "custom-lobbies", "type": "text", "topic": "Custom match room codes, passwords, and schedules"}
        ]
    },
    {
        "category": "🎥 STREAMS & CONTENT",
        "type": "verified_only",
        "channels": [
            {"name": "stream-notifications", "type": "text", "topic": "Live Twitch and YouTube stream alerts"},
            {"name": "content-creators", "type": "text", "topic": "Verified creator showcase and socials"},
            {"name": "youtube-videos", "type": "text", "topic": "New video drops, guides, and montages"}
        ]
    },
    {
        "category": "🤖 BOT COMMANDS & UTILS",
        "type": "verified_only",
        "channels": [
            {"name": "bot-commands", "type": "text", "topic": "Bot spam and slash command interactions"},
            {"name": "music-requests", "type": "text", "topic": "Song requests and queue management"},
            {"name": "ticket-support", "type": "text", "topic": "Open a support ticket for staff assistance"}
        ]
    },
    {
        "category": "📊 SERVER STATS",
        "type": "verified_only",
        "channels": [
            {"name": "📊 Members: 70", "type": "voice", "user_limit": 0}
        ]
    }
]

async def execute_architect_rebuild(guild):
    print(f"\n=======================================================", flush=True)
    print(f"🏗️ 1. SYNCING & CLEANING ROLES ON {guild.name}", flush=True)
    print(f"=======================================================\n", flush=True)

    # Delete redundant legacy roles
    for r_name in LEGACY_ROLES_TO_DELETE:
        role = discord.utils.get(guild.roles, name=r_name)
        if role and not role.managed:
            try:
                await role.delete()
                print(f"  - Deleted legacy role: @{r_name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Could not delete @{r_name}: {e}", flush=True)

    # Create/Update exact roles
    roles_map = {}
    existing_roles = {r.name.lower(): r for r in guild.roles}

    for r_def in TARGET_ROLES:
        r_name = r_def["name"]
        perms = discord.Permissions.none()
        for p_name, p_val in r_def.get("perms", {}).items():
            if hasattr(perms, p_name):
                setattr(perms, p_name, p_val)

        if r_name.lower() in existing_roles:
            role = existing_roles[r_name.lower()]
            if not role.managed:
                try:
                    await role.edit(
                        color=discord.Color(r_def["color"]),
                        hoist=r_def["hoist"],
                        permissions=perms
                    )
                    print(f"  [UPDATED] @{role.name}", flush=True)
                except Exception as e:
                    print(f"  [CANNOT EDIT] @{r_name}: {e}", flush=True)
            roles_map[r_name] = role
        else:
            try:
                role = await guild.create_role(
                    name=r_name,
                    color=discord.Color(r_def["color"]),
                    hoist=r_def["hoist"],
                    permissions=perms
                )
                print(f"  [CREATED] @{role.name}", flush=True)
                roles_map[r_name] = role
            except Exception as e:
                print(f"  [FAILED TO CREATE] @{r_name}: {e}", flush=True)
        await asyncio.sleep(0.3)

    admin_role = roles_map.get("Admin") or discord.utils.get(guild.roles, name="Admin")
    head_admin_role = roles_map.get("Head Admin") or discord.utils.get(guild.roles, name="Head Admin")
    mod_role = roles_map.get("Moderator") or discord.utils.get(guild.roles, name="Moderator")
    verified_role = roles_map.get("Verified Member") or discord.utils.get(guild.roles, name="Verified Member")
    quarantine_role = roles_map.get("Quarantine") or discord.utils.get(guild.roles, name="Quarantine")

    print(f"\n=======================================================", flush=True)
    print(f"🗑️ 2. PURGING ALL EXISTING CHANNELS & CATEGORIES", flush=True)
    print(f"=======================================================\n", flush=True)

    for ch in list(guild.channels):
        if not isinstance(ch, discord.CategoryChannel):
            try:
                await ch.delete()
                print(f"  - Deleted: #{ch.name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Preserved/Required #{ch.name}: {e}", flush=True)

    for cat in list(guild.categories):
        try:
            await cat.delete()
            print(f"  - Deleted Category: [{cat.name}]", flush=True)
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"  - Preserved Category [{cat.name}]: {e}", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"⚡ 3. BUILDING EXACT CATEGORIES & CHANNELS WITH PERMISSIONS", flush=True)
    print(f"=======================================================\n", flush=True)

    created_text_channels = {}

    for cat_data in STRUCTURE:
        cat_name = cat_data["category"]
        c_type = cat_data["type"]

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }

        # Staff Always Have Access
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
        if head_admin_role:
            overwrites[head_admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, connect=True, speak=True)

        # Quarantine Role Removed Posting
        if quarantine_role:
            overwrites[quarantine_role] = discord.PermissionOverwrite(send_messages=False, speak=False, add_reactions=False)

        if c_type == "staff":
            # Only staff, already configured above
            pass
        elif c_type == "start_here":
            overwrites[guild.default_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                add_reactions=True,
                read_message_history=True
            )
        elif c_type == "verified_only":
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
        elif c_type == "game_gated":
            g_role_name = cat_data.get("game_role")
            g_role = roles_map.get(g_role_name) or discord.utils.get(guild.roles, name=g_role_name)
            if g_role:
                overwrites[g_role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True,
                    read_message_history=True,
                    connect=True,
                    speak=True
                )

        try:
            cat = await guild.create_category(cat_name, overwrites=overwrites)
            print(f"\n📂 [CATEGORY] {cat.name}", flush=True)
        except Exception as e:
            print(f"\n📂 [ERROR CATEGORY] {cat_name}: {e}", flush=True)
            continue

        for ch_def in cat_data["channels"]:
            ch_name = ch_def["name"]
            ch_type = ch_def.get("type", "text")
            ch_topic = ch_def.get("topic", "")

            ch_overwrites = None
            if ch_def.get("text_disabled"):
                ch_overwrites = {
                    guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }

            try:
                if ch_type == "text":
                    new_ch = await guild.create_text_channel(
                        name=ch_name,
                        category=cat,
                        topic=ch_topic
                    )
                    created_text_channels[ch_name] = new_ch
                    print(f"   ├── 💬 #{new_ch.name}", flush=True)
                elif ch_type == "voice":
                    user_limit = ch_def.get("user_limit", 0)
                    new_ch = await guild.create_voice_channel(
                        name=ch_name,
                        category=cat,
                        user_limit=user_limit,
                        overwrites=ch_overwrites
                    )
                    print(f"   ├── 🔊 {new_ch.name} (limit: {user_limit})", flush=True)
                await asyncio.sleep(0.4)
            except Exception as e:
                print(f"   ├── ❌ [ERROR] {ch_name}: {e}", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"📜 4. POSTING STARTER EMBEDS, VERIFICATION & ROLE MENUS", flush=True)
    print(f"=======================================================\n", flush=True)

    # 1. Rules
    if "rules" in created_text_channels:
        rules_ch = created_text_channels["rules"]
        rules_embed = discord.Embed(
            title="📜 APEX UNIVERSE — OFFICIAL SERVER RULES",
            description="Welcome to **Apex Universe**! Please review and follow the community rules below.\n",
            color=discord.Color.from_rgb(26, 188, 156)
        )
        rules_embed.add_field(
            name="1️⃣ Respect & Professional Conduct",
            value="Treat all members and staff with respect. No toxicity, harassment, racism, or hate speech.",
            inline=False
        )
        rules_embed.add_field(
            name="2️⃣ Zero Tolerance for Cheating / Exploits",
            value="Using hacks, aimbots, wallhacks, scripts, strike packs, or cronus will result in an immediate permanent ban.",
            inline=False
        )
        rules_embed.add_field(
            name="3️⃣ No Spam & Clean Comms",
            value="Do not spam text channels, mentions, or soundboards in voice comms. Keep comms clear during ranked sessions.",
            inline=False
        )
        rules_embed.add_field(
            name="4️⃣ Controlled Self-Promotion",
            value="No unapproved Discord server invites or DM advertising. Post your content strictly in `#self-promo` and `#content-creators`.",
            inline=False
        )
        rules_embed.set_footer(text="Apex Universe Administration • Enforced by Moderation Team")
        await rules_ch.send(embed=rules_embed)
        print("  + Sent rules embed to #rules", flush=True)

    # 2. Roles Self-Assign
    if "roles" in created_text_channels:
        roles_ch = created_text_channels["roles"]
        roles_embed = discord.Embed(
            title="🏷️ GAME ROLES SELECTION",
            description="Select your games to unlock the corresponding channels and squad lobbies!\n\n"
                        "🔫 **Warzone Player** — Unlocks `#warzone-lobby`, loadouts, strats & comms\n"
                        "🎯 **Valorant Player** — Unlocks Valorant lobbies & strats\n"
                        "🔺 **Apex Player** — Unlocks Apex Legends lobbies & strats\n"
                        "📱 **Mobile Player** — Unlocks COD Mobile & BGMI lobbies\n",
            color=discord.Color.dark_blue()
        )
        roles_embed.set_footer(text="Click the buttons below or use /reactionrole to self-assign")
        await roles_ch.send(embed=roles_embed)
        print("  + Sent roles guide to #roles", flush=True)

    # 3. Verification Prompt
    if "verify-here" in created_text_channels:
        verify_ch = created_text_channels["verify-here"]
        verify_embed = discord.Embed(
            title="🛡️ SERVER VERIFICATION GATEWAY",
            description="Welcome to **Apex Universe**!\n\n"
                        "To protect our community against raids and automated bots, please verify your account to unlock access to the **Community Hub** and game lobbies.\n\n"
                        "Click the verification button or complete verification to gain the **Verified Member** role.",
            color=discord.Color.from_rgb(46, 204, 113)
        )
        verify_embed.set_footer(text="Apex Universe Automated Security")
        await verify_ch.send(embed=verify_embed)
        print("  + Sent verification embed to #verify-here", flush=True)

    # 4. Pinned LFG Format
    if "looking-for-squad" in created_text_channels:
        lfg_ch = created_text_channels["looking-for-squad"]
        lfg_embed = discord.Embed(
            title="🎯 SQUAD SEARCH (LFG) FORMAT",
            description="Copy and fill out the template below when searching for teammates:\n",
            color=discord.Color.blue()
        )
        lfg_embed.add_field(
            name="📋 Standard LFG Post Template",
            value="```yaml\nGame: Warzone / Valorant / Apex / Mobile\nRegion: NA / EU / IN / ASIA\nSquad Size: Need 1 / Need 2\nMode / Rank: Ranked (Diamond+) / Casual\nMic Required: Yes / No\nGamertag: YourTag#1234\n```",
            inline=False
        )
        msg = await lfg_ch.send(embed=lfg_embed)
        try:
            await msg.pin()
        except:
            pass
        print("  + Sent LFG template to #looking-for-squad", flush=True)

    # 5. Pinned Loadouts Guide
    if "loadouts-and-meta" in created_text_channels:
        loadout_ch = created_text_channels["loadouts-and-meta"]
        loadout_embed = discord.Embed(
            title="🔫 WARZONE META LOADOUT TEMPLATE",
            description="Share your top weapon builds with attachment tuning:\n",
            color=discord.Color.dark_grey()
        )
        loadout_embed.add_field(
            name="📝 Loadout Post Format",
            value="```yaml\nWeapon: [e.g. Superi 46 / KASTOV LSW]\nRole: Primary AR / Close-Range SMG / Sniper\nMuzzle: ...\nBarrel: ...\nOptic: ...\nUnderbarrel / Stock: ...\nMagazine: ...\nPerks: Double Time, Sleight of Hand, High Alert\n```",
            inline=False
        )
        msg = await loadout_ch.send(embed=loadout_embed)
        try:
            await msg.pin()
        except:
            pass
        print("  + Sent loadout template to #loadouts-and-meta", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"🎉 MASTER REBUILD COMPLETED EXACTLY AS SPECIFIED!", flush=True)
    print(f"=======================================================\n", flush=True)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    if not client.guilds:
        print("No guilds found.", flush=True)
        await client.close()
        return

    target_guild = client.guilds[0]
    await execute_architect_rebuild(target_guild)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
