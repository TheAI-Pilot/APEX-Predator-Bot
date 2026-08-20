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

# Additional Professional Roles
EXTRA_ROLES = [
    {"name": "🧠 IGL (In-Game Leader)", "color": 0x3498DB, "hoist": False},
    {"name": "🎯 Sniper Specialist", "color": 0xE67E22, "hoist": False},
    {"name": "⚡ Entry Fragger", "color": 0xE74C3C, "hoist": False},
    {"name": "🛡️ Support / Anchor", "color": 0x2ECC71, "hoist": False},
    {"name": "💻 PC Operator", "color": 0x34495E, "hoist": False},
    {"name": "🎮 Console Operator", "color": 0x9B59B6, "hoist": False},
    {"name": "🔔 Scrim & Tournament Ping", "color": 0xF39C12, "hoist": False},
    {"name": "🔔 Meta Patch Ping", "color": 0x1ABC9C, "hoist": False},
    {"name": "🔔 Stream Alert Ping", "color": 0x9B59B6, "hoist": False}
]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = client.guilds[0]

    print(f"\n=======================================================", flush=True)
    print(f"🎖️ 1. CREATING ENHANCED TACTICAL & PLAYSTYLE ROLES", flush=True)
    print(f"=======================================================\n", flush=True)

    existing_roles = {r.name.lower(): r for r in guild.roles}

    for r_def in EXTRA_ROLES:
        r_name = r_def["name"]
        if r_name.lower() not in existing_roles:
            try:
                role = await guild.create_role(
                    name=r_name,
                    color=discord.Color(r_def["color"]),
                    hoist=r_def["hoist"],
                    reason="Enhanced Warzone tactical role addition"
                )
                print(f"  + [CREATED ROLE] @{role.name}", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error creating @{r_name}: {e}", flush=True)
        else:
            print(f"  [EXISTS] @{r_name}", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"📁 2. ADDING HIGH-VALUE ENHANCED CHANNELS", flush=True)
    print(f"=======================================================\n", flush=True)

    # 1. Inside START HERE -> #faq
    start_here_cat = discord.utils.get(guild.categories, name="🚪 START HERE")
    if start_here_cat:
        if not discord.utils.get(start_here_cat.text_channels, name="server-faq"):
            try:
                faq_ch = await guild.create_text_channel(
                    name="server-faq",
                    category=start_here_cat,
                    topic="Frequently Asked Questions, Voice Rules & Tournament Info"
                )
                faq_embed = discord.Embed(
                    title="❓ APEX UNIVERSE — FREQUENTLY ASKED QUESTIONS",
                    description="Everything you need to know about our Warzone community!\n",
                    color=discord.Color.from_rgb(52, 152, 219)
                )
                faq_embed.add_field(
                    name="❓ How do I find a squad?",
                    value="Head over to <#looking-for-squad> and fill out the pinned LFG template, or hop directly into an open `Warzone Lobby` voice channel.",
                    inline=False
                )
                faq_embed.add_field(
                    name="❓ How do I participate in tournaments?",
                    value="Tournaments are announced in <#tournaments>. Grab the **@Scrim & Tournament Ping** role in <#roles> to receive match alerts.",
                    inline=False
                )
                faq_embed.add_field(
                    name="❓ What are the voice comms rules?",
                    value="Keep callouts clear, concise, and tactical. Zero soundboards or ear-rape during competitive drops.",
                    inline=False
                )
                faq_embed.add_field(
                    name="❓ How do I report a toxic player or cheater?",
                    value="Open a private support desk ticket in <#ticket-support> with video proof or screenshots.",
                    inline=False
                )
                faq_embed.set_footer(text="Apex Universe Staff • Support Desk")
                await faq_ch.send(embed=faq_embed)
                print("  + Created & Populated #server-faq in [START HERE]", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error creating #server-faq: {e}", flush=True)

    # 2. Inside COMMUNITY HUB -> #squad-recruitment
    comm_cat = discord.utils.get(guild.categories, name="💬 COMMUNITY HUB")
    if comm_cat:
        if not discord.utils.get(comm_cat.text_channels, name="squad-recruitment"):
            try:
                recruit_ch = await guild.create_text_channel(
                    name="squad-recruitment",
                    category=comm_cat,
                    topic="Long-term squad, clan & team recruitment"
                )
                recruit_embed = discord.Embed(
                    title="🛡️ CLAN & SQUAD RECRUITMENT DIRECTORY",
                    description="Building a permanent 4-man stack for Warzone Ranked or Scrims? Post your recruitment callouts here!\n\n"
                                "```yaml\n"
                                "Team Name: [Your Clan Tag / Team]\n"
                                "Looking For: IGL / Sniper / Entry Fragger / Anchor\n"
                                "Requirements: Diamond+ / 2.0+ KD / Daily Activity\n"
                                "Region: NA / EU / IN / ASIA\n"
                                "Contact: DM @LeaderTag\n"
                                "```",
                    color=discord.Color.from_rgb(230, 126, 34)
                )
                await recruit_ch.send(embed=recruit_embed)
                print("  + Created & Populated #squad-recruitment in [COMMUNITY HUB]", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error creating #squad-recruitment: {e}", flush=True)

    # 3. Inside WARZONE -> #patch-notes, Duos, Trios & AFK Voice Lobbies
    wz_cat = discord.utils.get(guild.categories, name="🔫 WARZONE")
    if wz_cat:
        # Patch Notes Text Channel
        if not discord.utils.get(wz_cat.text_channels, name="patch-notes"):
            try:
                patch_ch = await guild.create_text_channel(
                    name="patch-notes",
                    category=wz_cat,
                    topic="Official Call of Duty Warzone Patch Notes & Weapon Balances"
                )
                patch_embed = discord.Embed(
                    title="📰 OFFICIAL WARZONE PATCH NOTES & WEAPON BALANCES",
                    description="Stay updated with all official Activision patch notes, weapon tuning updates, shadow nerfs, and season roadmaps!\n\n"
                                "🔔 *Grab the **@Meta Patch Ping** in <#roles> to get notified whenever a new weapon balance patch drops!*",
                    color=discord.Color.from_rgb(26, 188, 156)
                )
                await patch_ch.send(embed=patch_embed)
                print("  + Created & Populated #patch-notes in [WARZONE]", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error creating #patch-notes: {e}", flush=True)

        # Duo & Trio Voice Lobbies
        extra_voice = [
            {"name": "🔊 Duo Comms 1", "limit": 2},
            {"name": "🔊 Duo Comms 2", "limit": 2},
            {"name": "🔊 Trio Comms 1", "limit": 3},
            {"name": "🔊 Trio Comms 2", "limit": 3},
            {"name": "💤 AFK / Gulag Lounge", "limit": 0}
        ]
        for v in extra_voice:
            if not discord.utils.get(wz_cat.voice_channels, name=v["name"]):
                try:
                    await guild.create_voice_channel(
                        name=v["name"],
                        category=wz_cat,
                        user_limit=v["limit"]
                    )
                    print(f"  + Created Voice Channel: {v['name']} (limit: {v['limit']})", flush=True)
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"  - Error creating {v['name']}: {e}", flush=True)

    # 4. Inside EVENTS & TOURNAMENTS -> #hall-of-fame
    events_cat = discord.utils.get(guild.categories, name="🏆 EVENTS & TOURNAMENTS")
    if events_cat:
        if not discord.utils.get(events_cat.text_channels, name="hall-of-fame"):
            try:
                hof_ch = await guild.create_text_channel(
                    name="hall-of-fame",
                    category=events_cat,
                    topic="Tournament Champions, Trophy Records & MVP Leaderboards"
                )
                hof_embed = discord.Embed(
                    title="🏆 APEX UNIVERSE — HALL OF FAME",
                    description="Dedicated to the legends and champions of Apex Universe competitive tournaments!\n\n"
                                "🥇 **Season 1 Kill-Race Champions**: *TBD (Sign up in <#tournaments>)*\n"
                                "🥈 **Season 1 Runners-Up**: *TBD*\n"
                                "🎖️ **Tournament MVP (Most Eliminations)**: *TBD*\n\n"
                                "Compete in official scrims and tournaments to earn your spot in the Hall of Fame and the exclusive **@Warzone Champion** role!",
                    color=discord.Color.from_rgb(241, 196, 15)
                )
                await hof_ch.send(embed=hof_embed)
                print("  + Created & Populated #hall-of-fame in [EVENTS & TOURNAMENTS]", flush=True)
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"  - Error creating #hall-of-fame: {e}", flush=True)

    # 5. Update #roles to include the new playstyle & notification badges
    roles_ch = discord.utils.get(guild.text_channels, name="roles")
    if roles_ch:
        try:
            await roles_ch.purge(limit=10)
        except:
            pass

        roles_embed = discord.Embed(
            title="🏷️ SPECIALIZATION & NOTIFICATION ROLES",
            description="Customize your squad profile and ping preferences below!\n\n"
                        "### 🎖️ Squad Specializations & Roles:\n"
                        "• **🧠 @IGL (In-Game Leader)** — Tactical shot-caller\n"
                        "• **🎯 @Sniper Specialist** — Long-range precision marksman\n"
                        "• **⚡ @Entry Fragger** — Aggressive SMG point-man\n"
                        "• **🛡️ @Support / Anchor** — Squad anchor & buy-station economy\n\n"
                        "### 💻 Hardware & Platform:\n"
                        "• **💻 @PC Operator** — PC / Keyboard & Mouse\n"
                        "• **🎮 @Console Operator** — PlayStation / Xbox / Controller\n\n"
                        "### 🔔 Notification Badges:\n"
                        "• **🔔 @Scrim & Tournament Ping** — Scrim & tournament alerts\n"
                        "• **🔔 @Meta Patch Ping** — Weapon balance & patch alerts\n"
                        "• **🔔 @Stream Alert Ping** — Live stream notifications\n",
            color=discord.Color.from_rgb(26, 188, 156)
        )
        roles_embed.set_footer(text="Click the reaction buttons to claim your roles!")
        await roles_ch.send(embed=roles_embed)
        print("  + Refreshed #roles with enhanced playstyle and ping roles!", flush=True)

    print(f"\n=======================================================", flush=True)
    print(f"✨ ALL ENHANCED CHANNELS & ROLES SUCCESSFULLY DEPLOYED!", flush=True)
    print(f"=======================================================\n", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
