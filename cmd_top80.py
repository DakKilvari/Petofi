import time
from numpy import *
from discord.ext import commands
from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
import global_settings


class GAC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Top 80 karakter gp'])
    @commands.has_any_role(global_settings.Role3)  # User need this role to run command (can have multiple)
    async def top80(self, ctx, raw_allycode):
        """Top 80 karakter gp
        Aktuális roster top80 karakterének összGP értéke
        raw_allycode: me / taggelés / allykód"""

        tic()
        await ctx.message.add_reaction("⏳")

        m1 = str(ctx.author.id)
        try:
            m2 = str(ctx.message.mentions[0].id)
        except:
            m2 = "000000000"

        database = db_handler(m1, m2)
        mydb = database.myDb()
        mycursor = mydb.cursor()
        allycode = database.fetchMe(raw_allycode, mycursor)

        mycursor.close()
        mydb.close()

        creds = settings()
        client = api_swgoh_help(creds)
        raw_player = client.fetchPlayers(allycode)

        temp = 0

        try:
            raw_player['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        if temp != -1:

            print("\n" + raw_player[0]['name'] + "-tól top80 lekérés.")

            await ctx.message.add_reaction("✅")

            player = fetchPlayerRoster(raw_player)

            await ctx.send(ctx.message.author.mention + "  " + player['jatekosnev'] + " top 80 karakter GP-je: " + str('{:,}'.format(player['top80'])))

            toc()

        else:
            pass


    @top80.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def fetchPlayerRoster(raw_player):
    player = {
        "jatekosnev": " ",
        "top80": 0
    }

    temp = []
    player['jatekosnev'] = raw_player[0]['name']
    i = 0
    for a in raw_player[0]['roster']:
        relikGP:int = 0
        if raw_player[0]['roster'][i]['combatType'] == "CHARACTER":
            if raw_player[0]['roster'][i]['gear'] == 13:
                relikGP = fetchRelik(raw_player[0]['roster'][i])
            fullGP = raw_player[0]['roster'][i]['gp'] + relikGP
            temp.insert(i, fullGP)
        i += 1
    temp.sort(reverse=True)

    i = 0
    while i < 80:
        player['top80'] += temp[i]
        i += 1

    return player

def fetchRelik(player):

    relikGP:int = 0
    if player['relic']['currentTier'] == 2:
        relikGP = 0
    if player['relic']['currentTier'] == 3:
        relikGP = 759
    if player['relic']['currentTier'] == 4:
        relikGP = 1594
    if player['relic']['currentTier'] == 5:
        relikGP = 2505
    if player['relic']['currentTier'] == 6:
        relikGP = 3492
    if player['relic']['currentTier'] == 7:
        relikGP = 4554
    if player['relic']['currentTier'] == 8:
        relikGP = 6072
    if player['relic']['currentTier'] == 9:
        relikGP = 7969

    return relikGP

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
    bot.add_cog(GAC(bot))