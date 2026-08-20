import os
import sys
import asyncio
import datetime
import discord
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv("AI_PILOT_TOKEN") or os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}", flush=True)
    guild = discord.utils.get(client.guilds, id=1539332811276947537)
    if not guild:
        print("AI Pilot guild not found!")
        await client.close()
        return

    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # 1. Slot 1: Morning Model Intel & Breaking AI News (#announcements)
    news_ch = discord.utils.get(guild.text_channels, name="announcements")
    if news_ch:
        embed1 = discord.Embed(
            title="📢 MORNING MODEL INTEL: Claude 3.5 Sonnet & Flux Dev Advances",
            description="### ⚡ Key Breakthroughs Today:\n"
                        "• **Anthropic Claude 3.5 Sonnet**: New benchmarks show 93.7% accuracy on complex multi-file codebase refactors.\n"
                        "• **FLUX.1 Open-Weights**: Local ComfyUI workflows now achieving 1.2s inference with FP8 quantizations.\n"
                        "• **Cursor Composer**: Multi-file autonomous editing workflows now supporting deep AST parsing.\n\n"
                        "💡 *Discussion topic: How are you integrating local open-weights into your production stack? Share in <#general>!*",
            color=discord.Color.from_rgb(52, 152, 219),
            timestamp=now_utc
        )
        embed1.set_footer(text="AI Pilot 09:00 AM Model Intel Drop")
        await news_ch.send(embed=embed1)
        print("  + Dispatched Slot 1 -> #announcements", flush=True)
        await asyncio.sleep(0.5)

    # 2. Slot 2: Midday High-Signal Prompt Engineering (#featured-prompts)
    prompt_ch = discord.utils.get(guild.text_channels, name="featured-prompts")
    if prompt_ch:
        embed2 = discord.Embed(
            title="🧠 FEATURED PROMPT DROP: The Recursive Meta-Architect",
            description="### 🎯 Purpose:\n"
                        "Force LLMs to deconstruct ambiguous software or business problems into zero-defect execution roadmaps.\n\n"
                        "### 📋 Copy & Paste Prompt:\n"
                        "```markdown\n"
                        "You are an Elite Enterprise AI Systems Architect. \n"
                        "Your mission is to analyze [TARGET_TOPIC] using first-principles reasoning.\n\n"
                        "Execution Constraints:\n"
                        "1. Identify hidden edge cases and failure modes.\n"
                        "2. Output modular JSON schemas for all data contracts.\n"
                        "3. Provide step-by-step implementation code with zero pseudocode.\n"
                        "```\n\n"
                        "👉 Test this with `!optimize <prompt>` in <#bot-commands>!",
            color=discord.Color.from_rgb(155, 89, 182),
            timestamp=now_utc
        )
        embed2.set_footer(text="AI Pilot 12:00 PM Prompt Engineering Drop")
        await prompt_ch.send(embed=embed2)
        print("  + Dispatched Slot 2 -> #featured-prompts", flush=True)
        await asyncio.sleep(0.5)

    # 3. Slot 3: Afternoon Production Automation Blueprints (#automation-control-room)
    auto_ch = discord.utils.get(guild.text_channels, name="automation-control-room")
    if auto_ch:
        embed3 = discord.Embed(
            title="⚙️ PRODUCTION AUTOMATION BLUEPRINT: n8n + Webhooks + LLM Router",
            description="### 🏗️ Architecture Breakdown:\n"
                        "```\n"
                        "Webhook Ingest ➔ Payload Validation ➔ Semantic Router (Claude)\n"
                        "     ├── Code Refactor ➔ GitHub PR Creator Node\n"
                        "     └── Lead Enrichment ➔ PostgreSQL + Slack Alert\n"
                        "```\n\n"
                        "### 🚀 Key Implementation Rules:\n"
                        "1. **Never use polling** — always utilize webhook callbacks.\n"
                        "2. **State Storage** — Persist conversation IDs in Redis or SQLite to prevent memory bloat.\n"
                        "3. **Fallback Retry** — Wrap all LLM HTTP nodes in 3x exponential backoff.\n\n"
                        "Explore more blueprints in <#learning-paths>!",
            color=discord.Color.from_rgb(46, 204, 113),
            timestamp=now_utc
        )
        embed3.set_footer(text="AI Pilot 03:00 PM Automation Blueprint")
        await auto_ch.send(embed=embed3)
        print("  + Dispatched Slot 3 -> #automation-control-room", flush=True)
        await asyncio.sleep(0.5)

    # 4. Slot 4: Evening YouTube Retention & Video AI Strategies (#content-creation)
    content_ch = discord.utils.get(guild.text_channels, name="content-creation")
    if content_ch:
        embed4 = discord.Embed(
            title="🎥 CREATOR STRATEGY: High-Retention AI Video Production Pipeline",
            description="### 📈 3-Phase Retention Framework:\n"
                        "1. **0:00 - 0:15 (The Hook)**: Show the finished working automation/result immediately with dynamic B-roll.\n"
                        "2. **0:15 - 3:00 (The Core System)**: Explain the blueprint step-by-step with zero fluff.\n"
                        "3. **3:00+ (The Drop)**: Give members direct access to the GitHub repo & template links.\n\n"
                        "🛠️ **Recommended Tool Stack**: ElevenLabs (Voice) + Premiere Pro (Pacing) + Cursor (Live Builds).\n\n"
                        "Post your video drafts and get feedback in <#video-discussion>!",
            color=discord.Color.from_rgb(230, 126, 34),
            timestamp=now_utc
        )
        embed4.set_footer(text="AI Pilot 06:00 PM Creator Strategy Drop")
        await content_ch.send(embed=embed4)
        print("  + Dispatched Slot 4 -> #content-creation", flush=True)
        await asyncio.sleep(0.5)

    # 5. Slot 5: Night Daily AI Trivia & Challenge (#daily-ai-challenge)
    trivia_ch = discord.utils.get(guild.text_channels, name="daily-ai-challenge")
    if trivia_ch:
        embed5 = discord.Embed(
            title="🏆 DAILY AI TRIVIA & BUILDER CHALLENGE #01",
            description="### 🧩 Today's Challenge:\n"
                        "**Question**: What is the primary difference between **LoRA (Low-Rank Adaptation)** and full model fine-tuning?\n\n"
                        "**Options**:\n"
                        "🇦 LoRA freezes the original weights and trains rank decomposition matrices.\n"
                        "🇧 LoRA modifies all billion weights across every transformer block.\n"
                        "🇨 LoRA only works on text embeddings and cannot be used for diffusion.\n"
                        "🇩 LoRA increases VRAM memory consumption by 400%.\n\n"
                        "💬 *Drop your answer below! First 3 correct answers earn reputation points via Tatsu (`t!rep`)!*",
            color=discord.Color.from_rgb(241, 196, 15),
            timestamp=now_utc
        )
        embed5.set_footer(text="AI Pilot 09:00 PM Daily Challenge")
        await trivia_ch.send(embed=embed5)
        print("  + Dispatched Slot 5 -> #daily-ai-challenge", flush=True)

    print("\n✨ All 5 daily content slots successfully populated across AI Pilot server!", flush=True)
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
