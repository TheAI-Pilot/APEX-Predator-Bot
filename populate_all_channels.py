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
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# Custom channel content specifications
CONTENT_SPECS = {
    # -------------------------------------------------------------
    # 🚪 START HERE
    # -------------------------------------------------------------
    "welcome": {
        "embed": discord.Embed(
            title="👋 WELCOME TO APEX UNIVERSE",
            description="The premier community for **Call of Duty: Warzone** players, competitive squads, and content creators!\n\n"
                        "### 🚀 Getting Started in 3 Easy Steps:\n"
                        "1. **Read the Rules** in <#rules> to keep the server clean and toxic-free.\n"
                        "2. **Verify Yourself** in <#verify-here> to unlock the entire community.\n"
                        "3. **Claim Your Role** in <#roles> to get pinged for squad drops and tournaments.\n\n"
                        "Drop your Activision tag in <#gamer-tags> and find your squad in <#looking-for-squad>!",
            color=discord.Color.from_rgb(46, 204, 113)
        ).set_footer(text="Apex Universe • Built for Warzone Grinders")
    },

    "announcements": {
        "embed": discord.Embed(
            title="🚨 MAJOR SERVER OVERHAUL & WARZONE TAKEOVER 🚨",
            description="Attention **Apex Universe** operators!\n\n"
                        "We have officially restructured the server into an elite, dedicated **Call of Duty: Warzone Headquarters**!\n\n"
                        "### 💀 A Moment of Silence for Non-Warzone Gamers:\n"
                        "> *To all the Valorant tacticians saving their abilities for the next round, the Apex Legends movement gods tap-strafing into the void, and the 4-finger gyro Mobile players...*\n\n"
                        "**It's time to put away the fantasy blasters and touch some real asphalt.** We are dropping straight into Urzikstan & Rebirth Island. Delete your crosshair codes, grab your meta loadout, and get into a squad comms channel or get left in the gas!\n\n"
                        "### 🔥 What's New:\n"
                        "• **Dedicated 4-Man Warzone Squad Lobbies** & low-latency Comms channels.\n"
                        "• **Meta Loadout & Weapon Tuning Hub** in <#loadouts-and-meta>.\n"
                        "• **Custom Scrims & Kill-Race Tournaments** in <#tournaments>.\n"
                        "• **Streamer & Creator Spotlights** in <#content-creators>.\n\n"
                        "Lock in, grab your loadouts, and let's get those wins! 🏆",
            color=discord.Color.from_rgb(231, 76, 60)
        ).set_footer(text="Apex Universe Staff • Adapt or Get Sent to the Gulag")
    },

    "rules": {
        "embed": discord.Embed(
            title="📜 APEX UNIVERSE — OFFICIAL SERVER RULES",
            description="Welcome to **Apex Universe**! To maintain a competitive, fun, and respectful environment, all members must abide by the following community standards.\n",
            color=discord.Color.from_rgb(26, 188, 156)
        ).add_field(
            name="1️⃣ Respect & Conduct",
            value="Treat all squadmates with respect. Zero tolerance for harassment, racism, sexism, or toxic flaming.",
            inline=False
        ).add_field(
            name="2️⃣ Zero Tolerance for Cheating",
            value="Using aimbots, wallhacks, engine scripts, chronus, strike-packs, or exploits results in an immediate permanent ban.",
            inline=False
        ).add_field(
            name="3️⃣ Squad Comms Etiquette",
            value="Keep voice comms clear during ranked drops. No soundboards, screaming, or mic spam in comms channels.",
            inline=False
        ).add_field(
            name="4️⃣ Controlled Self-Promotion",
            value="No unsolicited DM ads or unapproved Discord invites. Post your streams and clips strictly in <#self-promo>.",
            inline=False
        ).add_field(
            name="5️⃣ Follow Staff Directions",
            value="Moderators and Admins have final discretion on enforcement. Open a ticket in <#ticket-support> if you have inquiries.",
            inline=False
        ).set_footer(text="Apex Universe Administration • Break rules at your own risk")
    },

    "roles": {
        "embed": discord.Embed(
            title="🏷️ ROLES & NOTIFICATIONS DIRECTORY",
            description="Assign your roles to customize your pings and server identity!\n\n"
                        "### 🎮 Primary Game Role:\n"
                        "• **@Warzone Player** — Unlocks full access to the Warzone lobby, loadout hub, and squad voice comms.\n\n"
                        "### 🔔 Notification Roles:\n"
                        "• **@Tournament Participant** — Get pinged when custom lobbies, kill races, and tournaments open.\n"
                        "• **@Event Winner** — Hall of Fame role for tournament champions.\n"
                        "• **@OG / Founder** — Core early supporters of Apex Universe.\n\n"
                        "Click the buttons below or use the reaction menu to toggle your roles!",
            color=discord.Color.from_rgb(52, 73, 94)
        )
    },

    "verify-here": {
        "embed": discord.Embed(
            title="🛡️ MEMBER VERIFICATION GATEWAY",
            description="Welcome to **Apex Universe**!\n\n"
                        "To protect our server from spam bots and raids, please verify your account to unlock access to the **Community Hub**, squad search, and voice lobbies.\n\n"
                        "Click the **Verify** button below to receive the **@Verified Member** role!",
            color=discord.Color.from_rgb(46, 204, 113)
        ).set_footer(text="Automated Gatekeeper • Apex Universe Security")
    },

    # -------------------------------------------------------------
    # 💬 COMMUNITY HUB
    # -------------------------------------------------------------
    "general-chat": {
        "embed": discord.Embed(
            title="🏠 APEX UNIVERSE — GENERAL CHAT",
            description="Welcome to the main hangout! Talk about anything gaming, setup upgrades, squad clips, or general banter.\n\n"
                        "💬 **Topic Starter**: What's your current go-to Warzone primary weapon, and are you dropping Rebirth or Big Map?",
            color=discord.Color.blue()
        )
    },

    "warzone-chat": {
        "embed": discord.Embed(
            title="🔫 WARZONE STRAT & META CHAT",
            description="Dedicated space for all things Call of Duty: Warzone!\n\n"
                        "• Discuss weapon balance patches, shadow nerfs & buffs.\n"
                        "• Talk about movement tech, audio settings & visual filters.\n"
                        "• Share map rotations for Urzikstan, Rebirth Island, and Area 99.",
            color=discord.Color.dark_grey()
        )
    },

    "clips-and-highlights": {
        "embed": discord.Embed(
            title="🎬 CLIPS & SQUAD HIGHLIGHTS",
            description="Got a crazy 1v4 clutch, cross-map sniper shot, or hilarious death-comm?\n\n"
                        "Post your YouTube shorts, TikToks, Medal clips, or Discord MP4s here!\n"
                        "⭐ *Top clips will be featured in the server highlight reel!*",
            color=discord.Color.purple()
        )
    },

    "looking-for-squad": {
        "embed": discord.Embed(
            title="🎯 SQUAD SEARCH (LFG) DIRECTORY",
            description="Looking for teammates? Copy and fill out the format below to find a squad in seconds!\n\n"
                        "```yaml\n"
                        "Mode: Warzone Battle Royale / Resurgence / Ranked\n"
                        "Squad Needed: Need 1 / Need 2 / Need 3\n"
                        "Region: NA / EU / IN / ASIA\n"
                        "Rank / KD: Diamond+ / 1.5+ KD / Casual\n"
                        "Mic: Yes (Comms Required)\n"
                        "Activision Tag: YourName#0000000\n"
                        "```\n"
                        "💡 **Tip**: Hop into an empty `Warzone Lobby` or `Warzone Comms` voice channel first!",
            color=discord.Color.gold()
        )
    },

    "gamer-tags": {
        "embed": discord.Embed(
            title="🆔 ACTIVISION & GAMERTAG DATABASE",
            description="Share your gamertags so members can add you directly in-game!\n\n"
                        "```yaml\n"
                        "Activision ID: User#1234567\n"
                        "Platform: PC / PlayStation / Xbox\n"
                        "Playstyle: Aggressive Rusher / Anchor / Sniper\n"
                        "Active Hours: Evenings / Weekends\n"
                        "```",
            color=discord.Color.dark_blue()
        )
    },

    "self-promo": {
        "embed": discord.Embed(
            title="🎙️ CONTENT CREATOR & STREAM PROMOTION",
            description="Promote your live Twitch streams, YouTube videos, and kick channels here!\n\n"
                        "**Guidelines:**\n"
                        "• Only 1 self-promo link per 6 hours.\n"
                        "• Include a brief title describing your stream.\n"
                        "• No spamming other Discord servers or invite links.",
            color=discord.Color.teal()
        )
    },

    "memes-and-media": {
        "embed": discord.Embed(
            title="📸 MEMES & GAMING MEDIA",
            description="Drop your best Warzone memes, setup photos, rage moments, and gaming humor here!",
            color=discord.Color.orange()
        )
    },

    # -------------------------------------------------------------
    # 🔫 WARZONE FLAGSHIP
    # -------------------------------------------------------------
    "warzone-lobby": {
        "embed": discord.Embed(
            title="👑 WARZONE PRIMARY LOBBY",
            description="The central command lobby for organizing Warzone squads, Resurgence grinds, and Ranked stacks.\n\n"
                        "• Match up with verified players.\n"
                        "• Join **Warzone Lobby 1–4** for casual drops or **Warzone Comms 1–2** for pure in-game callouts.",
            color=discord.Color.from_rgb(52, 73, 94)
        )
    },

    "loadouts-and-meta": {
        "embed": discord.Embed(
            title="🔫 WARZONE META LOADOUT VAULT",
            description="Stay ahead of the meta! Post your best weapon builds and attachment tunings.\n\n"
                        "### 📝 Loadout Submission Format:\n"
                        "```yaml\n"
                        "Weapon: [e.g. Superi 46 / KASTOV LSW / Kar98k]\n"
                        "Role: Long-Range Primary / Close SMG / Sniper\n"
                        "Muzzle: ...\n"
                        "Barrel: ...\n"
                        "Optic: ...\n"
                        "Underbarrel / Stock: ...\n"
                        "Magazine: ...\n"
                        "Perk Package: Double Time, Sleight of Hand, Quick Fix, High Alert\n"
                        "```\n"
                        "Attach screenshot of your gunsmith build if available!",
            color=discord.Color.dark_grey()
        )
    },

    "warzone-strats": {
        "embed": discord.Embed(
            title="🗺️ WARZONE STRATEGIES & ROTATIONS",
            description="Share high-IQ rotation routes, power positions, gas plays, and UAV pacing tips.\n\n"
                        "• High-ground control on Rebirth & Big Map\n"
                        "• Gulag tips & 1v1 fundamentals\n"
                        "• Buy station economy & loadout drop timing",
            color=discord.Color.dark_gold()
        )
    },

    "warzone-clips": {
        "embed": discord.Embed(
            title="🎯 WARZONE-ONLY SNIPES & SQUAD WIPES",
            description="Pure Call of Duty: Warzone gameplay! Post your cleanest snipes, squad wipes, and 20+ kill gameplay summaries.",
            color=discord.Color.red()
        )
    },

    "warzone-events": {
        "embed": discord.Embed(
            title="🏆 WARZONE EVENTS & COMMUNITY SCRIMS",
            description="Stay tuned for upcoming server tournaments, private lobby matches, and bounty challenges!\n\n"
                        "• Weekly Resurgence Custom Lobbies\n"
                        "• Duo & Squad Kill-Race Tournaments\n"
                        "• Prize pools & @Event Winner recognition",
            color=discord.Color.gold()
        )
    },

    # -------------------------------------------------------------
    # 🏆 EVENTS & TOURNAMENTS
    # -------------------------------------------------------------
    "events-hub": {
        "embed": discord.Embed(
            title="🏆 TOURNAMENT RULES & SCORING SYSTEM",
            description="Official rules for all Apex Universe competitive events and kill races.\n\n"
                        "### 📊 Standard Scoring Formula:\n"
                        "• **1st Place Victory**: +15 Points\n"
                        "• **2nd–5th Place**: +10 Points\n"
                        "• **6th–10th Place**: +5 Points\n"
                        "• **Each Kill / Elimination**: +1 Point\n\n"
                        "Check <#tournaments> for upcoming bracket signups!",
            color=discord.Color.from_rgb(241, 196, 15)
        )
    },

    "tournaments": {
        "embed": discord.Embed(
            title="⚔️ UPCOMING TOURNAMENT REGISTRATION",
            description="Sign up your squad for official community tournaments!\n\n"
                        "```yaml\n"
                        "Team Name: [Your Squad Name]\n"
                        "Captain: @CaptainTag (Activision ID)\n"
                        "Teammates: @Player2, @Player3, @Player4\n"
                        "Region: NA / EU / IN / ASIA\n"
                        "```",
            color=discord.Color.from_rgb(230, 126, 34)
        )
    },

    "custom-lobbies": {
        "embed": discord.Embed(
            title="🎮 CUSTOM MATCH ROOM CODES",
            description="When private match scrims or custom lobbies are active, match passwords and room codes will be broadcasted here.\n\n"
                        "⚠️ *Sharing custom room codes outside of verified members will result in disqualification.*",
            color=discord.Color.purple()
        )
    },

    # -------------------------------------------------------------
    # 🎥 STREAMS & CONTENT
    # -------------------------------------------------------------
    "stream-notifications": {
        "embed": discord.Embed(
            title="🔴 LIVE STREAM NOTIFICATIONS",
            description="Automatic live notifications for server creators and streamers! Tune in, support community members, and watch high-tier gameplay.",
            color=discord.Color.red()
        )
    },

    "content-creators": {
        "embed": discord.Embed(
            title="🎬 VERIFIED CREATOR PROGRAM",
            description="Are you a Twitch Streamer, YouTuber, or TikTok creator producing Warzone content?\n\n"
                        "**Creator Perks:**\n"
                        "• Automatic live stream announcements in <#stream-notifications>\n"
                        "• Exclusive **@Content Creator** role\n"
                        "• Featured clip spots in server media\n\n"
                        "Open a ticket in <#ticket-support> to apply with links to your channels!",
            color=discord.Color.magenta()
        )
    },

    "youtube-videos": {
        "embed": discord.Embed(
            title="📺 YOUTUBE VIDEO SHOWCASE",
            description="Drop your newly uploaded YouTube videos, weapon guides, movement tutorials, and montages here!",
            color=discord.Color.red()
        )
    },

    # -------------------------------------------------------------
    # 🤖 BOT COMMANDS & UTILS
    # -------------------------------------------------------------
    "bot-commands": {
        "embed": discord.Embed(
            title="🤖 BOT COMMAND DIRECTORY",
            description="Keep general chat clean by using all bot commands in this channel!\n\n"
                        "### ⚡ Useful Commands:\n"
                        "• `/help` — Open interactive command directory\n"
                        "• `/serverinfo` — View live server health & member counts\n"
                        "• `/userinfo [user]` — Inspect account profile & roles\n"
                        "• `/ping` — Check bot response latency\n"
                        "• `!rank` / `!levels` — Check your MEE6 XP rank and level",
            color=discord.Color.blue()
        )
    },

    "music-requests": {
        "embed": discord.Embed(
            title="🎵 GREEN-BOT MUSIC CONTROLS",
            description="Request songs and control voice channel music queue!\n\n"
                        "### 🎧 Commands:\n"
                        "• `/play <song name or link>` — Play a song in your voice channel\n"
                        "• `/queue` — View upcoming songs in queue\n"
                        "• `/skip` — Vote to skip the current song\n"
                        "• `/pause` & `/resume` — Pause or resume playback\n"
                        "• `/volume <1-100>` — Adjust music volume",
            color=discord.Color.green()
        )
    },

    "ticket-support": {
        "embed": discord.Embed(
            title="🎫 STAFF SUPPORT & TICKET DESK",
            description="Need assistance from the **Apex Universe Staff Team**?\n\n"
                        "Open a private support ticket for:\n"
                        "• 🛡️ Reporting a toxic player or cheater\n"
                        "• 🎥 Applying for Verified Content Creator status\n"
                        "• 🏆 Tournament bracket inquiries & questions\n"
                        "• 🤝 Server partnerships & sponsorships\n\n"
                        "Click **Create Ticket** below to open a private channel with our moderators!",
            color=discord.Color.from_rgb(88, 101, 242)
        )
    },

    # -------------------------------------------------------------
    # 🛡️ STAFF ONLY
    # -------------------------------------------------------------
    "staff-chat": {
        "embed": discord.Embed(
            title="🛡️ APEX UNIVERSE STAFF HEADQUARTERS",
            description="Private discussion channel for Server Administrators and Moderators.\n\n"
                        "• Coordinate moderation actions and user warnings.\n"
                        "• Organize custom lobbies and tournament schedules.\n"
                        "• Review support tickets and ban appeals.",
            color=discord.Color.dark_gold()
        )
    },

    "mod-logs": {
        "embed": discord.Embed(
            title="🛡️ AUTOMATED MODERATION AUDIT FEED",
            description="Automated log feed for all mod commands (`/ban`, `/kick`, `/timeout`, `/warn`, `/purge`) and AutoMod security flags.",
            color=discord.Color.dark_red()
        )
    },

    "audit-logs": {
        "embed": discord.Embed(
            title="📜 SERVER AUDIT TRAIL",
            description="Live log feed tracking member joins, leaves, role updates, and message edits/deletions.",
            color=discord.Color.dark_blue()
        )
    },

    "ticket-logs": {
        "embed": discord.Embed(
            title="📁 ARCHIVED TICKET TRANSCRIPTS",
            description="Archived support ticket logs and resolution records.",
            color=discord.Color.greyple()
        )
    }
}

