import glob
import os
import re

for f in glob.glob("*.py"):
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    new_content = re.sub(r'["\']MTUzOTkyODQwMjIwOTkzNTQzMA[^"\']+["\']', 'os.getenv("DISCORD_TOKEN")', content)
    with open(f, "w", encoding="utf-8") as file:
        file.write(new_content)

print("Scrubbed all python files.")
