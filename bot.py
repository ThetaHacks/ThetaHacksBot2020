import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import random
import requests
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TYPEFORM = os.getenv('TYPEFORM_TOKEN')

client = discord.Client()
client.v = 0


headers = {
    'Authorization': 'bearer ' + TYPEFORM
}


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="being made by Andy Li"))
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    # ! COMMANDS

    if message.author == client.user:
        return

    # HI

    if "".join([i for i in message.content.lower() if i != " "]) in ('hi', 'hello', 'hola'):
        await message.channel.send("Hello %s!" % message.author.display_name)

    # SIGNUP

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!signup'):
        embed = discord.Embed(
            title="Sign Up", description="Go to https://thetahacks.github.io/ThetaHacksSite/ to sign up!", color=0xb134eb)
        await message.channel.send(embed=embed)

    # INFO

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!info'):
        embed = discord.Embed(
            title="Information", description="ThetaHacks is a high school hackathon held in the Bay Area. More information coming soon.", color=0xc0e8f9)
        await message.channel.send(embed=embed)

    # HELP

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!help'):
        embed = discord.Embed(
            title="Help", description="Valid commands:\n`!signup` - Signup form link\n`!info` - ThetaHacks information\n`!help` - View valid commands\n`!stats` - See server statistics\n`!rules` - See server rules\n`!kill [@user]`", color=0x0027ff)
        await message.channel.send(embed=embed)

    # RULES

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!rules'):
        embed = discord.Embed(
            title="Server Rules", description="1. Do not bully or harass others. Homophobia, racism and other discrimination is not allowed. Treat others the way you wish to be treated.\n\n2. Spamming, messages that do not contribute to the general conversation and non-English messages are not allowed. With this in mind, please also send content to its relevant channels.\n\n3. Excessive or toxic swearing, as well as generally distasteful or NSFW content is not allowed.\n\n4. Do not partake in activity against any Terms of Service within our community. This includes but is not limited to, the act of purchasing and selling accounts.\n\n5. Discord statuses should be clean, this means no slurs, nothing that breaks TOS, no promotion, etc. Failure to comply with a mod’s request to change your status in a timely manner will deem a punishment proportionate to how severe your status is.", color=0xaa00ff)
        await message.channel.send(embed=embed)

    # KILL

    elif message.content.lower().strip().split(" ")[0] == "!kill":
        temp = message.content.lower().split(" ")
        if len(temp) < 2:
            await message.channel.send("Invalid arguments for command `kill`.")
        else:
            try:
                u = message.mentions[0]
            except:
                await message.channel.send("Invalid arguments for command `kill`.")
            else:
                kill_messages = ["barbecued", "disintegrated", "360-no-scoped",
                                 "eaten alive", "yeeted out of existence", "squashed", "smited"]
                this_msg = random.choice(kill_messages)

                embed = discord.Embed(
                    title="K-O!", description="%s was %s by %s" % (u.display_name, this_msg, message.author.display_name), color=0xff00d1)
                await message.channel.send(embed=embed)

    # STATS

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!stats'):
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

    elif message.content.lower().strip().split(" ")[0] == "sudo":
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
                    kick_messages = ["kicked in the heinie",
                                     "yeeted out of existence", "turned into dust", "barbecued"]

                    this_msg = random.choice(kick_messages)
                    if len(temp) > 3:
                        r = " ".join(temp[3:])
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nReason: %s." % (temp[2], this_msg, message.author.display_name, r), color=0xffa600)
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
                                title="", description="%s was %s by %s.\nNo reason provided." % (temp[2], this_msg, message.author.display_name), color=0xffa600)
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
                    ban_messages = ["struck by the banhammer",
                                    "banned out of existence"]

                    this_msg = random.choice(ban_messages)

                    if len(temp) > 3:
                        r = " ".join(temp[3:])
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nReason: %s." % (temp[2], this_msg, message.author.display_name, r), color=0xff0000)
                            embed2 = discord.Embed(
                                title="", description="You were banned from the `Official ThetaHacks Server` by %s. Reason: %s." % (message.author.display_name, r), color=0xff0000)
                            await u.send(embed=embed2)
                            await message.author.guild.ban(user=u, reason=r)
                            await message.channel.send(embed=embed)
                    else:
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nNo reason provided." % (temp[2], this_msg, message.author.display_name), color=0xff0000)
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
            title="Verify", description="React with ✅ to get the `Attendees` role if you have already signed up for ThetaHacks at https://thetahacks.github.io/ThetaHacksSite/.", color=0x00ff00)
        msg = await message.channel.send(embed=embed)
        client.v = str(msg.id)
        await msg.add_reaction("✅")

    elif message.content[0] == '!':
        await message.channel.send("Invalid command. `!help` for more commands.")