async def populate_all_channels(guild):
    print(f"\n=======================================================", flush=True)
    print(f"🚀 POPULATING & REFRESHING ALL CHANNELS ON {guild.name}", flush=True)
    print(f"=======================================================\n", flush=True)

    for ch in guild.text_channels:
        ch_name = ch.name.lower()
        if ch_name in CONTENT_SPECS:
            spec = CONTENT_SPECS[ch_name]
            try:
                # Delete old messages in the channel to remove conflicts
                try:
                    await ch.purge(limit=20)
                except Exception as e:
                    # fallback delete one by one if bulk delete fails
                    async for msg in ch.history(limit=20):
                        try:
                            await msg.delete()
                        except:
                            pass

                # Post new relevant embed
                embed = spec["embed"]
                sent_msg = await ch.send(embed=embed)
                
                # Pin if appropriate (rules, lfg, loadouts, tournaments)
                if ch_name in ["rules", "looking-for-squad", "loadouts-and-meta", "events-hub"]:
                    try:
                        await sent_msg.pin()
                    except:
                        pass

                print(f"  [SUCCESS] Populated #{ch.name} with custom Warzone content", flush=True)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"  [ERROR] Populating #{ch.name}: {e}", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"✨ ALL CHANNELS SUCCESSFULLY POPULATED & UPDATED!", flush=True)
    print(f"=======================================================\n", flush=True)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]
    await populate_all_channels(guild)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
