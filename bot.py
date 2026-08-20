import os
import sys
import asyncio
import datetime
import re
from threading import Thread
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from flask import Flask

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID", "1539928402209935430")
PORT = int(os.environ.get("PORT", 10000))

# Flask Web Server for 24/7 Render Health Checks
app = Flask(__name__)

@app.route('/')
def home():
    return "Apex Predator Discord Bot is Online 24/7!"

@app.route('/health')
def health():
    return {"status": "ok", "bot": "APEX PREDATOR", "time": str(datetime.datetime.now(datetime.timezone.utc))}

def run_flask():
    print(f"[RENDER] Web server listening on port {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================================================================
# 🛡️ OPERATOR VERIFICATION MODAL & VIEW
# ==============================================================================
class VerificationModal(discord.ui.Modal, title="🛡️ Accept Rules & Verify Operator"):
    gamertag = discord.ui.TextInput(
        label="Activision Gamertag",
        placeholder="e.g. GhostOperator#1234567",
        required=True,
        max_length=40
    )
    clantag = discord.ui.TextInput(
        label="Clan Tag / Playstyle",
        placeholder="e.g. [APEX] / Aggressive SMG Rusher",
        required=False,
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        # 1. Assign Roles: Verified Operator & Warzone Slayer
        verified_role = discord.utils.get(guild.roles, name="🪖 Verified Operator") or discord.utils.get(guild.roles, name="Verified Member")
        warzone_role = discord.utils.get(guild.roles, name="🔫 Warzone Slayer") or discord.utils.get(guild.roles, name="Warzone Player")

        roles_to_add = [r for r in [verified_role, warzone_role] if r is not None]
        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason="Operator Verification & Rules Acceptance")
            except Exception as e:
                print(f"Error adding verified roles: {e}", flush=True)

        joined_str = member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "Unknown"
        created_str = member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        gamertag_val = self.gamertag.value.strip()
        clantag_val = self.clantag.value.strip() or "None"

        # 2. Welcome Message in #welcome
        welcome_ch = discord.utils.get(guild.text_channels, name="welcome")
        if welcome_ch:
            welcome_embed = discord.Embed(
                title=f"🎉 WELCOME OPERATOR {member.name.upper()}!",
                description=f"Welcome {member.mention} to **Apex Universe**!\n\n"
                            f"✅ **Rules Accepted & Verified**\n"
                            f"🎮 **Activision ID:** `{gamertag_val}`\n"
                            f"🏷️ **Clan / Style:** `{clantag_val}`\n\n"
                            f"### 🚀 Next Steps:\n"
                            f"1. Check <#gamer-tags> to connect with fellow squad members.\n"
                            f"2. Post your squad callout in <#looking-for-squad>.\n"
                            f"3. Drop into a `Warzone Lobby` or `Warzone Comms` voice channel!",
                color=discord.Color.from_rgb(46, 204, 113),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            welcome_embed.set_thumbnail(url=member.display_avatar.url)
            welcome_embed.set_footer(text="Apex Universe Onboarding System")
            await welcome_ch.send(embed=welcome_embed)

        # 3. Post to Staff Chat
        staff_chat = discord.utils.get(guild.text_channels, name="staff-chat")
        if staff_chat:
            staff_embed = discord.Embed(
                title="🛡️ NEW OPERATOR ONBOARDED & LOGGED",
                description=f"Member {member.mention} has agreed to rules and verified their gamertag!",
                color=discord.Color.from_rgb(52, 152, 219),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            staff_embed.set_thumbnail(url=member.display_avatar.url)
            staff_embed.add_field(name="👤 Username", value=f"`{member.name}` ({member.mention})", inline=True)
            staff_embed.add_field(name="🆔 Discord ID", value=f"`{member.id}`", inline=True)
            staff_embed.add_field(name="🎮 Activision ID", value=f"**`{gamertag_val}`**", inline=False)
            staff_embed.add_field(name="🏷️ Clan Tag / Style", value=f"`{clantag_val}`", inline=False)
            staff_embed.add_field(name="📅 Joined Server", value=f"`{joined_str}`", inline=True)
            staff_embed.add_field(name="👶 Account Age", value=f"`{created_str}`", inline=True)
            staff_embed.set_footer(text="Operator Database • Staff Record")
            await staff_chat.send(embed=staff_embed)

        # 4. Broadcast Gamertag to #gamer-tags
        gt_channel = discord.utils.get(guild.text_channels, name="gamer-tags")
        if gt_channel:
            gt_embed = discord.Embed(
                description=f"🎮 **{member.mention}** registered Activision ID: **`{gamertag_val}`** | Clan: `{clantag_val}`",
                color=discord.Color.dark_grey()
            )
            await gt_channel.send(embed=gt_embed)

        # 5. Direct reply to user
        await interaction.response.send_message(
            f"✅ **Rules Accepted & Verification Complete!**\n\n"
            f"You are now an official **@🪖 Verified Operator**! All community channels and Warzone lobbies are unlocked.\n\n"
            f"👉 Check out your welcome card in <#welcome>\n"
            f"👉 View community tags in <#gamer-tags>\n"
            f"👉 Jump into <#general-chat> or <#looking-for-squad>!",
            ephemeral=True
        )

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛡️ Accept Rules & Verify Operator", style=discord.ButtonStyle.success, custom_id="verify_operator_btn")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerificationModal())

# ==============================================================================
# 🎫 TICKET SYSTEM
# ==============================================================================
class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close & Archive Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        guild = interaction.guild

        await interaction.response.send_message("🔒 Closing ticket in 5 seconds and logging transcript...", ephemeral=False)
        await asyncio.sleep(5)

        ticket_logs = discord.utils.get(guild.text_channels, name="ticket-logs")
        if ticket_logs:
            messages = [msg async for msg in channel.history(limit=100, oldest_first=True)]
            transcript = "\n".join([f"[{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {m.author.name}: {m.content}" for m in messages])
            
            embed = discord.Embed(
                title=f"📁 TICKET CLOSED: {channel.name}",
                description=f"Closed by {interaction.user.mention}\n\n**Transcript Preview:**\n```\n{transcript[:1500]}\n```",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await ticket_logs.send(embed=embed)

        await channel.delete(reason=f"Ticket closed by {interaction.user.name}")

class TicketLaunchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Open Support Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user

        staff_cat = discord.utils.get(guild.categories, name="🛡️ STAFF ONLY")
        admin_role = discord.utils.get(guild.roles, name="👑 High Command") or discord.utils.get(guild.roles, name="Admin")
        mod_role = discord.utils.get(guild.roles, name="🛡️ Tactical Enforcer") or discord.utils.get(guild.roles, name="Moderator")

        existing_ch = discord.utils.get(guild.text_channels, name=f"ticket-{member.name.lower()}")
        if existing_ch:
            await interaction.response.send_message(f"⚠️ You already have an open ticket in {existing_ch.mention}!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, read_message_history=True)
        }
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True)
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True)

        ticket_ch = await guild.create_text_channel(
            name=f"ticket-{member.name.lower()}",
            category=staff_cat,
            overwrites=overwrites,
            topic=f"Support ticket for {member.name} (ID: {member.id})"
        )

        ticket_embed = discord.Embed(
            title=f"🎫 SUPPORT TICKET — {member.name}",
            description=f"Welcome {member.mention}!\n\n"
                        f"Please describe your issue, inquiry, or report in detail. Server staff will assist you shortly.\n\n"
                        f"Click the button below when your issue is resolved.",
            color=discord.Color.from_rgb(88, 101, 242)
        )
        await ticket_ch.send(embed=ticket_embed, view=TicketCloseView())
        await interaction.response.send_message(f"✅ Ticket created! Head over to {ticket_ch.mention}.", ephemeral=True)

# ==============================================================================
# 🚀 BOT EVENTS & AUDIT/MOD LOGGING
# ==============================================================================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)

    bot.add_view(VerifyView())
    bot.add_view(TicketLaunchView())
    bot.add_view(TicketCloseView())

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} application commands.", flush=True)
    except Exception as e:
        print(f"Failed to sync commands: {e}", flush=True)

    guild = bot.guilds[0] if bot.guilds else None
    if guild:
        # 1. Ensure #predator-chat exists in STAFF ONLY
        staff_cat = discord.utils.get(guild.categories, name="🛡️ STAFF ONLY")
        if staff_cat:
            pred_ch = discord.utils.get(staff_cat.text_channels, name="predator-chat")
            if not pred_ch:
                try:
                    pred_ch = await guild.create_text_channel(
                        name="predator-chat",
                        category=staff_cat,
                        topic="AI Staff Assistant — Ask server questions or command role assignments."
                    )
                    intro = discord.Embed(
                        title="🤖 APEX PREDATOR — STAFF INTELLIGENCE ASSISTANT",
                        description="Welcome Staff Members! This is your dedicated AI assistant channel.\n\n"
                                    "### 💬 How to Use Predator Chat:\n"
                                    "1. **Ask Any Server Question**:\n"
                                    "   • *\"Who can award the Entry Fragger role?\"*\n"
                                    "   • *\"How does a member earn Clip Creator?\"*\n"
                                    "   • *\"What are the requirements for Warzone Champion?\"*\n"
                                    "   • *\"What does Carl-bot or Dyno handle?\"*\n\n"
                                    "2. **Command Role Assignments**:\n"
                                    "   • *\"Assign @User the Entry Fragger role\"*\n"
                                    "   • *\"Give @User @Highlight MVP\"*\n"
                                    "   • *\"Award @User @Daily Grinder\"*\n\n"
                                    "The bot will execute the role assignment immediately or provide full operational guidance!",
                        color=discord.Color.from_rgb(231, 76, 60)
                    )
                    await pred_ch.send(embed=intro)
                    print("  + Created #predator-chat in [STAFF ONLY]", flush=True)
                except Exception as e:
                    print(f"Error creating #predator-chat: {e}", flush=True)

        # 2. Deploy/Update Verification Message in #verify-here
        verify_ch = discord.utils.get(guild.text_channels, name="verify-here")
        if verify_ch:
            try:
                await verify_ch.purge(limit=10)
            except:
                pass
            verify_embed = discord.Embed(
                title="🛡️ APEX UNIVERSE — OPERATOR VERIFICATION",
                description="Welcome to **Apex Universe**!\n\n"
                            "To gain full access to the server, unlock all squad lobbies, and view community channels:\n\n"
                            "1. Click **`🛡️ Accept Rules & Verify Operator`** below.\n"
                            "2. Enter your **Activision Gamertag** and **Clan Tag**.\n\n"
                            "✅ **Instant Unlocks:**\n"
                            "• **@🪖 Verified Operator** Role\n"
                            "• **@🔫 Warzone Slayer** Voice & Lobby Access\n"
                            "• <#welcome>, <#general-chat>, <#gamer-tags>, and all Squad Lobbies!\n",
                color=discord.Color.from_rgb(46, 204, 113)
            )
            verify_embed.set_footer(text="Apex Universe Automated Security • Click below to register")
            await verify_ch.send(embed=verify_embed, view=VerifyView())
            print("  + Deployed Interactive Verification Button to #verify-here", flush=True)

        # 3. Deploy Rules Embed + Agreement Button in #rules
        rules_ch = discord.utils.get(guild.text_channels, name="rules")
        if rules_ch:
            try:
                await rules_ch.purge(limit=10)
            except:
                pass
            rules_embed = discord.Embed(
                title="📜 APEX UNIVERSE — OFFICIAL SERVER RULES",
                description="Welcome to **Apex Universe**! To maintain a competitive, fun, and respectful environment, all members must abide by the following community standards.\n",
                color=discord.Color.from_rgb(26, 188, 156)
            )
            rules_embed.add_field(
                name="1️⃣ Respect & Conduct",
                value="Treat all squadmates with respect. Zero tolerance for harassment, racism, sexism, or toxic flaming.",
                inline=False
            )
            rules_embed.add_field(
                name="2️⃣ Zero Tolerance for Cheating",
                value="Using aimbots, wallhacks, engine scripts, chronus, strike-packs, or exploits results in an immediate permanent ban.",
                inline=False
            )
            rules_embed.add_field(
                name="3️⃣ Squad Comms Etiquette",
                value="Keep voice comms clear during ranked drops. No soundboards, screaming, or mic spam in comms channels.",
                inline=False
            )
            rules_embed.add_field(
                name="4️⃣ Controlled Self-Promotion",
                value="No unsolicited DM ads or unapproved Discord invites. Post your streams strictly in <#self-promo>.",
                inline=False
            )
            rules_embed.add_field(
                name="5️⃣ Follow Staff Directions",
                value="Moderators and Admins have final discretion on enforcement. Open a ticket in <#ticket-support> if you have inquiries.",
                inline=False
            )
            rules_embed.set_footer(text="Click the button below to accept the rules and unlock the server!")
            await rules_ch.send(embed=rules_embed, view=VerifyView())
            print("  + Deployed Rules with Agreement Button to #rules", flush=True)

        # 4. Deploy Ticket Launch in #ticket-support
        ticket_ch = discord.utils.get(guild.text_channels, name="ticket-support")
        if ticket_ch:
            try:
                await ticket_ch.purge(limit=10)
            except:
                pass
            t_embed = discord.Embed(
                title="🎫 STAFF SUPPORT & TICKET DESK",
                description="Need assistance from the **Apex Universe Staff Team**?\n\n"
                            "Open a private support ticket for:\n"
                            "• 🛡️ Reporting a toxic player or cheater\n"
                            "• 🎥 Applying for Verified Content Creator status\n"
                            "• 🏆 Tournament bracket inquiries\n"
                            "• 🤝 Server partnerships & sponsorships\n\n"
                            "Click the button below to open a private ticket channel!",
                color=discord.Color.from_rgb(88, 101, 242)
            )
            await ticket_ch.send(embed=t_embed, view=TicketLaunchView())
            print("  + Deployed Ticket Launch Button to #ticket-support", flush=True)

# ------------------------------------------------------------------------------
# 🧠 ON MESSAGE: PREDATOR CHAT INTELLIGENCE & ROLE ASSIGNMENT ENGINE
# ------------------------------------------------------------------------------
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    # Check if message is in #predator-chat
    if message.channel.name == "predator-chat":
        content = message.content.lower().strip()
        guild = message.guild
        author = message.author

        # A. ROLE ASSIGNMENT COMMAND EXECUTION (e.g. "assign @user role" or "give @user @role")
        if any(keyword in content for keyword in ["assign", "give", "award", "add role", "grant", "!assign"]):
            target_member = None
            if message.mentions:
                # First non-bot mentioned user
                target_member = next((m for m in message.mentions if not m.bot), None)

            # Find matching role in guild
            target_role = None
            if message.role_mentions:
                target_role = message.role_mentions[0]
            else:
                for r in guild.roles:
                    if r.name.lower() in content and r.name != "@everyone":
                        target_role = r
                        break

            if target_member and target_role:
                # Check if bot can assign
                if target_role >= guild.me.top_role:
                    await message.reply(f"⚠️ I cannot assign {target_role.mention} because it is positioned higher than my role hierarchy!")
                    return

                try:
                    await target_member.add_roles(target_role, reason=f"Staff Command by {author.name} in #predator-chat")
                    embed = discord.Embed(
                        title="✅ ROLE ASSIGNED SUCCESSFULLY",
                        description=f"**Target Member:** {target_member.mention} (`{target_member.id}`)\n"
                                    f"**Awarded Role:** {target_role.mention}\n"
                                    f"**Authorized By:** {author.mention}\n"
                                    f"**Timestamp:** {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
                        color=discord.Color.green()
                    )
                    await message.reply(embed=embed)
                    return
                except Exception as e:
                    await message.reply(f"❌ Error assigning role: {e}")
                    return
            elif target_member and not target_role:
                await message.reply(f"⚠️ I found member {target_member.mention}, but couldn't detect which role to assign. Please specify the role name or mention the role!")
                return

        # B. ROLE INQUIRY GUIDANCE (e.g. "who can award Entry Fragger", "how to get Highlight MVP", etc.)
        role_inquiries = {
            "entry fragger": {
                "role": "⚡ Entry Fragger",
                "who": "**🛡️ Tactical Enforcer (Moderator)**, **⭐ Task Force Director (Head Admin)**, or self-claimable by members in <#roles>.",
                "criteria": "Operators specializing in aggressive close-range SMG/Shotgun point-man combat and building breaches.",
                "command": f"`assign @User Entry Fragger` in this channel."
            },
            "igl": {
                "role": "🧠 IGL (In-Game Leader)",
                "who": "**🛡️ Tactical Enforcer (Moderator)**, **⭐ Task Force Director (Head Admin)**, or self-claimable in <#roles>.",
                "criteria": "Squad captains, rotation tacticians, and zone prediction shot-callers.",
                "command": f"`assign @User IGL` in this channel."
            },
            "sniper specialist": {
                "role": "🎯 Sniper Specialist",
                "who": "**🛡️ Tactical Enforcer (Moderator)**, **⭐ Task Force Director (Head Admin)**, or self-claimable in <#roles>.",
                "criteria": "Long-range marksmen and designated sniper operators.",
                "command": f"`assign @User Sniper Specialist` in this channel."
            },
            "support": {
                "role": "🛡️ Support / Anchor",
                "who": "**🛡️ Tactical Enforcer (Moderator)**, **⭐ Task Force Director (Head Admin)**, or self-claimable in <#roles>.",
                "criteria": "Squad anchors managing buy-station economy, UAV callouts, and redeploy covers.",
                "command": f"`assign @User Support / Anchor` in this channel."
            },
            "clip creator": {
                "role": "🎬 Clip Creator",
                "who": "**🛡️ Tactical Enforcer** or **⭐ Task Force Director**.",
                "criteria": "Awarded to members who actively upload 3+ gameplay clips or clutch highlights in <#clips-and-highlights>.",
                "command": f"`assign @User Clip Creator` in this channel."
            },
            "highlight mvp": {
                "role": "🌟 Highlight MVP",
                "who": "**⭐ Task Force Director** or **🛡️ Tactical Enforcer** (or automated Starboard).",
                "criteria": "Awarded to creators whose clutch clip receives **5 ⭐ reactions** in <#clips-and-highlights> and gets featured on the Starboard.",
                "command": f"`assign @User Highlight MVP` in this channel."
            },
            "daily grinder": {
                "role": "🔥 Daily Grinder",
                "who": "**Automated via MEE6 XP** or Staff override.",
                "criteria": "Awarded to members who reach **Level 5** in chat activity.",
                "command": f"`assign @User Daily Grinder` in this channel."
            },
            "community elite": {
                "role": "💎 Community Elite",
                "who": "**Automated via MEE6 XP** or Staff override.",
                "criteria": "Awarded to members who reach **Level 15** in chat activity.",
                "command": f"`assign @User Community Elite` in this channel."
            },
            "warzone champion": {
                "role": "🏆 Warzone Champion",
                "who": "**👑 High Command** or **⭐ Task Force Director**.",
                "criteria": "Exclusively awarded to tournament winners and custom lobby kill-race champions (permanently inducted into <#hall-of-fame>).",
                "command": f"`assign @User Warzone Champion` in this channel."
            },
            "scrim contender": {
                "role": "⚔️ Scrim Contender",
                "who": "**🛡️ Tactical Enforcer** or **⭐ Task Force Director**.",
                "criteria": "Awarded to active tournament participants and competitive team stacks.",
                "command": f"`assign @User Scrim Contender` in this channel."
            }
        }

        # Check if question matches any role inquiry
        for key, info in role_inquiries.items():
            if key in content or (key == "igl" and re.search(r'\bigl\b', content)):
                embed = discord.Embed(
                    title=f"📋 ROLE GUIDE: {info['role']}",
                    color=discord.Color.from_rgb(52, 152, 219)
                )
                embed.add_field(name="👑 Who Can Award This Role?", value=info["who"], inline=False)
                embed.add_field(name="🎯 Qualification Criteria", value=info["criteria"], inline=False)
                embed.add_field(name="⚡ How Staff Can Assign It", value=f"Reply with: {info['command']}", inline=False)
                embed.set_footer(text="Predator Intelligence Assistant")
                await message.reply(embed=embed)
                return

        # C. GENERAL SERVER ARCHITECTURE & OPERATIONS FAQ
        if "bot" in content or "carl" in content or "mee6" in content or "dyno" in content or "wick" in content:
            bot_embed = discord.Embed(
                title="🤖 SERVER BOT ARCHITECTURE SUMMARY",
                description="• **🛡️ APEX PREDATOR**: Registration Gateway, Verification Modal, Tickets, Audit & Mod Logging.\n"
                            "• **🐢 Carl-bot**: Reaction roles, custom tags (`!tag <name>`), 5 ⭐ Starboard in <#clips-and-highlights>.\n"
                            "• **🐺 Dyno**: Staff moderation hammer (`?warn`, `?mute`, `?kick`, `?ban`, `?lock`) & utilities (`?whois`).\n"
                            "• **⭐ MEE6**: Chat XP Leaderboard (`!rank`, `!levels`) & YouTube/Twitch live alerts.\n"
                            "• **🎮 Tatsu**: RPG profiles (`t!profile`), daily coins (`t!daily`), squad reputation (`t!rep @user`).\n"
                            "• **🛡️ Wick**: Anti-Nuke, Anti-Raid & Guild Security Shield.\n"
                            "• **🎵 Green-Bot**: High-definition music player in squad voice channels.",
                color=discord.Color.gold()
            )
            await message.reply(embed=bot_embed)
            return

        if "ticket" in content:
            await message.reply("🎫 **Ticket System**: Handled by **APEX PREDATOR** in <#ticket-support>. Opening a ticket creates a private channel in `🛡️ STAFF ONLY` accessible to Staff, and transcript logs are saved to <#ticket-logs> upon closure.")
            return

        if "voice" in content or "comms" in content or "lobby" in content:
            await message.reply("🔊 **Voice Channel Hierarchy**: `Warzone Lobby 1–4` and `Warzone Comms 1–2` are strictly capped at **4 members**. Duo Comms are capped at 2, and Trio Comms at 3. Text chat is disabled on Comms channels to maintain clear squad callouts.")
            return

        # General helpful staff fallback response
        help_fallback = discord.Embed(
            title="🤖 APEX PREDATOR STAFF ASSISTANT",
            description="I am your 24/7 Staff Operations Assistant! Here is what I can do for you:\n\n"
                        "• **Assign Roles Directly**: Say `assign @User RoleName` or `give @User @RoleName`.\n"
                        "• **Role Inquiries**: Ask *\"Who can award Entry Fragger?\"* or *\"How to get Clip Creator?\"*.\n"
                        "• **Bot & Architecture Help**: Ask about *\"bots\"*, *\"tickets\"*, or *\"voice comms\"*.\n"
                        "• **Moderation Commands**: Use Dyno (`?warn`, `?mute`, `?kick`, `?ban`) or APEX PREDATOR (`/ban`, `/kick`, `/timeout`, `/purge`).",
            color=discord.Color.from_rgb(231, 76, 60)
        )
        await message.reply(embed=help_fallback)

    await bot.process_commands(message)

# ------------------------------------------------------------------------------
# 📥 ON MEMBER JOIN: SEND PERSONALIZED DM GUIDE & LOG EVENT
# ------------------------------------------------------------------------------
@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    mod_logs = discord.utils.get(guild.text_channels, name="mod-logs")
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")
    created_str = member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # 1. Dispatch Logging Embeds
    if member.bot:
        embed = discord.Embed(
            title="🤖 BOT ADDED TO SERVER",
            description=f"**Bot:** {member.mention} (`{member.name}`)\n"
                        f"**Bot ID:** `{member.id}`\n"
                        f"**Account Created:** `{created_str}`",
            color=discord.Color.purple(),
            timestamp=now_utc
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Security Alert • Apex Predator Logger")
        if mod_logs:
            await mod_logs.send(embed=embed)
        if audit_logs:
            await audit_logs.send(embed=embed)
    else:
        embed = discord.Embed(
            title="📥 MEMBER JOINED SERVER",
            description=f"**User:** {member.mention} (`{member.name}`)\n"
                        f"**User ID:** `{member.id}`\n"
                        f"**Account Created:** `{created_str}`\n"
                        f"**Total Member Count:** `{guild.member_count}`",
            color=discord.Color.green(),
            timestamp=now_utc
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Member Join Event")
        if mod_logs:
            await mod_logs.send(embed=embed)
        if audit_logs:
            await audit_logs.send(embed=embed)

        # 2. Send Direct Personal Welcome & Server Guide DM to New Member
        try:
            dm_embed1 = discord.Embed(
                title=f"👑 WELCOME TO APEX UNIVERSE, OPERATOR {member.name.upper()}!",
                description=f"Welcome to the **#1 Warzone & Tactical Gaming Community**!\n\n"
                            f"To get you into the action immediately, here is your complete **Server Operations & Progression Guide**.\n",
                color=discord.Color.from_rgb(231, 76, 60)
            )
            dm_embed1.add_field(
                name="🔓 STEP 1: UNLOCK THE SERVER (VERIFICATION)",
                value="1. Head to the **#verify-here** or **#rules** channel in the server.\n"
                      "2. Click the green **`🛡️ Accept Rules & Verify Operator`** button.\n"
                      "3. Enter your **Activision Gamertag** and **Clan Tag**.\n"
                      "*(This instantly unlocks all 25+ community channels, squad lobbies, and voice comms!)*",
                inline=False
            )
            dm_embed1.add_field(
                name="🎖️ STEP 2: HOW TO EARN ROLES & PROGRESSION",
                value="We reward our active operators with exclusive roles and perks:\n\n"
                      "• **🎯 Squad Specializations** *(Self-select in #roles)*:\n"
                      "  `@IGL`, `@Sniper Specialist`, `@Entry Fragger`, `@Support / Anchor`, `@PC Operator`, `@Console Operator`.\n\n"
                      "• **🔥 Activity & Chat Leveling** *(Earn XP by chatting)*:\n"
                      "  `Level 5` ➔ **@🔥 Daily Grinder**\n"
                      "  `Level 15` ➔ **@💎 Community Elite**\n\n"
                      "• **🎬 Content Creator & Clip Rewards**:\n"
                      "  Post your clutch 1v4s & snipes in **#clips-and-highlights**.\n"
                      "  3+ clips posted ➔ **@🎬 Clip Creator**\n"
                      "  Receive 5 ⭐ reactions ➔ Featured on Starboard & earns **@🌟 Highlight MVP**!\n\n"
                      "• **🏆 Competitive Scrims & Tournaments**:\n"
                      "  Participate in community matches in **#tournaments** to earn **@⚔️ Scrim Contender** and **@🏆 Warzone Champion** (inducted into **#hall-of-fame**)!",
                inline=False
            )
            dm_embed1.add_field(
                name="🤖 STEP 3: SERVER BOTS & HOW TO USE THEM",
                value="• **⭐ MEE6**: Check your chat rank & level (`!rank`, `!levels` in #bot-commands).\n"
                      "• **🎮 Tatsu**: View your RPG profile (`t!profile`), claim coins (`t!daily`), award squad honor (`t!rep @user`).\n"
                      "• **🎵 Green-Bot**: High-definition music in squad voice channels (`/play <song>` in #music-requests).\n"
                      "• **🐢 Carl-bot**: Reaction roles, custom tags (`!tag <name>`), and community Starboard.\n"
                      "• **🐺 Dyno**: AFK statuses (`?afk <reason>`) & account info (`?whois @user`).\n"
                      "• **🛡️ APEX PREDATOR**: Private staff help desk (`#ticket-support`).",
                inline=False
            )
            dm_embed1.add_field(
                name="🎯 STEP 4: FINDING A SQUAD",
                value="Looking for teammates right now? Post your stats in **#looking-for-squad** or jump directly into any open **Warzone Lobby (1–4)** or **Duo/Trio Comms** voice room!",
                inline=False
            )
            dm_embed1.set_footer(text="Apex Universe High Command • See you in Urzikstan!")
            await member.send(embed=dm_embed1)
            print(f"  + Sent comprehensive personal welcome guide DM to {member.name}", flush=True)
        except Exception as e:
            print(f"  - Could not send DM to {member.name} (DMs likely closed): {e}", flush=True)

# Member Leave Event (Logged to #mod-logs and #audit-logs)
@bot.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    mod_logs = discord.utils.get(guild.text_channels, name="mod-logs")
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")
    joined_str = member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "Unknown"
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    embed = discord.Embed(
        title="📤 MEMBER LEFT / REMOVED",
        description=f"**User:** {member.mention} (`{member.name}`)\n"
                    f"**User ID:** `{member.id}`\n"
                    f"**Joined Server:** `{joined_str}`\n"
                    f"**Total Member Count:** `{guild.member_count}`",
        color=discord.Color.red(),
        timestamp=now_utc
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Member Leave Event")
    if mod_logs:
        await mod_logs.send(embed=embed)
    if audit_logs:
        await audit_logs.send(embed=embed)

# Message Delete Event (Logged to #audit-logs)
@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot or not message.guild:
        return
    audit_ch = discord.utils.get(message.guild.text_channels, name="audit-logs")
    if audit_ch:
        content_preview = message.content[:1500] if message.content else "[Attachment / Embed]"
        embed = discord.Embed(
            title="🗑️ MESSAGE DELETED",
            description=f"**Author:** {message.author.mention} (`{message.author.id}`)\n"
                        f"**Channel:** {message.channel.mention}\n"
                        f"**Content:**\n```\n{content_preview}\n```",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_footer(text=f"Author ID: {message.author.id}")
        await audit_ch.send(embed=embed)

# Message Edit Event (Logged to #audit-logs)
@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot or not before.guild or before.content == after.content:
        return
    audit_ch = discord.utils.get(before.guild.text_channels, name="audit-logs")
    if audit_ch:
        embed = discord.Embed(
            title="✏️ MESSAGE EDITED",
            description=f"**Author:** {before.author.mention} (`{before.author.id}`)\n"
                        f"**Channel:** {before.channel.mention}\n"
                        f"**Before:**\n```\n{before.content[:700]}\n```\n"
                        f"**After:**\n```\n{after.content[:700]}\n```\n"
                        f"[Jump to Message]({after.jump_url})",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_footer(text=f"Author ID: {before.author.id}")
        await audit_ch.send(embed=embed)

# Member Update Event (Roles, Nicknames, Boosts)
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    guild = after.guild
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")
    general_ch = discord.utils.get(guild.text_channels, name="general-chat")

    # Boost Event
    if before.premium_since is None and after.premium_since is not None:
        boost_embed = discord.Embed(
            title="🚀 SERVER BOOST CELEBRATION! 🚀",
            description=f"Huge thank you to {after.mention} for boosting **Apex Universe**!\n\n"
                        f"Your support unlocks higher audio bitrate, custom emojis, and HD streaming for all squads! 👑",
            color=discord.Color.magenta(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        boost_embed.set_thumbnail(url=after.display_avatar.url)
        if general_ch:
            await general_ch.send(embed=boost_embed)
        if audit_logs:
            await audit_logs.send(embed=boost_embed)

    # Role Changes
    if before.roles != after.roles and audit_logs:
        added_roles = [r.mention for r in after.roles if r not in before.roles]
        removed_roles = [r.mention for r in before.roles if r not in after.roles]
        if added_roles or removed_roles:
            desc = f"**User:** {after.mention} (`{after.id}`)\n"
            if added_roles:
                desc += f"➕ **Added Roles:** {', '.join(added_roles)}\n"
            if removed_roles:
                desc += f"➖ **Removed Roles:** {', '.join(removed_roles)}\n"
            role_embed = discord.Embed(
                title="🏷️ MEMBER ROLES UPDATED",
                description=desc,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await audit_logs.send(embed=role_embed)

# Channel Create / Delete Events
@bot.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    audit_logs = discord.utils.get(channel.guild.text_channels, name="audit-logs")
    if audit_logs:
        embed = discord.Embed(
            title="📁 CHANNEL CREATED",
            description=f"**Channel:** #{channel.name} (`{channel.id}`)\n**Type:** {str(channel.type).capitalize()}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        await audit_logs.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
    audit_logs = discord.utils.get(channel.guild.text_channels, name="audit-logs")
    if audit_logs:
        embed = discord.Embed(
            title="📁 CHANNEL DELETED",
            description=f"**Channel:** #{channel.name} (`{channel.id}`)\n**Type:** {str(channel.type).capitalize()}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        await audit_logs.send(embed=embed)

# ==============================================================================
# ⚔️ SLASH COMMANDS (MODERATION & UTILITIES)
# ==============================================================================
@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(member="The member to ban", reason="Reason for the ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=f"{reason} (Banned by {interaction.user.name})")
    embed = discord.Embed(
        title="🔨 MEMBER BANNED",
        description=f"**User:** {member.mention} (`{member.id}`)\n**Enforcer:** {interaction.user.mention}\n**Reason:** {reason}",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    mod_logs = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if mod_logs:
        await mod_logs.send(embed=embed)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.kick(reason=f"{reason} (Kicked by {interaction.user.name})")
    embed = discord.Embed(
        title="👢 MEMBER KICKED",
        description=f"**User:** {member.mention} (`{member.id}`)\n**Enforcer:** {interaction.user.mention}\n**Reason:** {reason}",
        color=discord.Color.orange(),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    mod_logs = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if mod_logs:
        await mod_logs.send(embed=embed)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timeout", description="Timeout/Mute a member")
@app_commands.describe(member="The member to timeout", minutes="Duration in minutes", reason="Reason for timeout")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=f"{reason} (Timed out by {interaction.user.name})")
    embed = discord.Embed(
        title="⏳ MEMBER TIMED OUT",
        description=f"**User:** {member.mention} (`{member.id}`)\n**Duration:** {minutes} minutes\n**Enforcer:** {interaction.user.mention}\n**Reason:** {reason}",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    mod_logs = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if mod_logs:
        await mod_logs.send(embed=embed)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="purge", description="Bulk delete messages from the current channel")
@app_commands.describe(amount="Number of messages to delete")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 Successfully deleted {len(deleted)} messages.", ephemeral=True)

# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    bot.run(TOKEN)
