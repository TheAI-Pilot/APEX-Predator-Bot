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

# Fetch valid channel IDs in START HERE
req_ch = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/channels", headers=headers)
with urllib.request.urlopen(req_ch) as resp:
    channels = json.loads(resp.read().decode())
    rules_ch = next((c for c in channels if c['name'] == 'rules'), None)
    ann_ch = next((c for c in channels if c['name'] == 'announcements'), None)
    verify_ch = next((c for c in channels if c['name'] == 'verify-here'), None)
    gen_ch = next((c for c in channels if c['name'] == 'general-chat'), None)

default_channels = []
if rules_ch: default_channels.append(rules_ch['id'])
if ann_ch: default_channels.append(ann_ch['id'])
if verify_ch: default_channels.append(verify_ch['id'])
if gen_ch: default_channels.append(gen_ch['id'])

print("Default onboarding channels to set:", default_channels)

payload = {
    "prompts": [],
    "default_channel_ids": default_channels,
    "enabled": False,
    "mode": 0
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    "https://discord.com/api/v10/guilds/1511457449360752690/onboarding",
    data=data,
    headers=headers,
    method="PUT"
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        print("Successfully updated onboarding settings!")
        print("Enabled:", result.get("enabled"))
        print("Prompts count:", len(result.get("prompts", [])))
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f"HTTP Error {e.code}: {err_body}")
except Exception as e:
    print("Error:", e)
