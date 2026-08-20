import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.getenv("DISCORD_TOKEN")
headers = {"Authorization": f"Bot {TOKEN}", "User-Agent": "DiscordBot"}

req = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/onboarding", headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(json.dumps(data, indent=2))
