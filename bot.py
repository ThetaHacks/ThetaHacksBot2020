import os

import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
client.v = 0


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    await client.change_presence(activity=discord.Game(name='Made by Andy Li'))


@client.event
async def on_message(message):

    # ! COMMANDS

    if message.author == client.user:
        return

    # HI

    if message.content.lower() in ['hi', 'hello', 'hola']:
        await message.channel.send("Hello %s!" % message.author.display_name)

    # SIGNUP

    elif message.content.lower() == '!signup':
        embed = discord.Embed(
            title="Sign Up", description="Go to [some link] to sign up!", color=0xb134eb)
        await message.channel.send(embed=embed)

    # INFO

    elif message.content.lower() == '!info':
        embed = discord.Embed(
            title="Information", description="ThetaHacks is a high school hackathon held in the Bay Area. More information coming soon.", color=0xc0e8f9)
        await message.channel.send(embed=embed)

    # HELP

    elif message.content.lower() == '!help':
        embed = discord.Embed(
            title="Help", description="Valid commands:\n`!signup` - Signup form link\n`!info` - ThetaHacks information\n`!help` - View valid commands\n`!stats` - See server statistics", color=0x0027ff)
        await message.channel.send(embed=embed)

    # STATS

    elif message.content.lower() == '!stats':
        a = {}
        a["testing"] = 0
        for member in message.author.guild.members:
            for role in member.roles:
                if str(role.name) not in a.keys():
                    a[str(role.name)] = 1
                else:
                    a[str(role.name)] += 1

        a["Attendees"] -= a["testing"] + a["ThetaHacks Bot"]
        text = "\n".join("`%i` %s" % (v, k) for k, v in a.items() if k not in [
                         "testing", "ThetaHacks Bot", "@everyone"])

        embed = discord.Embed(
            title="ThetaHacks Stats", description=text, color=0x00ff9d)
        await message.channel.send(embed=embed)

    # SUDO COMMANDS

    elif message.content.lower().split(" ")[0] == "sudo":
        admin = get(message.author.guild.roles, name="Admins")
        mod = get(message.author.guild.roles, name="Senior Mods")
        bot = get(message.author.guild.roles, name="ThetaHacks Bot")
        if admin in message.author.roles or bot in message.author.roles or mod in message.author.roles:
            temp = message.content.lower().split(" ")

            # CLEAR

            if temp[1] == "clear":
                if len(temp) == 2:
                    await message.channel.send("Invalid arguments for command `clear`.")
                elif temp[2] == "all":
                    msg = []
                    async for x in message.channel.history():
                        msg.append(x)
                    await message.channel.delete_messages(msg)
                    await message.channel.send("All messages deleted by %s." % message.author.display_name)
                else:
                    try:
                        n = int(temp[2])
                        if n <= 0 or not n:
                            await message.channel.send("Invalid arguments for command `clear`.")
                        else:
                            msg = []
                            async for x in message.channel.history(limit=n+1):
                                msg.append(x)
                            await message.channel.delete_messages(msg)

                            await message.channel.send("`%i` messages deleted by %s" % (n, message.author.display_name))
                    except:
                        await message.channel.send("Invalid arguments for command `clear`.")

            if temp[1] == "kick":
                if len(temp) == 2:
                    await message.channel.send("Invalid arguments for command `kick`.")
                try:
                    u = message.mentions[0]
                except:
                    await message.channel.send("Invalid arguments for command `kick`.")
                else:
                    if len(temp) > 3:
                        r = " ".join(temp[3:])
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was kicked by %s.\nReason: %s." % (temp[2], message.author.display_name, r), color=0xffa600)
                            embed2 = discord.Embed(
                                title="", description="You were kicked from the `Official ThetaHacks Server` by %s.\nReason: %s." % (message.author.display_name, r), color=0xffa600)

                            await u.send(embed=embed2)
                            await message.author.guild.kick(user=u, reason=r)
                            await message.channel.send(embed=embed)

                    else:
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was kicked by %s.\nNo reason provided." % (temp[2], message.author.display_name), color=0xffa600)
                            embed2 = discord.Embed(
                                title="", description="You were kicked from the `Official ThetaHacks Server` by %s.\nNo reason provided." % (message.author.display_name), color=0xffa600)

                            await u.send(embed=embed2)
                            await message.author.guild.kick(user=u)
                            await message.channel.send(embed=embed)

            if temp[1] == "ban":
                if len(temp) == 2:
                    await message.channel.send("Invalid arguments for command `ban`.")
                try:
                    u = message.mentions[0]
                except:
                    await message.channel.send("Invalid arguments for command `ban`.")
                else:
                    if len(temp) > 3:
                        r = " ".join(temp[3:])
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was banned by %s.\nReason: %s." % (temp[2], message.author.display_name, r), color=0xff0000)
                            embed2 = discord.Embed(
                                title="", description="You were banned from the `Official ThetaHacks Server` by %s. Reason: %s." % (message.author.display_name, r), color=0xff0000)
                            await u.send("You were banned from the `Official ThetaHacks Server`. Reason: %s." % r)
                            await message.author.guild.ban(user=u, reason=r)
                            await message.channel.send(embed=embed)
                    else:
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was banned by %s.\nNo reason provided." % (temp[2], message.author.display_name), color=0xff0000)
                            embed2 = discord.Embed(
                                title="", description="You were banned by %s.\nNo reason provided." % (message.author.display_name), color=0xff0000)
                            await u.send(embed=embed2)
                            await message.author.guild.ban(user=u)
                            await message.channel.send(embed=embed)

        else:
            await message.channel.send("{} is not in the sudoers file. This incident will be reported.".format(
                message.author.display_name))

    #VERIFY (SPECIAL)

    elif message.content == "?!v01":
        embed = discord.Embed(
            title="Verify", description="React with ✅ to get the `Attendees` role if you have already signed up for ThetaHacks at [some link].", color=0x00ff00)
        msg = await message.channel.send(embed=embed)
        client.v = str(msg.id)
        await msg.add_reaction("✅")

    elif message.content[0] == '!':
        await message.channel.send("Invalid command. `!help` for more commands.")


