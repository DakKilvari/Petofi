from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import time
from discord.ext import commands
import cmd_rank
import cmd_guild_rank


creds = settings()
client = api_swgoh_help(creds)


class GUILDLOAD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['GuildRangKulonbseg'])
    @commands.has_any_role('Leader', 'Officer')  # User need this role to run command (can have multiple)
    async def guild_load(self, ctx):

        tic()
        await ctx.message.add_reaction("⏳")

        print("Hamarosan...")

        await ctx.send("Hamarosan...")


        toc()

    @guild_load.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


def TicTocGenerator():
    # Generator that returns time differences
    ti = 0  # initial time
    tf = time.time()  # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf - ti  # returns the time difference

TicToc = TicTocGenerator()  # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print("Elapsed time: %f seconds.\n" % tempTimeInterval)

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)

def setup(bot):
    bot.add_cog(GUILDLOAD(bot))


