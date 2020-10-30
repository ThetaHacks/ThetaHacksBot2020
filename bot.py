import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import random
import requests
import json

####### SETUP #######
#
#
#
#
####### SETUP #######

# get tokens as environment variables (for security)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#TYPEFORM = os.getenv('TYPEFORM_TOKEN')

# initiate client

intents = discord.Intents.all()

client = discord.Client(intents = intents)
client.v = 0
client.v2 = 0
client.v3 = 0
client.v4 = 0
client.v5 = 0
client.sent = False
client.roledict={"🐍": "Python", "💀": "Clang", "➕": "C++", "☕": "Java", "🇭": "HTML/CSS", "🇵": "PHP", "🇯": "JavaScript", "#️⃣": "C#", "❓": "Other"}
client.roledict2={"🤖": "AI/Machine Learning", "🌐": "Web Development", "🎮": "Game Design", "📈" : "Data Science", "🔎": "Algorithms"}


# headers for TypeForm API

#headers = {
#    'Authorization': 'bearer ' + TYPEFORM
#}

####### EVENTS #######
#
#
#
#
####### EVENTS #######

# when bot is first activated


@client.event
async def on_ready():
    # set status (currently broken)
    await client.change_presence(activity=discord.Game(name="thetahacks.tech"))
    # print when ready
    print(f'{client.user} has connected to Discord!')

# message monitoring


