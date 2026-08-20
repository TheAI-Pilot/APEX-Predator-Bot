import os
import sys
import json
import urllib.request
import discord

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

TOKEN = os.getenv("DISCORD_TOKEN")
headers = {"Authorization": f"Bot {TOKEN}", "User-Agent": "DiscordBot"}

# 1. Fetch Audit Logs
print("=== AUDIT LOGS ===")
try:
    req = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/audit-logs?limit=100", headers=headers)
    with urllib.request.urlopen(req) as resp:
        audit = json.loads(resp.read().decode())
        entries = audit.get("audit_log_entries", [])
        for e in entries:
            # Action 25 is MEMBER_ROLE_UPDATE, Action 24 is MEMBER_UPDATE
            if e.get("action_type") in [25, 24, 20]: # 20 is ROLE_CREATE
                print(f"Action: {e.get('action_type')} | User: {e.get('user_id')} | Target: {e.get('target_id')} | Changes: {e.get('changes')}")
except Exception as e:
    print("Audit log query error:", e)

# 2. Fetch Members
print("\n=== MEMBERS WITH ROLES ===")
req = urllib.request.Request("https://discord.com/api/v10/guilds/1511457449360752690/members?limit=1000", headers=headers)
with urllib.request.urlopen(req) as resp:
    members = json.loads(resp.read().decode())
    for m in members:
        user = m.get("user", {})
        if user.get("bot"):
            continue
        roles = m.get("roles", [])
        print(f"Member: {user.get('username')}#{user.get('discriminator')} | Nick: {m.get('nick')} | ID: {user.get('id')} | Roles: {roles}")
