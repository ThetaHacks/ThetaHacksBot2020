import discord
from discord.ext import commands
from discord.utils import get
from random import randrange
import random


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        client = self.bot
        # set status (currently broken)
        await client.change_presence(activity=discord.Game(name="thetahacks.tech"))
        # print when ready
        print(f'{client.user} has connected to Discord!')


        py = get(client.guilds[0].emojis, name='python')
        clang = get(client.guilds[0].emojis, name='clang')
        cpp = get(client.guilds[0].emojis, name='cpp')
        java = get(client.guilds[0].emojis, name='java')
        html = get(client.guilds[0].emojis, name='html')
        php = get(client.guilds[0].emojis, name='php')
        js = get(client.guilds[0].emojis, name='javascript')
        csharp = get(client.guilds[0].emojis, name='csharp')
        mern = get(client.guilds[0].emojis, name='mern')
        swift = get(client.guilds[0].emojis, name='swift')
        dart = get(client.guilds[0].emojis, name='dartlang')
        other = get(client.guilds[0].emojis, name='huh')
        rust = get(client.guilds[0].emojis, name='rust')

        client.roledict[py] = "Python"
        client.roledict[clang] = "Clang"
        client.roledict[cpp] = "C++"
        client.roledict[java] = "Java"
        client.roledict[html] = "HTML/CSS"
        client.roledict[php] = "PHP"
        client.roledict[js] = "JavaScript"
        client.roledict[mern] = "MERN"
        client.roledict[csharp] = "C#"
        client.roledict[swift] = "Swift"
        client.roledict[dart] = "Dart"
        client.roledict[rust] = "Rust"
        client.roledict[other] = "Other"


    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        if not client.sent:
            client.sent = True

            text = "Available Roles:\n\n" + "\n".join(v + ": " + str(
                k) for k, v in client.roledict2.items()) + "\n\n**Unreact to remove a role.**"
            embed2 = discord.Embed(
                title="Get Topic Roles", description=text, color=0x0000ff)

            channel2 = get(message.author.guild.text_channels,
                           name="get-roles")

            msg2 = await channel2.send(embed=embed2)

            # store message in variable (check line 394)
            client.v4 = str(msg2.id)

            for key in client.roledict2.keys():
                await msg2.add_reaction(key)

            text = "Available Roles:\n\n" + "\n".join(v + ": " + str(
                k) for k, v in client.roledict.items()) + "\n\n**Unreact to remove a role.**"

            embed2 = discord.Embed(
                title="Get Language Roles", description=text, color=0x00ff00)

            channel2 = get(message.author.guild.text_channels,
                           name="get-roles")

            msg2 = await channel2.send(embed=embed2)

            # store message in variable (check line 394)
            client.v2 = str(msg2.id)

            for key in client.roledict.keys():
                await msg2.add_reaction(key)

            if message.author == client.user:
                return

        if "".join([i for i in message.content.lower() if i != " "]) in ('hi', 'hello', 'hola'):
            await message.channel.send("Hello %s!" % message.author.display_name)

        if message.content.lower().strip().split(" ")[0] == "sudo":
            # admin/mod.bot role variable
            admin = get(message.author.guild.roles, name="Admin")
            # mod = get(message.author.guild.roles, name="Senior Mods")
            bot = get(message.author.guild.roles, name="ThetaHacks Bot")

            # only admins can use this command
            if admin in message.author.roles or bot in message.author.roles:
                temp = message.content.lower().split(" ")

                # message

                if temp[1] == "message":
                    if temp[2] == "@#de43v%^":
                        tobesent = " ".join(message.content.split(" ")[3:])

                        for member in message.author.guild.members:
                            try:
                                await member.send(("Hello %s,\n\n" % member.mention) + tobesent)
                            except:
                                pass
                    else:
                        tobesent = " ".join(message.content.split(" ")[2:])

                        for member in message.author.guild.members:
                            try:
                                if admin in member.roles:
                                    await member.send(("Hello %s,\n\n" % member.mention) + tobesent)
                            except:
                                pass

                # CLEAR

                elif temp[1] == "clear":
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

                elif temp[1] == "kick":
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
                            if admin in u.roles or bot in u.roles:
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
                            if admin in u.roles or bot in u.roles:
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

                elif temp[1] == "ban":
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
                            if admin in u.roles or bot in u.roles:
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
                            if admin in u.roles or bot in u.roles:
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

                elif temp[1] == "top":
                    d = {}

                    for channel in client.guilds[0].text_channels:
                        try:
                            await message.channel.send("Parsing " + channel.name)

                            # create list of all messages in channel history
                            async for m in channel.history(limit=10000000000000000):
                                if m.author.display_name in d:
                                    d[m.author.display_name] += 1
                                else:
                                    d[m.author.display_name] = 1
                        except:
                            pass

                    d = {k: v for k, v in sorted(
                        d.items(), key=lambda item: item[1], reverse=True)}

                    with open('d.txt', 'w') as f:
                        f.write("\n".join(k+" "+str(v)
                                            for k, v in d.items()))

                    with open('d.txt', 'rb') as f:
                        await message.channel.send(file=discord.File(f, 'd.txt'))


            else:
                # if message author is not not admin/mod/bot
                await message.channel.send("{} is not in the sudoers file. This incident will be reported.".format(
                    message.author.display_name))

        #await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        print('reaction removed')
        client = self.bot
        if str(reaction.message.id) == client.v2 and reaction.emoji in client.roledict.keys():
            role = get(user.guild.roles, name=client.roledict[reaction.emoji])
            await user.remove_roles(role)

            await user.send("Your `" + client.roledict[reaction.emoji] + "` language role has been removed.")

        if str(reaction.message.id) == client.v4 and str(reaction.emoji).strip() in client.roledict2.keys():
            role = get(user.guild.roles,
                       name=client.roledict2[str(reaction.emoji).strip()])
            await user.remove_roles(role)

            await user.send("Your `" + client.roledict2[str(reaction.emoji).strip()] + "` topic role has been removed.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print("Reaction added")
        client = self.bot
        ####### VERIFY WITH REACTION #######
        #
        #
        #
        ####### VERIFY WITH REACTION #######
        
        try:
            if str(reaction.message.id) == client.v2:
                if reaction.emoji in client.roledict.keys():
                    role = get(user.guild.roles,
                               name=client.roledict[reaction.emoji])
                    await user.add_roles(role)

                    await user.send("The `" + client.roledict[reaction.emoji] + "` language role has been given to you.")
                else:
                    await reaction.remove(user)

            if str(reaction.message.id) == client.v4:
                if str(reaction.emoji).strip() in client.roledict2.keys():
                    role = get(
                        user.guild.roles, name=client.roledict2[str(reaction.emoji).strip()])
                    await user.add_roles(role)

                    await user.send("The `" + client.roledict2[str(reaction.emoji).strip()] + "` topic role has been given to you.")
                else:
                    await reaction.remove(user)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("member joined")
        client = self.bot
        ##### CUSTOM WELCOME #####
        #
        #
        #
        ##### CUSTOM WELCOME #####

        for channel in member.guild.channels:
            if channel.name == 'welcome':
                # send to welcome channel
                embed = discord.Embed(
                    title="Welcome", description="Welcome to the `Official ThetaHacks Server`, %s! The next ThetaHacks is in the works, stay tuned for more info!" % member.mention, color=0xff00d1)
                await channel.send(embed=embed)

                try:
                # send in DMs
                    embed = discord.Embed(
                        title="Welcome", description="Hello %s, welcome to the `Official ThetaHacks Server`! The next ThetaHacks is in the works, stay tuned for more info!" % member.mention, color=0xff00d1)
                    await member.send(embed=embed)
                except:
                    pass

                role = get(member.guild.roles, name="Attendees")
                while role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except:
                        pass

                try:
                    await member.send("The `Attendee` role has been given to you.")
                except:
                    pass
                break


def setup(bot):
    print("events")
    bot.add_cog(EventsCog(bot))
