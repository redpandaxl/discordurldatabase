import discord
from discord.ext import commands
from src.processing import extract_and_log_urls, load_last_processed, save_last_processed

# Setup bot with command prefix and intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


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
