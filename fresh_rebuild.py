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

# Target Category & Channel Structure
BLUEPRINT = [
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
            {"name": "Warzone Comms 2", "type": "voice", "user_limit": 4}
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
            {"name": "custom-lobbies", "type": "text", "topic": "Custom match room codes, passwords, and schedules"}
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

async def fresh_rebuild(guild):
    print(f"\n=======================================================", flush=True)
    print(f"🗑️ 1. DELETING ALL CHANNELS & CATEGORIES ON {guild.name}", flush=True)
    print(f"=======================================================\n", flush=True)

    # First delete non-category channels
    for ch in list(guild.channels):
        if not isinstance(ch, discord.CategoryChannel):
            try:
                await ch.delete()
                print(f"  - Deleted Channel: #{ch.name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Failed to delete #{ch.name}: {e}", flush=True)

    # Then delete all categories
    for cat in list(guild.categories):
        try:
            await cat.delete()
            print(f"  - Deleted Category: [{cat.name}]", flush=True)
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"  - Failed to delete category [{cat.name}]: {e}", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"🏗️ 2. REBUILDING CATEGORIES & CHANNELS FROM SCRATCH", flush=True)
    print(f"=======================================================\n", flush=True)

    admin_role = discord.utils.get(guild.roles, name="Admin")
    mod_role = discord.utils.get(guild.roles, name="Moderator")

    created_text_channels = {}

    for cat_def in BLUEPRINT:
        cat_name = cat_def["name"]
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

        try:
            cat = await guild.create_category(cat_name, overwrites=overwrites)
            print(f"\n📂 [CREATED CATEGORY] {cat.name}", flush=True)
        except Exception as e:
            print(f"\n📂 [ERROR CATEGORY] {cat_name}: {e}", flush=True)
            continue

        for ch_def in cat_def["channels"]:
            ch_name = ch_def["name"]
            ch_type = ch_def.get("type", "text")
            ch_topic = ch_def.get("topic", "")

            try:
                if ch_type == "text":
                    new_ch = await guild.create_text_channel(
                        name=ch_name,
                        category=cat,
                        topic=ch_topic
                    )
                    created_text_channels[ch_name] = new_ch
                    print(f"   ├── [TEXT] #{new_ch.name}", flush=True)
                elif ch_type == "voice":
                    user_limit = ch_def.get("user_limit", 0)
                    new_ch = await guild.create_voice_channel(
                        name=ch_name,
                        category=cat,
                        user_limit=user_limit
                    )
                    print(f"   ├── [VOICE] 🔊 {new_ch.name} (limit: {user_limit})", flush=True)
                await asyncio.sleep(0.4)
            except Exception as e:
                print(f"   ├── [ERROR] {ch_name}: {e}", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"📜 3. DEPLOYING STARTER EMBEDS & GUIDELINES", flush=True)
    print(f"=======================================================\n", flush=True)

    # 1. Post Rules
    if "rules" in created_text_channels:
        rules_ch = created_text_channels["rules"]
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

    # 2. Post LFG Format
    if "looking-for-squad" in created_text_channels:
        lfg_ch = created_text_channels["looking-for-squad"]
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

    # 3. Post Loadout Guide
    if "loadouts-and-meta" in created_text_channels:
        loadout_ch = created_text_channels["loadouts-and-meta"]
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

    # 4. Post Verification Prompt
    if "verify-here" in created_text_channels:
        verify_ch = created_text_channels["verify-here"]
        verify_embed = discord.Embed(
            title="🛡️ APEX UNIVERSE MEMBER VERIFICATION",
            description="Welcome to **Apex Universe**!\n\nTo prevent raids and keep our community secure, please verify your account to unlock full channel access.\n\nClick the button below or react to gain the **Verified Member** role.",
            color=discord.Color.green()
        )
        verify_embed.set_footer(text="Apex Universe Verification System")
        await verify_ch.send(embed=verify_embed)
        print("  + Sent Verification prompt to #verify-here", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"🎉 CLEAN REBUILD COMPLETED 100% SUCCESSFULLY!", flush=True)
    print(f"=======================================================\n", flush=True)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    if not client.guilds:
        print("No guilds found.", flush=True)
        await client.close()
        return

    target_guild = client.guilds[0]
    await fresh_rebuild(target_guild)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