@client.event
async def on_message(message):
    
    if(not client.sent):
        client.sent = True
        embed = discord.Embed(
                    title="Verify", description="React with ✅ to get the `Attendees` role!", color=0x00ff00)
        
        channel = get(message.author.guild.text_channels, name="verify")
        
        msg = await channel.send(embed=embed)

        # store message in variable (check line 394)
        client.v = str(msg.id)

        # first reaction

        await msg.add_reaction("✅")
        
        
        
        text = "Available Roles:\n\n" + "\n\n".join(v + ": " + k for k,v in client.roledict2.items()) + "\n\n**Unreact to remove a role.**"
        embed2 = discord.Embed(
                    title="Get Topic Roles", description=text, color=0x0000ff)
        
        channel2 = get(message.author.guild.text_channels, name="get-roles")
        
        msg2 = await channel2.send(embed=embed2)

        # store message in variable (check line 394)
        client.v4 = str(msg2.id)
        
        for key in client.roledict2.keys():
            await msg2.add_reaction(key)
        
        
        
        text = "Available Roles:\n\n" + "\n\n".join(v + ": " + k for k,v in client.roledict.items()) + "\n\n**Unreact to remove a role.**"
        
    
        
        embed2 = discord.Embed(
                    title="Get Language Roles", description=text, color=0x00ff00)
        
        channel2 = get(message.author.guild.text_channels, name="get-roles")
        
        msg2 = await channel2.send(embed=embed2)

        # store message in variable (check line 394)
        client.v2 = str(msg2.id)
        
        for key in client.roledict.keys():
            await msg2.add_reaction(key)
            

        

    ####### ! COMMANDS #######
    #
    #
    #
    ####### ! COMMANDS #######

    # prevent looping    

    if message.author == client.user:
        return

    # HI

    if "".join([i for i in message.content.lower() if i != " "]) in ('hi', 'hello', 'hola'):
        await message.channel.send("Hello %s!" % message.author.display_name)

    # SIGNUP

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!signup'):
        embed = discord.Embed(
            title="Sign Up", description="Go to https://thetahacks.tech to sign up. Be sure to register by December 5th!", color=0xb134eb)
        await message.channel.send(embed=embed)

    # INFO

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!info'):
        embed = discord.Embed(
            title="Information", description="ThetaHacks is a 24-hour virtual High-School Hackathon occurring from December 19-20. What better way to start off your winter break with free merch, coding workshops, and a community of developers to talk with! We have awards from our sponsors ranging from awesome tech to free t-shirts & more! Anyone from any background of coding is welcome to join. \n More info on our website: https://thetahacks.tech/", color=0xc0e8f9)
        await message.channel.send(embed=embed)

    # PING

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!ping'):
        await message.channel.send(str(random.randint(0, 100)) + " ms")

    # DICE

    elif message.content.lower().strip().startswith('!dice'):
        # get N dice to roll
        temp = [i for i in message.content.lower().strip().split(" ")
                if i.strip() != ""]
        try:
            n = int(temp[1])
            # lower and upper bounds
            if n < 1 or n > 10:
                await message.channel.send("Invalid arguments for command `dice`.")
            else:
                # roll N dice
                await message.channel.send(" ".join(str(random.randint(1, 6)) for i in range(n)))
        except:  # error
            await message.channel.send("Invalid arguments for command `dice`.")

    # MAGIC 8 BALL

    elif message.content.lower().strip().startswith('!magic8'):
        # randomly choose from list
        bm = ("It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "Most likely.", "Outlook good.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
              "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.")
        await message.channel.send(random.choice(bm))

    # HELP

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!help'):
        embed = discord.Embed(
            title="Help", description="Valid commands:\n\n**Utility**\n`!signup` - Signup form link\n`!info` - ThetaHacks information\n`!help` - View valid commands\n`!stats` - See server statistics\n`!rules` - See server rules\n\n**Fun**\n`!kill @user`\n`!ping` - pong\n`!magic8` - Magic 8 ball\n`!dice N` - Roll N dice (1 <= N <= 10)", color=0x0027ff)
        await message.channel.send(embed=embed)

    # RULES

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!rules'):
        embed = discord.Embed(
            title="Server Rules", description="1. Do not bully or harass others. Homophobia, racism and other discrimination is not allowed. Treat others the way you wish to be treated.\n\n2. Spamming, messages that do not contribute to the general conversation and non-English messages are not allowed. With this in mind, please also send content to its relevant channels.\n\n3. Excessive or toxic swearing, as well as generally distasteful or NSFW content is not allowed.\n\n4. Do not partake in activity against any Terms of Service within our community. This includes but is not limited to, the act of purchasing and selling accounts.\n\n5. Do not promote your personal material on our server without consent of a mod or admin. If you would like to partner with us, please contact an admin.\n\n6. Discord statuses/nicknames/names should be clean, this means no slurs, nothing that breaks TOS, no promotion, etc. Failure to comply with a mod’s request to change your status in a timely manner will deem a punishment proportionate to how severe your status is.\n\n7. Logical extensions of rules may also be enforced.", color=0xaa00ff)
        await message.channel.send(embed=embed)

    # KILL

    elif message.content.lower().strip().split(" ")[0] == "!kill":
        temp = message.content.lower().split(" ")
        # no target
        if len(temp) < 2:
            await message.channel.send("Invalid arguments for command `kill`.")
        else:
            try:
                # try to get target
                u = message.mentions[0]
            except:
                # invalid target
                await message.channel.send("Invalid arguments for command `kill`.")
            else:
                # possible kill messages
                kill_messages = ["barbecued", "disintegrated", "360-no-scoped",
                                 "eaten alive", "yeeted out of existence", "squashed", "smited", "dropped in the void"]
                # choose random message
                this_msg = random.choice(kill_messages)

                embed = discord.Embed(
                    title="K-O!", description="%s was %s by %s" % (u.display_name, this_msg, message.author.display_name), color=0xff00d1)
                await message.channel.send(embed=embed)

    # STATS

    elif "".join([i for i in message.content.lower() if i != " "]).startswith('!stats'):
        # dictionary
        a = {}
        # prevent errors when no members have role "testing", check line 158
        '''a["testing"] = 0
        # loop through server members
        for member in message.author.guild.members:
            # count roles
            for role in member.roles:
                if str(role.name) not in a.keys():
                    a[str(role.name)] = 1
                else:
                    a[str(role.name)] += 1

        # subtract testing and bot from attendees
        a["Attendees"] -= a["testing"] + a["ThetaHacks Bot"]

        # on each new line, lists a role and how many people have that role (excluded are "testing", "ThetaHacks Bot")
        text = "\n".join("`%i` %s" % (v, k) for k, v in a.items()
                         if k not in ("testing", "ThetaHacks Bot"))'''
                         
        good_roles = ("@everyone", "Attendees", "Leadership", "Staff")
                         
        for member in message.author.guild.members:
            # count roles
            for role in member.roles:
                if(str(role.name) in good_roles):
                    if str(role.name) not in a.keys():
                        a[str(role.name)] = 1
                    else:
                        a[str(role.name)] += 1    
                    
        a["All Members"] = a["@everyone"]
        del a["@everyone"]
                    
        text = "\n".join("`%i` %s" % (v, k) for k, v in a.items())   
        
        embed = discord.Embed(
            title="ThetaHacks Stats", description=text, color=0x00ff9d)
        await message.channel.send(embed=embed)

    ##### SUDO COMMANDS #####
    #
    #
    #
    #
    ##### SUDO COMMANDS #####

    elif message.content.lower().strip().split(" ")[0] == "sudo":
        # admin/mod.bot role variable
        admin = get(message.author.guild.roles, name="Leadership")
        # mod = get(message.author.guild.roles, name="Senior Mods")
        bot = get(message.author.guild.roles, name="ThetaHacks Bot")

        # only admins can use this command
        if admin in message.author.roles or bot in message.author.roles or mod in message.author.roles:
            temp = message.content.lower().split(" ")

            # CLEAR

            if temp[1] == "clear":
                # if no arguments
                if len(temp) == 2:
                    await message.channel.send("Invalid arguments for command `clear`.")
                elif temp[2] == "all":
                    # clear all
                    msg = []
                    # create list of all messages in channel history
                    async for x in message.channel.history():
                        msg.append(x)
                    # delete messages
                    await message.channel.delete_messages(msg)
                    await message.channel.send("All messages deleted by %s." % message.author.display_name)
                else:
                    try:
                        # try to parse argument for integer
                        n = int(temp[2])

                        # if invalid argument
                        if n <= 0 or not n:
                            await message.channel.send("Invalid arguments for command `clear`.")
                        else:
                            # delete last n messages (plus the clear command)
                            msg = []
                            async for x in message.channel.history(limit=n+1):
                                msg.append(x)
                            await message.channel.delete_messages(msg)

                            await message.channel.send("`%i` messages deleted by %s" % (n, message.author.display_name))
                    except:
                        # error while parsing
                        await message.channel.send("Invalid arguments for command `clear`.")

            # KICK

            if temp[1] == "kick":
                # if no user provided
                if len(temp) == 2:
                    await message.channel.send("Invalid arguments for command `kick`.")
                try:
                    # attempt to parse for user
                    u = message.mentions[0]
                except:
                    # no mentions found
                    await message.channel.send("Invalid arguments for command `kick`.")
                else:
                    # possible kick messages
                    kick_messages = ["kicked in the heinie",
                                     "yeeted out of existence", "turned into dust", "barbecued"]

                    this_msg = random.choice(kick_messages)

                    if len(temp) > 3:
                        # if reason is given

                        # get reason
                        r = " ".join(temp[3:])

                        # cannot kick admin, bot, or mod
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            # send message in channel
                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nReason: %s." % (temp[2], this_msg, message.author.display_name, r), color=0xffa600)
                            # send DM to kicked user
                            embed2 = discord.Embed(
                                title="", description="You were kicked from the `Official ThetaHacks Server` by %s.\nReason: %s." % (message.author.display_name, r), color=0xffa600)

                            await u.send(embed=embed2)

                            # kick user

                            await message.author.guild.kick(user=u, reason=r)
                            await message.channel.send(embed=embed)
                    else:
                        # if no reason provided

                        # cannot kick admin, bot, or mod
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:
                            # send message in channel
                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nNo reason provided." % (temp[2], this_msg, message.author.display_name), color=0xffa600)
                            # send DM to kicked user
                            embed2 = discord.Embed(
                                title="", description="You were kicked from the `Official ThetaHacks Server` by %s.\nNo reason provided." % (message.author.display_name), color=0xffa600)

                            # kick user

                            await u.send(embed=embed2)
                            await message.author.guild.kick(user=u)
                            await message.channel.send(embed=embed)

            # BAN

            if temp[1] == "ban":
                # no user provided
                if len(temp) == 2:
                    await message.channel.send("Invalid arguments for command `ban`.")
                try:
                    # parse for user
                    u = message.mentions[0]
                except:
                    # no mentions
                    await message.channel.send("Invalid arguments for command `ban`.")
                else:
                    # possible messages
                    ban_messages = ["struck by the banhammer",
                                    "banned out of existence"]

                    this_msg = random.choice(ban_messages)

                    # with reason
                    if len(temp) > 3:

                        # get reason
                        r = " ".join(temp[3:])

                        # cannot kick admin, bot, or mod
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:

                            # send message and ban

                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nReason: %s." % (temp[2], this_msg, message.author.display_name, r), color=0xff0000)
                            embed2 = discord.Embed(
                                title="", description="You were banned from the `Official ThetaHacks Server` by %s. Reason: %s." % (message.author.display_name, r), color=0xff0000)
                            await u.send(embed=embed2)
                            await message.author.guild.ban(user=u, reason=r)
                            await message.channel.send(embed=embed)
                    else:
                        # cannot kick admin, bot, or mod
                        if admin in u.roles or bot in u.roles or mod in u.roles:
                            await message.channel.send("Insufficient permissions.")
                        else:

                            # send message and ban

                            embed = discord.Embed(
                                title="", description="%s was %s by %s.\nNo reason provided." % (temp[2], this_msg, message.author.display_name), color=0xff0000)
                            embed2 = discord.Embed(
                                title="", description="You were banned by %s.\nNo reason provided." % (message.author.display_name), color=0xff0000)
                            await u.send(embed=embed2)
                            await message.author.guild.ban(user=u)
                            await message.channel.send(embed=embed)

        else:
            # if message author is not not admin/mod/bot
            await message.channel.send("{} is not in the sudoers file. This incident will be reported.".format(
                message.author.display_name))

    # GENERATE REACION TO VERIFY (SPECIAL) #
    #
    #
    # GENERATE REACION TO VERIFY (SPECIAL) #


    # INVALID ATTEMPTED COMMAND #
    #
    #
    # INVALID ATTEMPTED COMMAND #

    elif message.content.strip()[0] == '!':
        await message.channel.send("Invalid command. `!help` for more commands.")

