import os
from src.bot import bot
from src.database import create_table
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError(
        "No token found. Please set the DISCORD_BOT_TOKEN environment variable.")

# Create the table if it doesn't exist
create_table()

bot.run(TOKEN)
