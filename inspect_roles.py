import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.getenv("DISCORD_TOKEN")
headers = {"Authorization": f"Bot {TOKEN}", "User-Agent": "DiscordBot"}

req = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/roles", headers=headers)
with urllib.request.urlopen(req) as resp:
    roles = json.loads(resp.read().decode())
    roles_sorted = sorted(roles, key=lambda x: x['position'], reverse=True)
    print("Current Role Hierarchy (Top to Bottom):")
    for r in roles_sorted:
        print(f"[{r['position']:02d}] @{r['name']:<30} | ID: {r['id']} | Managed: {r.get('managed', False)}")
