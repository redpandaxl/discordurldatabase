import discord
import re
from datetime import datetime
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError(
        "No token found. Please set the DISCORD_BOT_TOKEN environment variable.")

intents = discord.Intents.default()
intents.messages = True  # Subscribe to messages
intents.message_content = True  # Needed to access message content


class URLScraperBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        # Skip messages sent by the bot
        if message.author == self.user:
            return

        # Regex to extract URLs
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        urls = url_pattern.findall(message.content)

        if urls:
            for url in urls:
                data = {
                    "channel_name": message.channel.name,
                    "channel_id": message.channel.id,
                    "timestamp": datetime.fromtimestamp(float(message.created_at.timestamp())).strftime('%Y-%m-%d %H:%M:%S'),
                    "url": url,
                    "author": f"{message.author.name}#{message.author.discriminator}",
                    "message_content": message.content
                }
                print(data)
                with open('urls_data.csv', 'a') as file:
                    file.write(
                        f"{data['timestamp']},{data['channel_name']},{data['channel_id']},{data['url']},{data['author']},\"{data['message_content']}\"\n")


client = URLScraperBot(intents=intents)
client.run(TOKEN)
