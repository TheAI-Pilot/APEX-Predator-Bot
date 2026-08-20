import os
import sys
import asyncio
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

ROLE_DEFINITIONS = {
    # Squad Playstyles
    "claim_role_igl": "🧠 IGL (In-Game Leader)",
    "claim_role_sniper": "🎯 Sniper Specialist",
    "claim_role_entry": "⚡ Entry Fragger",
    "claim_role_support": "🛡️ Support / Anchor",
    # Platform
    "claim_role_pc": "💻 PC Operator",
    "claim_role_console": "🎮 Console Operator",
    # Pings
    "claim_role_scrim": "🔔 Scrim & Tournament Ping",
    "claim_role_patch": "🔔 Meta Patch Ping",
    "claim_role_stream": "🔔 Stream Alert Ping"
}

class SquadRolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🧠 IGL (Shot-Caller)", style=discord.ButtonStyle.primary, custom_id="claim_role_igl")
    async def btn_igl(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🧠 IGL (In-Game Leader)")

    @discord.ui.button(label="🎯 Sniper Specialist", style=discord.ButtonStyle.primary, custom_id="claim_role_sniper")
    async def btn_sniper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🎯 Sniper Specialist")

    @discord.ui.button(label="⚡ Entry Fragger", style=discord.ButtonStyle.danger, custom_id="claim_role_entry")
    async def btn_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "⚡ Entry Fragger")

    @discord.ui.button(label="🛡️ Support / Anchor", style=discord.ButtonStyle.success, custom_id="claim_role_support")
    async def btn_support(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🛡️ Support / Anchor")

    async def toggle_role(self, interaction: discord.Interaction, role_name: str):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(f"❌ Role `{role_name}` not found!", ephemeral=True)
            return

        if role in member.roles:
            await member.remove_roles(role, reason="Self-unclaimed via Specialty Roles Hub")
            await interaction.response.send_message(f"🗑️ Removed **{role.mention}** from your profile.", ephemeral=True)
        else:
            await member.add_roles(role, reason="Self-claimed via Specialty Roles Hub")
            await interaction.response.send_message(f"✅ Awarded **{role.mention}**! Check your profile.", ephemeral=True)

class PlatformAndPingsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💻 PC Operator", style=discord.ButtonStyle.secondary, custom_id="claim_role_pc")
    async def btn_pc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "💻 PC Operator")

    @discord.ui.button(label="🎮 Console Operator", style=discord.ButtonStyle.secondary, custom_id="claim_role_console")
    async def btn_console(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🎮 Console Operator")

    @discord.ui.button(label="🔔 Scrim & Tourney Ping", style=discord.ButtonStyle.secondary, custom_id="claim_role_scrim")
    async def btn_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🔔 Scrim & Tournament Ping")

    @discord.ui.button(label="🔔 Meta Patch Ping", style=discord.ButtonStyle.secondary, custom_id="claim_role_patch")
    async def btn_patch(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🔔 Meta Patch Ping")

    @discord.ui.button(label="🔔 Stream Alert Ping", style=discord.ButtonStyle.secondary, custom_id="claim_role_stream")
    async def btn_stream(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "🔔 Stream Alert Ping")

    async def toggle_role(self, interaction: discord.Interaction, role_name: str):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(f"❌ Role `{role_name}` not found!", ephemeral=True)
            return

        if role in member.roles:
            await member.remove_roles(role, reason="Self-unclaimed via Specialty Roles Hub")
            await interaction.response.send_message(f"🗑️ Removed **{role.mention}** from your preferences.", ephemeral=True)
        else:
            await member.add_roles(role, reason="Self-claimed via Specialty Roles Hub")
            await interaction.response.send_message(f"✅ Subscribed to **{role.mention}**!", ephemeral=True)

@client.event
async def on_ready():
    guild = client.guilds[0]
    print(f"Deploying to {guild.name} ({guild.id})", flush=True)

    roles_ch = None
    for c in guild.text_channels:
        if "role" in c.name.lower() or "specialty" in c.name.lower():
            roles_ch = c
            break

    if not roles_ch:
        print("❌ Roles channel not found!", flush=True)
        await client.close()
        return

    print(f"Purging and deploying interactive role claim system to #{roles_ch.name}...", flush=True)
    try:
        await roles_ch.purge(limit=20)
    except:
        pass

    # 1. Server Booster VIP Perks Embed
    booster_embed = discord.Embed(
        title="💎 SERVER BOOSTER VIP PERKS & REWARDS",
        description="Support **Apex Universe** with a Discord Nitro Server Boost to instantly unlock exclusive VIP rewards, private lounges, and enhanced voice comms!\n\n"
                    "### 🎁 Exclusive Booster Perks:\n"
                    "• **👑 Elevated VIP Status**: Stand out at the top of the member list with a shiny booster gem.\n"
                    "• **🛋️ Private Supporter Lounge**: Hang out directly with leadership and content creators in exclusive rooms.\n"
                    "• **⚡ Early Tournament Registration**: Guaranteed priority slots in official kill-race scrims.\n"
                    "• **🎙️ Ultra HD 384kbps Voice Audio**: Crystal-clear tactical comms + 1080p 60fps screen streaming.\n"
                    "• **🎨 Custom Emoji & Soundboard Freedom**: Use external emojis and animated soundboard audio anywhere.\n\n"
                    "✨ *Boost the server by clicking the Server Name at the top left ➔ 'Server Boost'!*",
        color=discord.Color.from_rgb(244, 127, 255)
    )
    if guild.icon:
        booster_embed.set_thumbnail(url=guild.icon.url)
    booster_embed.set_image(url="https://media.giphy.com/media/26tOZ42Mg6pbTUPHW/giphy.gif")
    await roles_ch.send(embed=booster_embed)
    await asyncio.sleep(1)

    # 2. Squad Playstyle Specializations (Interactive Buttons)
    squad_embed = discord.Embed(
        title="🎖️ SQUAD COMBAT ROLES & SPECIALIZATIONS",
        description="Claim your tactical combat role so squad leaders know your playstyle when forming squads in <#looking-for-squad>!\n\n"
                    "• **🧠 @IGL (In-Game Leader)** — Tactical captain, rotations, zone prediction & macro shot-caller.\n"
                    "• **🎯 @Sniper Specialist** — Long-range precision marksman & designated spotter.\n"
                    "• **⚡ @Entry Fragger** — Point-man, aggressive SMG rusher, room clearer & first-contact slayer.\n"
                    "• **🛡️ @Support / Anchor** — Buy-station economy, UAV callouts & squad anchor.\n\n"
                    "⚠️ **Role Lifecycle Policy**:\n"
                    "*These roles are active while you are a member of the server. If you leave the server, roles naturally reset and can be re-claimed here upon rejoining anytime!*\n\n"
                    "👇 **Click a button below to 1-Click Toggle your role:**",
        color=discord.Color.from_rgb(52, 152, 219)
    )
    await roles_ch.send(embed=squad_embed, view=SquadRolesView())
    await asyncio.sleep(1)

    # 3. Hardware Platform & Notification Pings (Interactive Buttons)
    pings_embed = discord.Embed(
        title="💻 PLATFORM & NOTIFICATION PREFERENCES",
        description="Select your gaming platform and opt into specific server alerts:\n\n"
                    "### 🎮 Hardware Platform:\n"
                    "• **💻 @PC Operator** — PC / Keyboard & Mouse\n"
                    "• **🎮 @Console Operator** — PlayStation / Xbox / Controller\n\n"
                    "### 🔔 Notification Badges:\n"
                    "• **🔔 @Scrim & Tournament Ping** — Alerts for weekly tournament brackets & custom scrims.\n"
                    "• **🔔 @Meta Patch Ping** — Official weapon balance updates, buffs, nerfs & patch notes.\n"
                    "• **🔔 @Stream Alert Ping** — Live broadcast & community stream alerts.\n\n"
                    "👇 **Click a button below to subscribe/unsubscribe:**",
        color=discord.Color.from_rgb(46, 204, 113)
    )
    pings_embed.set_footer(text="Apex Universe Automated Role Engine • 1-Click Toggle")
    await roles_ch.send(embed=pings_embed, view=PlatformAndPingsView())

    print("✨ Specialty roles interactive hub successfully deployed!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
