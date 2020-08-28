from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import time
from discord.ext import commands
import cmd_rank
import cmd_guild_rank


creds = settings()
client = api_swgoh_help(creds)


class GUILDSAVE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['GuildRangMentes'])
    @commands.has_any_role('Leader', 'Officer')  # User need this role to run command (can have multiple)
    async def guild_save(self, ctx, raw_allycode, month="m"):

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

        raw_guild = client.fetchGuilds(allycode)

        temp = 0

        try:
            raw_guild['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        DiscordID = m1
        AuthorID = m2

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if temp != -1 and myresult != None and month == 'January' or month == 'February' or month == 'March' or month == 'April' or month == 'May' or month == 'June' or month == 'July' or month == 'August' or month == 'September' or month == 'October' or month == 'November' or month == 'December':

                await ctx.message.add_reaction("✅")

                await ctx.send("Guild rang mentés folyamatban. ⏳")
                print("Guild rang mentés folyamatban.")

                guilddata = cmd_guild_rank.fetchGuildRoster(raw_guild)

                player = fetchPlayerRoster(guilddata)


                i = 0
                n = int_(len(player))

                while i < n:
                    n: int


                    sql = "UPDATE pilvax SET " + month + " = %s WHERE Allycode = %s"
                    adr = (player[i]['rank'], player[i]['allycode'])
                    mycursor.execute(sql, adr)
                    mydb.commit()
                    i += 1

                await ctx.send("Guild rang mentés kész! ✅")
                print("Guild rang mentés kész!")

            else:
                await ctx.message.add_reaction("❌")

            mycursor.close()
            mydb.close()

            toc()

        if month == "m":
            await ctx.send("Nem adtál meg hónapot!")

        else:
            pass


    @guild_save.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



def fetchPlayerRoster(guilddata):
    player = [{'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank': 0}]

    k = 0
    for g in guilddata:
        player[k]['jatekosnev'] = guilddata[k]['name']
        player[k]['allycode'] = guilddata[k]['allyCode']
        player[k]['rank'] = 0
        raw_player = guilddata[k]

        t = 0
        s = 0

        rankplayer = cmd_rank.fetchPlayerRoster(raw_player)
        player[k]['rank'] = rankplayer['rank']

        k += 1

    return player


def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)


def setup(bot):
    bot.add_cog(GUILDSAVE(bot))