import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "DiscordBot",
    "Content-Type": "application/json"
}

# Desired Order below Admin (Top to Bottom):
DESIRED_ORDER = [
    "⭐ Task Force Director",
    "🛡️ Tactical Enforcer",
    "🎯 Combat Advisor",
    "🔱 Warzone Veteran",
    "🏆 Warzone Champion",
    "🌟 Highlight MVP",
    "⚔️ Scrim Contender",
    "⚔️ Tournament Contender",
    "💎 Community Elite",
    "🔥 Daily Grinder",
    "🎬 Clip Creator",
    "🪖 Verified Operator",
    "🔫 Warzone Slayer",
    "🧠 IGL (In-Game Leader)",
    "🎯 Sniper Specialist",
    "⚡ Entry Fragger",
    "🛡️ Support / Anchor",
    "💻 PC Operator",
    "🎮 Console Operator",
    "🔔 Scrim & Tournament Ping",
    "🔔 Meta Patch Ping",
    "🔔 Stream Alert Ping",
    "⛓️ Gulag Inmate"
]

# Fetch current roles
req = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/roles", headers=headers)
with urllib.request.urlopen(req) as resp:
    roles = json.loads(resp.read().decode())

bot_role = next((r for r in roles if r.get("managed") and r["name"] == "APEX PREDATOR"), None)
bot_pos = bot_role["position"] if bot_role else 33

# Only reorder roles strictly below bot_pos and not managed
editable_roles = [r for r in roles if not r.get("managed") and r["name"] != "@everyone" and r["position"] < bot_pos]

matched_order = []
for name in DESIRED_ORDER:
    for r in editable_roles:
        if r["name"].lower() == name.lower() and r not in matched_order:
            matched_order.append(r)
            break

for r in editable_roles:
    if r not in matched_order:
        matched_order.append(r)

# In Discord API: If we set them with higher relative positions, they jump above the bot managed roles!
# We start from 32 downwards:
payload = []
for idx, r in enumerate(matched_order):
    pos = 32 - idx
    payload.append({"id": r["id"], "position": pos})

data = json.dumps(payload).encode('utf-8')
patch_req = urllib.request.Request(
    "https://discord.com/api/v10/guilds/1511457449360752690/roles",
    data=data,
    headers=headers,
    method="PATCH"
)

try:
    with urllib.request.urlopen(patch_req) as resp:
        updated_roles = json.loads(resp.read().decode())
        print("\n✨ Successfully rearranged all roles above bot integration roles!")
        sorted_res = sorted(updated_roles, key=lambda x: x['position'], reverse=True)
        print("\nNew Server Role Hierarchy:")
        for r in sorted_res:
            print(f"  [{r['position']:02d}] @{r['name']:<30} | Managed: {r.get('managed', False)}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
except Exception as e:
    print("Error:", e)
