import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.getenv("DISCORD_TOKEN")
headers = {"Authorization": f"Bot {TOKEN}", "User-Agent": "DiscordBot", "Content-Type": "application/json"}

# 1. Guild Overview
req = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690", headers=headers)
with urllib.request.urlopen(req) as resp:
    guild = json.loads(resp.read().decode())
    print("Guild Name:", guild.get("name"))
    print("Guild Features:", guild.get("features"))
    print("Verification Level:", guild.get("verification_level"))

# 2. Member Verification Form (Rule Screening)
try:
    req_screen = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/member-verification", headers=headers)
    with urllib.request.urlopen(req_screen) as resp:
        screening = json.loads(resp.read().decode())
        print("\nMembership Screening:", json.dumps(screening, indent=2))
except Exception as e:
    print("\nMembership Screening fetch error:", e)

# 3. Onboarding
try:
    req_onb = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/onboarding", headers=headers)
    with urllib.request.urlopen(req_onb) as resp:
        onboarding = json.loads(resp.read().decode())
        print("\nOnboarding Settings:", json.dumps(onboarding, indent=2))
except Exception as e:
    print("\nOnboarding fetch error:", e)
