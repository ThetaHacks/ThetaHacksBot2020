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
        await message.channel.send("Go to %s to sign up!" % "[some link]")

    # INFO

    elif message.content.lower() == '!info':
        await message.channel.send("ThetaHacks is a high school hackathon held in the Bay Area. More information coming soon.")

    # HELP

    elif message.content.lower() == '!help':
        await message.channel.send("Valid commands are: `!signup`, `!info`, `!help`, `!stats`.\nAdmin commands are: `sudo clear`, `sudo kick`, `sudo ban`")

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
            title="ThetaHacks Stats", description=text, color=0x0027ff)
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

                    await message.channel.send("`All` messages deleted by %s." % message.author.display_name)
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
                            await u.send("You were kicked from the `Official ThetaHacks Server`. Reason: %s." % r)
                            await message.author.guild.kick(user=u, reason=r)
                            await message.channel.send(embed=embed)
                    else:
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was kicked by %s.\nNo reason provided." % (temp[2], message.author.display_name), color=0xffa600)
                            await u.send("You were kicked from the `Official ThetaHacks Server`. No reason provided.")
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
                            await u.send("You were banned from the `Official ThetaHacks Server`. Reason: %s." % r)
                            await message.author.guild.ban(user=u, reason=r)
                            await message.channel.send(embed=embed)
                    else:
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was banned by %s.\nNo reason provided." % (temp[2], message.author.display_name), color=0xff0000)
                            await u.send("You were banned from the `Official ThetaHacks Server`. No reason provided.")
                            await message.author.guild.ban(user=u)
                            await message.channel.send(embed=embed)

        else:
            await message.channel.send("{} is not in the sudoers file. This incident will be reported.".format(
                message.author.display_name))

    #VERIFY (SPECIAL)

    elif message.content == "?!v01":
        embed = discord.Embed(
            title="Verify", description="React with ✅ to verify and gain access to the rest of the server.", color=0x00ff00)
        msg = await message.channel.send(embed=embed)
        client.v = str(msg.id)
        await msg.add_reaction("✅")

    elif message.content[0] == '!':
        await message.channel.send("Invalid command. `!help` for more commands.")


@client.event
async def on_reaction_add(reaction, user):

    # VERIFY WItH REACTION

    if str(reaction.emoji).strip() == "✅" and str(reaction.message.id) == client.v:
        role = get(user.guild.roles, name="Attendees")
        if role not in user.roles:
            await user.add_roles(role)
            await user.send("Hello {}, welcome to the `Official ThetaHacks Server`!".format(user.display_name))


@client.event
async def on_member_join(member):

    # CUSTOM WELCOME

    for channel in member.guild.channels:
        if channel.name == 'welcome':
            embed = discord.Embed(
                title="Welcome", description="Welcome to the `Official ThetaHacks Discord`, %s!\nHead over to `#verify` to gain access to the rest of the server!" % member.mention, color=0xff00d1)
            await channel.send(embed=embed)
            break

client.run(TOKEN)
