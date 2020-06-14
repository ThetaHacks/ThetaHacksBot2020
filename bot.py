import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'hi':
        await message.channel.send("Hello %s!" % message.author.display_name)

    elif message.content.lower() == '!signup':
        await message.channel.send("Go to %s to sign up!" % "{nonexitent link}")

    elif message.content.lower() == '!info':
        await message.channel.send("ThetaHacks is a high school hackathon held in the Bay Area. More information coming soon.")

    elif message.content[0] == '!':
        await message.channel.send("Invalid command. Valid commands are !signup and !info")

client.run(TOKEN)
