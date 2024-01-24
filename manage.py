import discord
from discord.ext import commands, tasks
import asyncio
import random

TOKEN = ""
GUILD_ID = 123456789012345678  # Replace with your server ID
SPAWN_CHANNEL_ID = 987654321098765432  # Replace with your spawn channel ID
COLLECTOR_ROLE_ID = 123456789012345678  # Replace with your collector role ID

bot = commands.Bot(command_prefix='$')

# Cooldown duration in seconds
COOLDOWN_DURATION = 30

# Flag to indicate whether a spawn is currently happening
spawn_in_progress = False

@bot.event
async def on_ready():
    print(f'Logged into account: {bot.user.name}')

@tasks.loop(minutes=1)
async def spawn_cooldown():
    global spawn_in_progress
    spawn_in_progress = True
    await asyncio.sleep(COOLDOWN_DURATION)
    spawn_in_progress = False

@bot.command(name='spawn', help='Trigger a rare/regional spawn')
async def spawn(ctx):
    global spawn_in_progress

    if spawn_in_progress:
        await ctx.send("A spawn is currently in progress. Please wait.")
    else:
        await ctx.send("Rare/regional spawn is happening! Collectors, get ready!")
        await spawn_cooldown.start()

@bot.event
async def on_message(message):
    global spawn_in_progress

    if message.guild and message.guild.id == GUILD_ID and message.channel.id == SPAWN_CHANNEL_ID:
        collector_role = message.guild.get_role(COLLECTOR_ROLE_ID)

        if collector_role in message.author.roles and spawn_in_progress:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you can't type during a rare/regional spawn!")

    await bot.process_commands(message)

bot.run(TOKEN)
