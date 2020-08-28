from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import time
from discord.ext import commands
import cmd_rank
import cmd_guild_rank
import global_settings
import datetime


creds = settings()
client = api_swgoh_help(creds)


class GUILDSAVE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['GuildRangMentes'])
    @commands.has_any_role(global_settings.Role1, global_settings.Role2)  # User need this role to run command (can have multiple)
    async def guildsave(self, ctx, raw_allycode, month="m"):

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


            if temp != -1 and myresult != None and month == 'jan' or month == '1' or month == 'feb' or month == '2' or month == 'mar' or month == '3' or\
                    month == 'apr' or month == '4' or month == 'may' or month == '5' or month == 'jun' or month == '6' or month == 'jul' or month == '7' or\
                    month == 'aug' or month == '8' or month == 'sep' or month == '9' or month == 'okt' or month == '10' or month == 'nov' or month == '11' or month == 'dec' or month == '12':

                honap = switch_month_names(month)

                today = datetime.datetime.now()
                mth = switch_month_names(today.month)

                if honap == mth:
                    await ctx.message.add_reaction("✅")

                    await ctx.send(honap + "i guild rang mentés folyamatban. ⏳")
                    print(str(honap) + "i guild rang mentés folyamatban.")

                    guilddata = cmd_guild_rank.fetchGuildRoster(raw_guild)

                    player = fetchPlayerRoster(guilddata)


                    i = 0
                    n = int_(len(player))

                    while i < n:
                        n: int


                        sql = "UPDATE pilvax SET " + honap + " = %s WHERE Allycode = %s"
                        adr = (player[i]['rank'], player[i]['allycode'])
                        mycursor.execute(sql, adr)
                        mydb.commit()
                        i += 1

                    await ctx.send("Guild rang mentés kész! ✅")
                    print("Guild rang mentés kész!")

                else:
                    await ctx.message.add_reaction("❌")
                    await ctx.send("Hibás hónap! Nem " + honap + " van, nem engedélyezett a guild rang mentés.")
                    print("Hibás hónap!")


            else:
                await ctx.message.add_reaction("❌")

            mycursor.close()
            mydb.close()

            toc()

        if month == "m":
            await ctx.send("Nem adtál meg hónapot!")

        else:
            pass


    @guildsave.error
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

def switch_month_names(month):
    if month == 'jan' or month == '1' or month == 1:
        honap = 'Januar'
    if month == 'feb' or month == '2' or month == 2:
        honap = 'Februar'
    if month == 'mar' or month == '3' or month == 3:
        honap = 'Marcius'
    if month == 'apr' or month == '4' or month == 4:
        honap = 'Aprilis'
    if month == 'maj' or month == '5' or month == 5:
        honap = 'Majus'
    if month == 'jun' or month == '6' or month == 6:
        honap = 'Junius'
    if month == 'jul' or month == '7' or month == 7:
        honap = 'Julius'
    if month == 'aug' or month == '8' or month == 8:
        honap = 'Augusztus'
    if month == 'sep' or month == '9' or month == 9:
        honap = 'Szeptember'
    if month == 'okt' or month == '10' or month == 10:
        honap = 'Oktober'
    if month == 'nov' or month == '11' or month == 11:
        honap = 'November'
    if month == 'dec' or month == '12' or month == 12:
        honap = 'December'
    return honap

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