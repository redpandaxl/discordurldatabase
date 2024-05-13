
import os
import discord
from discord.ext import commands
import re
from datetime import datetime
import json

# Setup bot with command prefix and intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

LAST_PROCESSED_FILE = 'last_processed.json'


def load_last_processed():
    """Load the last processed message IDs from a JSON file."""
    if os.path.exists(LAST_PROCESSED_FILE):
        with open(LAST_PROCESSED_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


def save_last_processed(data):
    """Save the last processed message IDs to a JSON file."""
    with open(LAST_PROCESSED_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def extract_and_log_urls(message):
    """Function to extract URLs from a message and log them to a CSV file."""
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    urls = url_pattern.findall(message.content)

    if urls:
        with open('urls_data.csv', 'a', encoding='utf-8') as file:
            for url in urls:
                data = {
                    "channel_name": message.channel.name,
                    "channel_id": message.channel.id,
                    "timestamp": datetime.fromtimestamp(float(message.created_at.timestamp())).strftime('%Y-%m-%d %H:%M:%S'),
                    "url": url,
                    "author": f"{message.author.name}#{message.author.discriminator}",
                    "message_content": message.content
                }
                file.write(
                    f"{data['timestamp']},{data['channel_name']},{data['channel_id']},{data['url']},{data['author']},\"{data['message_content']}\"\n")


@bot.command(name='fetch_history')
async def fetch_history(ctx, limit: int = 1000):
    await ctx.send("Command to fetch and log historical messages for URLs. Starting...")
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to execute this command.")
        return

    last_processed = load_last_processed()
    channels = ctx.guild.text_channels
    for channel in channels:
        last_message_id = last_processed.get(str(channel.id), None)
        try:
            if last_message_id:
                async for message in channel.history(limit=limit, after=discord.Object(id=last_message_id)):
                    extract_and_log_urls(message)
                    last_processed[str(channel.id)] = message.id
            else:
                async for message in channel.history(limit=limit):
                    extract_and_log_urls(message)
                    last_processed[str(channel.id)] = message.id
            await ctx.send(f"Processed history for {channel.name}.")
        except discord.errors.Forbidden:
            await ctx.send(f"Access denied to {channel.name}. Skipping...")
    await ctx.send("Completed!")
    save_last_processed(last_processed)


@bot.event
async def on_message(message):
    """Event listener for new messages to log URLs in real-time."""
    if message.author == bot.user:
        return
    extract_and_log_urls(message)
    # This is important to allow command processing
    await bot.process_commands(message)

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError(
        "No token found. Please set the DISCORD_BOT_TOKEN environment variable.")

bot.run(TOKEN)