@client.event
async def on_reaction_add(reaction, user):

    # VERIFY WItH REACTION

    if str(reaction.emoji).strip() == "✅" and str(reaction.message.id) == client.v:
        c = True
        while c:
            role = get(user.guild.roles, name="Attendees")
            if role not in user.roles:
                embed = discord.Embed(
                    title="Verification", description="Please type your registered email. If you have not registered yet, go to https://thetahacks.github.io/ThetaHacksSite/.", color=0x00f7ff)
                await user.send(embed=embed)

                def check(msg):
                    return msg.channel == user.dm_channel and msg.author == user
                reply = await client.wait_for('message', check=check)

                r = requests.get(
                    "https://api.typeform.com/forms/iPkfUe/responses", headers=headers)

                print(r.text)

                jsn = json.loads(r.text)

                valid_emails = [i["answers"][2]['email'].strip()
                                for i in jsn["items"]]

                with open('already_verified.txt', 'r') as fin:
                    already_verified = [
                        i.strip().split(" ")[1] for i in fin.read().split("\n") if i.strip() != ""]
                    if reply.content.lower().strip() in already_verified:
                        a_v_b = True
                    else:
                        a_v_b = False

                if reply.content.lower().strip() in valid_emails and not a_v_b:
                    await user.add_roles(role)
                    embed = discord.Embed(
                        title="Success!", description="You have been successfully verified.", color=0x00ff00)
                    await user.send(embed=embed)
                    with open('already_verified.txt', 'r') as fin:
                        prev = fin.read()
                    with open('already_verified.txt', 'w') as fout:
                        fout.write(prev + "\n" + str(reply.author.id) +
                                   " " + reply.content.lower().strip())
                    c = False
                else:
                    if a_v_b:
                        embed = discord.Embed(
                            title="Error", description="Your email has already been used by another user to verify. If you think this is a mistake, please DM one of the admins to be manually verified. Type `retry` if you want to try again.", color=0xff0000)
                        await user.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error", description="Your email is not in our database. Are you sure you signed up at https://thetahacks.github.io/ThetaHacksSite/? If you think this is a mistake, please DM one of the admins to be manually verified. Type `retry` if you want to try again.", color=0xff0000)
                        await user.send(embed=embed)
                    reply = await client.wait_for('message', check=check)
                    if reply.content.lower().strip() == 'retry':
                        c = True
                    else:
                        c = False
                        embed = discord.Embed(title="Verification Process Abandoned",
                                              description="If you still want to verify, unreact and react again with the checkmark in `#verify` again.", color=0xff0000)
                        await user.send(embed=embed)
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
                title="Welcome", description="Hello %s, welcome to the `Official ThetaHacks Server`!" % member.mention, color=0xff00d1)
            await member.send(embed=embed)
            break


@client.event
async def on_member_remove(member):
    with open('already_verified.txt', 'r') as fin:
        temp = fin.read().split("\n")
        for i in temp:
            if str(member.id) == i.split(" ")[0]:
                temp.remove(i)
        with open('already_verified.txt', 'w') as fout:
            fout.write("\n".join(temp))

client.run(TOKEN)