@client.event
async def on_reaction_remove(reaction, user):
        
    if str(reaction.message.id) == client.v2 and str(reaction.emoji).strip() in client.roledict.keys():
        role = get(user.guild.roles, name=client.roledict[str(reaction.emoji).strip()])
        await user.remove_roles(role)
        
        await user.send("Your `" + client.roledict[str(reaction.emoji).strip()] + "` language role has been removed.")
        
    if str(reaction.message.id) == client.v4 and str(reaction.emoji).strip() in client.roledict2.keys():
        role = get(user.guild.roles, name=client.roledict2[str(reaction.emoji).strip()])
        await user.remove_roles(role)
        
        await user.send("Your `" + client.roledict2[str(reaction.emoji).strip()] + "` topic role has been removed.")

@client.event
async def on_reaction_add(reaction, user):

    ####### VERIFY WITH REACTION #######
    #
    #
    #
    ####### VERIFY WITH REACTION #######
    
    if str(reaction.message.id) == client.v2 and str(reaction.emoji).strip() in client.roledict.keys():
        role = get(user.guild.roles, name=client.roledict[str(reaction.emoji).strip()])
        await user.add_roles(role)
        
        await user.send("The `" + client.roledict[str(reaction.emoji).strip()] + "` language role has been given to you.")

        
    if str(reaction.message.id) == client.v4 and str(reaction.emoji).strip() in client.roledict2.keys():
        role = get(user.guild.roles, name=client.roledict2[str(reaction.emoji).strip()])
        await user.add_roles(role)
        
        await user.send("The `" + client.roledict2[str(reaction.emoji).strip()] + "` topic role has been given to you.")


    # check for correct reaction and correct message
    if str(reaction.emoji).strip() == "✅" and str(reaction.message.id) == client.v:
        # loop attemps
        #c = True
        #while c:
            # get role

        role = get(user.guild.roles, name="Attendees")
        await user.add_roles(role)
        
        await user.send("The `Attendee` role has been given to you.")



@client.event
async def on_member_join(member):

    ##### CUSTOM WELCOME #####
    #
    #
    #
    ##### CUSTOM WELCOME #####

    for channel in member.guild.channels:
        if channel.name == 'welcome':
            # send to welcome channel
            embed = discord.Embed(
                title="Welcome", description="Welcome to the `Official ThetaHacks Server`, %s!" % member.mention, color=0xff00d1)
            await channel.send(embed=embed)

            # send in DMs
            embed = discord.Embed(
                title="Welcome", description="Hello %s, welcome to the `Official ThetaHacks Server`!" % member.mention, color=0xff00d1)
            await member.send(embed=embed)
            break


@client.event
async def on_member_remove(member):

    ##### UPDATE VERIFIED EMAILS #####
    #
    #
    #
    ##### UPDATE VERIFIED EMAILS #####

    with open('already_verified.txt', 'r') as fin:
        temp = fin.read().split("\n")
        for i in temp:
            if str(member.id) == i.split(" ")[0]:
                # remove email if registered with the leaving user
                temp.remove(i)
        with open('already_verified.txt', 'w') as fout:
            fout.write("\n".join(temp))


# run client
client.run(TOKEN)
