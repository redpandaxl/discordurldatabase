import json
import os
import re
from datetime import datetime
LAST_PROCESSED_FILE = 'data/last_processed.json'


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
        with open('data/urls_data.csv', 'a', encoding='utf-8') as file:
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
