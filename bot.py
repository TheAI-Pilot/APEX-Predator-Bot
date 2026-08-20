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

# Tokens for Dual-Bot Deployment via Environment Variables
APEX_TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("APEX_TOKEN")
AI_PILOT_TOKEN = os.getenv("AI_PILOT_TOKEN")

PORT = int(os.environ.get("PORT", 10000))

# Flask Web Server for 24/7 Render Health Checks
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Apex Universe & AI Pilot Dual-Bot Cloud Engine is Online 24/7!"

@app.route('/health')
def health():
    return {
        "status": "ok",
        "apex_predator": str(apex_bot.is_ready()),
        "ai_pilot": str(ai_pilot_bot.is_ready()),
        "time": str(datetime.datetime.now(datetime.timezone.utc))
    }

def run_flask():
    print(f"[RENDER] Web server listening on port {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

# 1. Primary Bot: APEX PREDATOR
apex_bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Secondary Bot: AI PILOT 2.0
ai_pilot_bot = commands.Bot(command_prefix=".", intents=intents)

# ==============================================================================
# 🛡️ APEX PREDATOR — OPERATOR VERIFICATION MODAL & VIEW (Apex Universe)
# ==============================================================================
class ApexVerificationModal(discord.ui.Modal, title="🛡️ Accept Rules & Verify Operator"):
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

class ApexVerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛡️ Accept Rules & Verify Operator", style=discord.ButtonStyle.success, custom_id="verify_operator_btn")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ApexVerificationModal())

# ==============================================================================
# ✈️ AI PILOT 2.0 — VERIFICATION MODAL & VIEW (AI Pilot Server)
# ==============================================================================
class AIPilotVerificationModal(discord.ui.Modal, title="✈️ Pilot Verification & Onboarding"):
    name_handle = discord.ui.TextInput(
        label="Full Name / Creator Handle",
        placeholder="e.g. Alex Hunter / @AlexAI",
        required=True,
        max_length=50
    )
    phone = discord.ui.TextInput(
        label="Phone Number",
        placeholder="e.g. +1 (555) 123-4567",
        required=True,
        max_length=30
    )
    email = discord.ui.TextInput(
        label="Email Address (Optional)",
        placeholder="e.g. alex@aipilot.io (for drops & templates)",
        required=False,
        max_length=60
    )
    background = discord.ui.TextInput(
        label="DOB / AI Background & Interests",
        placeholder="e.g. 1998-05-12 / Automation, Prompting, LLMs",
        required=True,
        style=discord.TextStyle.paragraph,
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        # 1. Assign Verified Pilot role and remove New Arrival if present
        pilot_role = discord.utils.get(guild.roles, name="✈️ Verified Pilot") or discord.utils.get(guild.roles, name="Verified Pilot")
        new_arrival_role = discord.utils.get(guild.roles, name="🛰️ New Arrival")

        if pilot_role:
            try:
                await member.add_roles(pilot_role, reason="AI Pilot Gateway Verification Submitted")
            except Exception as e:
                print(f"Error adding Pilot role: {e}", flush=True)

        if new_arrival_role and new_arrival_role in member.roles:
            try:
                await member.remove_roles(new_arrival_role, reason="Completed Verification")
            except:
                pass

        joined_str = member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "Unknown"
        created_str = member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        name_val = self.name_handle.value.strip()
        phone_val = self.phone.value.strip()
        email_val = self.email.value.strip() or "None Provided"
        bg_val = self.background.value.strip()

        # 2. Log to #owner-vault (confidential private log)
        vault_ch = discord.utils.get(guild.text_channels, name="owner-vault")
        if vault_ch:
            vault_embed = discord.Embed(
                title="🔒 PILOT ONBOARDING DOSSIER — OWNER VAULT",
                description=f"New member {member.mention} has completed Gateway Verification!",
                color=discord.Color.from_rgb(88, 101, 242),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            vault_embed.set_thumbnail(url=member.display_avatar.url)
            vault_embed.add_field(name="👤 Discord User", value=f"`{member.name}` ({member.mention})", inline=True)
            vault_embed.add_field(name="🆔 Discord ID", value=f"`{member.id}`", inline=True)
            vault_embed.add_field(name="🏷️ Full Name / Handle", value=f"**`{name_val}`**", inline=False)
            vault_embed.add_field(name="📱 Phone Number", value=f"**`{phone_val}`**", inline=True)
            vault_embed.add_field(name="📧 Email Address", value=f"`{email_val}`", inline=True)
            vault_embed.add_field(name="🧠 Background / Interests", value=f"```\n{bg_val}\n```", inline=False)
            vault_embed.add_field(name="📅 Joined Server", value=f"`{joined_str}`", inline=True)
            vault_embed.add_field(name="👶 Account Age", value=f"`{created_str}`", inline=True)
            vault_embed.set_footer(text="AI Pilot Security Core • Vault Record")
            await vault_ch.send(embed=vault_embed)

        # 3. Post public welcome to #welcome
        welcome_ch = discord.utils.get(guild.text_channels, name="welcome")
        if welcome_ch:
            w_embed = discord.Embed(
                title=f"✈️ WELCOME PILOT {name_val.upper()}!",
                description=f"Welcome {member.mention} to **AI Pilot ✈️🤖**!\n\n"
                            f"✅ **Gateway Verification Cleared**\n"
                            f"🎯 **Role:** @✈️ Verified Pilot\n\n"
                            f"### 🚀 Quick Flight Plan:\n"
                            f"1. Choose your specialty roles in <#choose-your-path>.\n"
                            f"2. Introduce yourself in <#introductions>.\n"
                            f"3. Drop into <#general> or explore our prompt libraries!",
                color=discord.Color.from_rgb(46, 204, 113),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            w_embed.set_thumbnail(url=member.display_avatar.url)
            await welcome_ch.send(embed=w_embed)

        # 4. Ephemeral confirmation
        await interaction.response.send_message(
            f"✅ **Pilot Verification Submitted Successfully!**\n\n"
            f"Welcome aboard, **{name_val}**! You now hold the **@✈️ Verified Pilot** role and all 60+ channels are unlocked.\n\n"
            f"👉 Check out <#choose-your-path> to pick your AI domains!\n"
            f"👉 Jump into <#general> to chat with fellow builders.",
            ephemeral=True
        )

class AIPilotVerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✈️ Start Pilot Verification", style=discord.ButtonStyle.success, custom_id="ai_pilot_exclusive_verify_btn")
    async def pilot_verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AIPilotVerificationModal())

# ==============================================================================
# 🎫 APEX PREDATOR — TICKET SYSTEM
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
# 🚀 APEX PREDATOR EVENTS & LOGGING
# ==============================================================================
@apex_bot.event
async def on_ready():
    print(f"[APEX PREDATOR] Logged in as {apex_bot.user} (ID: {apex_bot.user.id})", flush=True)

    apex_bot.add_view(ApexVerifyView())
    apex_bot.add_view(TicketLaunchView())
    apex_bot.add_view(TicketCloseView())

    try:
        synced = await apex_bot.tree.sync()
        print(f"[APEX PREDATOR] Synced {len(synced)} slash commands.", flush=True)
    except Exception as e:
        print(f"[APEX PREDATOR] Failed to sync commands: {e}", flush=True)

    guild = apex_bot.guilds[0] if apex_bot.guilds else None
    if guild:
        staff_cat = discord.utils.get(guild.categories, name="🛡️ STAFF ONLY")
        if staff_cat:
            pred_ch = discord.utils.get(staff_cat.text_channels, name="predator-chat")
            if not pred_ch:
                try:
                    await guild.create_text_channel(
                        name="predator-chat",
                        category=staff_cat,
                        topic="AI Staff Assistant — Ask server questions or command role assignments."
                    )
                except:
                    pass

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
            await verify_ch.send(embed=verify_embed, view=ApexVerifyView())

# ------------------------------------------------------------------------------
# 🧠 ON MESSAGE: PREDATOR CHAT INTELLIGENCE & ROLE ASSIGNMENT ENGINE
# ------------------------------------------------------------------------------
@apex_bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    if message.channel.name == "predator-chat":
        content = message.content.lower().strip()
        guild = message.guild
        author = message.author

        # Role Assignment
        if any(keyword in content for keyword in ["assign", "give", "award", "add role", "grant", "!assign"]):
            target_member = next((m for m in message.mentions if not m.bot), None) if message.mentions else None
            target_role = message.role_mentions[0] if message.role_mentions else None
            if not target_role:
                for r in guild.roles:
                    if r.name.lower() in content and r.name != "@everyone":
                        target_role = r
                        break

            if target_member and target_role:
                if target_role >= guild.me.top_role:
                    await message.reply(f"⚠️ I cannot assign {target_role.mention} because it is positioned higher than my role hierarchy!")
                    return
                try:
                    await target_member.add_roles(target_role, reason=f"Staff Command by {author.name} in #predator-chat")
                    embed = discord.Embed(
                        title="✅ ROLE ASSIGNED SUCCESSFULLY",
                        description=f"**Target Member:** {target_member.mention} (`{target_member.id}`)\n"
                                    f"**Awarded Role:** {target_role.mention}\n"
                                    f"**Authorized By:** {author.mention}",
                        color=discord.Color.green(),
                        timestamp=datetime.datetime.now(datetime.timezone.utc)
                    )
                    await message.reply(embed=embed)
                    return
                except Exception as e:
                    await message.reply(f"❌ Error assigning role: {e}")
                    return

        # Role Inquiries
        role_inquiries = {
            "entry fragger": ("⚡ Entry Fragger", "**🛡️ Tactical Enforcer (Moderator)**, **⭐ Task Force Director (Head Admin)**, or self-claimable in <#roles>.", "Aggressive SMG/Shotgun point-man combat."),
            "igl": ("🧠 IGL (In-Game Leader)", "**🛡️ Tactical Enforcer**, **⭐ Task Force Director**, or self-claimable in <#roles>.", "Squad captains and zone prediction shot-callers."),
            "sniper specialist": ("🎯 Sniper Specialist", "**🛡️ Tactical Enforcer**, **⭐ Task Force Director**, or self-claimable in <#roles>.", "Long-range marksmen and designated snipers."),
            "support": ("🛡️ Support / Anchor", "**🛡️ Tactical Enforcer**, **⭐ Task Force Director**, or self-claimable in <#roles>.", "Buy-station economy and UAV callout anchors."),
            "clip creator": ("🎬 Clip Creator", "**🛡️ Tactical Enforcer** or **⭐ Task Force Director**.", "Post 3+ gameplay clips in <#clips-and-highlights>."),
            "highlight mvp": ("🌟 Highlight MVP", "**⭐ Task Force Director** or **🛡️ Tactical Enforcer**.", "Clutch clip receives **5 ⭐ reactions** in <#clips-and-highlights>."),
            "daily grinder": ("🔥 Daily Grinder", "**Automated via MEE6 XP** (Level 5).", "Active chatters reaching Level 5."),
            "community elite": ("💎 Community Elite", "**Automated via MEE6 XP** (Level 15).", "Active chatters reaching Level 15."),
            "warzone champion": ("🏆 Warzone Champion", "**👑 High Command** or **⭐ Task Force Director**.", "Official tournament winners (inducted into <#hall-of-fame>)."),
            "scrim contender": ("⚔️ Scrim Contender", "**🛡️ Tactical Enforcer** or **⭐ Task Force Director**.", "Active tournament competitors.")
        }

        for key, (r_name, r_who, r_crit) in role_inquiries.items():
            if key in content or (key == "igl" and re.search(r'\bigl\b', content)):
                embed = discord.Embed(title=f"📋 ROLE GUIDE: {r_name}", color=discord.Color.from_rgb(52, 152, 219))
                embed.add_field(name="👑 Who Can Award This Role?", value=r_who, inline=False)
                embed.add_field(name="🎯 Criteria", value=r_crit, inline=False)
                embed.add_field(name="⚡ Assign Command", value=f"Say `assign @User {r_name}` in this channel.", inline=False)
                await message.reply(embed=embed)
                return

        # General helpful fallback
        fallback = discord.Embed(
            title="🤖 APEX PREDATOR STAFF ASSISTANT",
            description="I am your Staff Operations Assistant! Say `assign @User RoleName` or ask about any role or bot!",
            color=discord.Color.from_rgb(231, 76, 60)
        )
        await message.reply(embed=fallback)

    await apex_bot.process_commands(message)

# ------------------------------------------------------------------------------
# 📥 ON MEMBER JOIN: SEND PERSONALIZED DM GUIDE & LOG EVENT
# ------------------------------------------------------------------------------
@apex_bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    mod_logs = discord.utils.get(guild.text_channels, name="mod-logs")
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    if member.bot:
        embed = discord.Embed(
            title="🤖 BOT ADDED TO SERVER",
            description=f"**Bot:** {member.mention} (`{member.name}`)\n**Bot ID:** `{member.id}`",
            color=discord.Color.purple(),
            timestamp=now_utc
        )
        if mod_logs: await mod_logs.send(embed=embed)
        if audit_logs: await audit_logs.send(embed=embed)
    else:
        embed = discord.Embed(
            title="📥 MEMBER JOINED SERVER",
            description=f"**User:** {member.mention} (`{member.name}`)\n**Total Count:** `{guild.member_count}`",
            color=discord.Color.green(),
            timestamp=now_utc
        )
        if mod_logs: await mod_logs.send(embed=embed)
        if audit_logs: await audit_logs.send(embed=embed)

        try:
            dm_embed = discord.Embed(
                title=f"👑 WELCOME TO APEX UNIVERSE, OPERATOR {member.name.upper()}!",
                description="Welcome to the **#1 Warzone & Tactical Gaming Community**!\n\n"
                            "🔓 **STEP 1: UNLOCK THE SERVER**\n"
                            "Click **`🛡️ Accept Rules & Verify Operator`** in **#verify-here** or **#rules** to enter your Gamertag!\n\n"
                            "🎖️ **STEP 2: EARN ROLES**\n"
                            "• Specializations: Self-select `@IGL`, `@Sniper`, `@Entry Fragger` in **#roles**.\n"
                            "• Activity XP: Reach Level 5 for **@🔥 Daily Grinder**, Level 15 for **@💎 Community Elite**.\n"
                            "• Clips: Post clutch clips in **#clips-and-highlights** for **@🎬 Clip Creator** & **@🌟 Highlight MVP**!\n\n"
                            "🤖 **STEP 3: BOT USAGE**\n"
                            "• MEE6: `!rank` | Tatsu: `t!profile`, `t!daily` | Green-Bot: `/play` in **#music-requests** | Dyno: `?afk`.",
                color=discord.Color.from_rgb(231, 76, 60)
            )
            await member.send(embed=dm_embed)
        except Exception as e:
            print(f"DM Error: {e}")

# Member Leave Event
@apex_bot.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    mod_logs = discord.utils.get(guild.text_channels, name="mod-logs")
    audit_logs = discord.utils.get(guild.text_channels, name="audit-logs")
    embed = discord.Embed(
        title="📤 MEMBER LEFT SERVER",
        description=f"**User:** {member.mention} (`{member.name}`)\n**Total Members:** `{guild.member_count}`",
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    if mod_logs: await mod_logs.send(embed=embed)
    if audit_logs: await audit_logs.send(embed=embed)

# Message Delete / Edit
@apex_bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot or not message.guild: return
    audit_ch = discord.utils.get(message.guild.text_channels, name="audit-logs")
    if audit_ch:
        embed = discord.Embed(
            title="🗑️ MESSAGE DELETED",
            description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}\n```\n{message.content[:1500]}\n```",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        await audit_ch.send(embed=embed)

@apex_bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot or not before.guild or before.content == after.content: return
    audit_ch = discord.utils.get(before.guild.text_channels, name="audit-logs")
    if audit_ch:
        embed = discord.Embed(
            title="✏️ MESSAGE EDITED",
            description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}\n**Before:** {before.content[:600]}\n**After:** {after.content[:600]}",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        await audit_ch.send(embed=embed)

# ==============================================================================
# 🤖 BOT 2: AI PILOT 2.0 EVENTS & FEATURES
# ==============================================================================
@ai_pilot_bot.event
async def on_ready():
    print(f"[AI PILOT 2.0] Logged in as {ai_pilot_bot.user} (ID: {ai_pilot_bot.user.id})", flush=True)

    # Register persistent verification view for AI Pilot server
    ai_pilot_bot.add_view(AIPilotVerifyView())
    ai_pilot_bot.add_view(ApexVerifyView())

@ai_pilot_bot.command(name="pilotinfo")
async def pilot_info(ctx):
    await ctx.send("✈️ **AI Pilot Cloud Engine Active** • Dual-Bot Cluster Online 24/7.")

# ==============================================================================
# 🚀 MULTI-BOT CONCURRENT LAUNCHER
# ==============================================================================
async def start_dual_bots():
    print("[CLOUD RUNTIME] Launching APEX PREDATOR & AI PILOT dual-bot cluster...", flush=True)
    tasks = []
    if APEX_TOKEN:
        tasks.append(apex_bot.start(APEX_TOKEN))
    if AI_PILOT_TOKEN:
        tasks.append(ai_pilot_bot.start(AI_PILOT_TOKEN))
    
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("[ERROR] No bot tokens provided in environment variables!", flush=True)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    asyncio.run(start_dual_bots())
