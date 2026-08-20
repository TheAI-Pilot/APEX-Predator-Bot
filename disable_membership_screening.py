import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.getenv("DISCORD_TOKEN")
headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "DiscordBot",
    "Content-Type": "application/json"
}

# 1. Disable member-verification (Rule Screening & Lobby Questions)
payload = {
    "enabled": False,
    "form_fields": [],
    "description": None
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    "https://discord.com/api/v10/guilds/1511457449360752690/member-verification",
    data=data,
    headers=headers,
    method="PATCH"
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print("Successfully disabled Membership Screening!")
        print("Result:", json.dumps(res, indent=2))
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f"HTTP Error {e.code}: {err_body}")
except Exception as e:
    print("Error:", e)

# 2. Verify guild features
req_g = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690", headers=headers)
with urllib.request.urlopen(req_g) as resp:
    guild = json.loads(resp.read().decode())
    print("\nUpdated Guild Features:", guild.get("features"))
