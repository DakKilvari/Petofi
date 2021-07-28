from api_swgoh_help import api_swgoh_help, settings
from discord.ext import commands

import global_settings

creds = settings()
client = api_swgoh_help(creds)

class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['LS geo tb-hez combat A visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def A(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @A.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat B visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def B(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @B.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat C visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def C(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @C.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat D visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def D(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @D.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat E visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def E(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @E.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat F visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def F(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @F.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat G visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def G(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @G.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


    @commands.command(aliases=['LS geo tb-hez combat H visszajelzés'])
    @commands.has_any_role(global_settings.Role2)  # User need this role to run command (can have multiple)
    async def H(self, ctx):

        await ctx.message.add_reaction("0️⃣")
        await ctx.message.add_reaction("1️⃣")
        await ctx.message.add_reaction("2️⃣")
        await ctx.message.add_reaction("3️⃣")
        await ctx.message.add_reaction("4️⃣")

    @H.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


def setup(bot):
    bot.add_cog(Feedback(bot))