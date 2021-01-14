import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import random


# get tokens as environment variables (for security)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# initiate client

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'), intents=intents)
client.v = 0
client.v2 = 0
client.v3 = 0
client.v4 = 0
client.v5 = 0
client.sent = False
client.roledict = {}
client.roledict2 = {"🤖": "AI/Machine Learning", "🌐": "Web Development",
                    "🎮": "Game Design", "📈": "Data Science", "🔎": "Algorithms"}

for cog in ['cogs.events', 'cogs.commands']:
    try:
        client.load_extension(cog)
    except e:
        print(f'Could not load cog {cog} for reason:{e}')

# run client
client.run(TOKEN)
