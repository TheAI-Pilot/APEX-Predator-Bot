import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_file = r"C:\Users\aaram\.gemini\antigravity\brain\15b2e825-65e4-43f9-8634-67a3a782d65b\.system_generated\logs\transcript.jsonl"
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        content = obj.get("content", "")
        if "Moderator" in content or "Majors" in content or "Members:" in content:
            if "ID:" in content:
                print(f"Step {obj.get('step_index')}:\n{content[:600]}\n---")
