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

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    # set status (currently broken)
    # print when ready
    print(f'{client.user} has connected to Discord!')
    
    d = {}
    msg = []
    
    for channel in client.guilds[0].text_channels:
        print(channel.name)
        
        # create list of all messages in channel history
        async for x in channel.history(limit=10000000000000000):
            msg.append(x)
    
    
    
    for m in msg:
        if m.author.display_name in d:
            d[m.author.display_name]+=1
        else:
            d[m.author.display_name]=1

    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
    
    for k,v in d.items():
        print(k, v)
    

        
    

client.run(TOKEN)