@client.event
async def on_reaction_add(reaction, user):

    # VERIFY WItH REACTION
    valid_emails = ["test@test.com"]

    if str(reaction.emoji).strip() == "✅" and str(reaction.message.id) == client.v:
        c = True
        while c:
            role = get(user.guild.roles, name="Attendees")
            if role not in user.roles:
                embed = discord.Embed(
                    title="Verification", description="Please type your registered email. If you have not registered yet, go to [some link].", color=0x00f7ff)
                await user.send(embed=embed)

                def check(msg):
                    return msg.channel == user.dm_channel and msg.author == user
                reply = await client.wait_for('message', check=check)

                if reply.content.lower().strip() in valid_emails:
                    await user.add_roles(role)
                    embed = discord.Embed(
                        title="Success!", description="You have been successfully verified.", color=0x00ff00)
                    await user.send(embed=embed)
                    c = False
                else:
                    embed = discord.Embed(
                        title="Error", description="Your email is not in our database. Are you sure you signed up at [some link]? If you think this is a mistake, please DM one of the admins to be manually verified. Type `retry` if you want to try again.", color=0xff0000)
                    await user.send(embed=embed)
                    reply = await client.wait_for('message', check=check)
                    if reply.content.lower().strip() == 'retry':
                        c = True
                    else:
                        c = False
            else:
                c = False


@client.event
async def on_member_join(member):

    # CUSTOM WELCOME

    for channel in member.guild.channels:
        if channel.name == 'welcome':
            embed = discord.Embed(
                title="Welcome", description="Welcome to the `Official ThetaHacks Server`, %s!" % member.mention, color=0xff00d1)
            await channel.send(embed=embed)
            embed = discord.Embed(
                title="Welcome", description="Hello %s, welcome to the `Official ThetaHacks Server!`" % member.mention, color=0xff00d1)
            await member.send(embed=embed)
            break

client.run(TOKEN)
