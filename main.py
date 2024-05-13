import os
from src.bot import bot

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError(
        "No token found. Please set the DISCORD_BOT_TOKEN environment variable.")

bot.run(TOKEN)
