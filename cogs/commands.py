from discord.ext import commands
import discord
import random
import time


class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        
    @commands.command(name="events")
    async def events(self, ctx):
        embed = discord.Embed(
            title="Events", description="", color=0x00ff9d)
        await ctx.send(embed=embed)

    @commands.command(name="signup")
    async def signup(self, ctx):
        embed = discord.Embed(
            title="Sign Up", description="Go to https://thetahacks.tech/signup to sign up. Be sure to register by January 15, 2021! \
                Also don't forget to sign up on Devpost at https://thetahacks.devpost.com and for events at https://thetahacks.tech/events.", color=0xb134eb)
        await ctx.send(embed=embed)

    @commands.command(name="info")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Information", description="ThetaHacks is a 24-hour virtual High-School Hackathon occurring from January 15-18, 2021. \
                What better way to start off your winter break with free merch, coding workshops, and a community of developers to talk with! \
                    We have awards from our sponsors ranging from awesome tech to free t-shirts & more! Anyone from any background of coding is \
                        welcome to join. \n\nLinks:\nMore info and signups on our website: https://thetahacks.tech \n Devpost: https://thetahacks.devpost.com", color=0xc0e8f9)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content='Pong! {:.2f}ms'.format(duration))

    @commands.command(name="dice")
    async def dice(self, ctx, n=1):
        try:
            if n < 1 or n > 20:
                await ctx.send("Invalid arguments for command `dice`.")
            else:
                # roll N dice
                await ctx.send(" ".join(str(random.randint(1, 6)) for i in range(n)))
        except:  # error
            await ctx.send("Invalid arguments for command `dice`.")

    @commands.command(name="magic8")
    async def magic8(self, ctx):
        bm = ("It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "Most likely.", "Outlook good.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
              "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.")
        await ctx.send(random.choice(bm))

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help", description="Valid commands:\n\n**Utility**\n`!events` - List event times and Zoom link\n`!signup` - Signup form link\n`!info` - ThetaHacks information\n`!help` - \
                View valid commands\n`!stats` - See server statistics\n`!rules` - See server rules\n\n**Fun**\n`!kill @user`\n`!ping` - pong\n`!magic8` - \
                    Magic 8 ball\n`!dice N` - Roll N dice (1 <= N <= 10)", color=0x0027ff)
        await ctx.send(embed=embed)

    @commands.command(name="rules")
    async def rules(self, ctx):
        embed = discord.Embed(
            title="Server Rules", description="1. Do not bully or harass others. Homophobia, racism and other discrimination is not allowed. \
                Treat others the way you wish to be treated.\n\n2. Spamming, messages that do not contribute to the general conversation and \
                    non-English messages are not allowed. With this in mind, please also send content to its relevant channels.\n\n3. \
                        Excessive or toxic swearing, as well as generally distasteful or NSFW content is not allowed.\n\n4. Do not partake in \
                            activity against any Terms of Service within our community. This includes but is not limited to, the act of purchasing \
                                and selling accounts.\n\n5. Do not promote your personal material on our server without consent of a mod or admin. \
                                    If you would like to partner with us, please contact an admin.\n\n6. Discord statuses/nicknames/names should be clean, \
                                        this means no slurs, nothing that breaks TOS, no promotion, etc. Failure to comply with a mod’s request to change your \
                                            status in a timely manner will deem a punishment proportionate to how severe your status is.\n\n7. Logical extensions of \
                                                rules may also be enforced.", color=0xaa00ff)
        await ctx.send(embed=embed)

    @commands.command(name="kill")
    async def kill(self, ctx, member: discord.Member):
        if not member:
            return await ctx.send("Invalid arguments for command `kill`")
        kill_messages = ["barbecued", "disintegrated", "360-no-scoped",
                         "eaten alive", "yeeted out of existence", "squashed", "smited", "dropped in the void"]
        # choose random message
        this_msg = random.choice(kill_messages)

        embed = discord.Embed(
            title="K-O!", description="%s was %s by %s" % (member.name, this_msg, ctx.author.name), color=0xff00d1)
        await ctx.send(embed=embed)

    @commands.command(name="stats")
    async def stats(self, ctx):
        print("hi")
        everyone = ctx.guild.get_role(717170061382516736)
        attendees = ctx.guild.get_role(721874238801313884)
        partners = ctx.guild.get_role(741822062221459568)
        bots = ctx.guild.get_role(721827685990531113)
        mentors = ctx.guild.get_role(722143200910901250)
        staff = ctx.guild.get_role(730445847938203718)
        coordinators = ctx.guild.get_role(717171411692683275)

        text = f"`{len(coordinators.members)}` Coordinators\n`{len(staff.members)}` Staff\n`{len(mentors.members)}` Mentors\n`{len(partners.members)}\
            ` Partners\n`{len(bots.members)}` Bots\n`{len(attendees.members)}` Attendees\n`{len(everyone.members)}` All Members"
        embed = discord.Embed(
            title="ThetaHacks Stats", description=text, color=0x00ff9d)
        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(CommandsCog(bot))
