from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import discord
import time
from discord.ext import commands
import cmd_rank

creds = settings()
client = api_swgoh_help(creds)


class GUILDRANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['GuildRang'])
    @commands.has_any_role('Leader', 'Officer', 'Commander')  # User need this role to run command (can have multiple)
    async def guild_rang(self, ctx, raw_allycode):
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

        if temp != -1:

            await ctx.message.add_reaction("✅")

            print("\n" + "Guild rang lekérés folyamatban.")

            guilddata = fetchGuildRoster(raw_guild)

            player = fetchPlayerRoster(guilddata)

            player.sort(reverse=True, key=Sort)

            player = fetchPlayerRanknev(player)

            i = 0
            n = int_(len(player))
            lth = 0
            while i < n:
                lth2 = int_(len(player[i]['jatekosnev']))
                if lth2 > lth:
                    lth = lth2
                i += 1

            embed = discord.Embed(title='Pilvax Hungary guild rang táblázata',
                                  url="https://swgoh.gg/g/1294/pilvax-hungary/",
                                  color=0x7289da)

            i = 0
            embed.add_field(name='=============== Top 10 Rangú játékos ===============', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 10
            embed.add_field(name='=================== Top 11 - 20 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 20
            embed.add_field(name='=================== Top 21 - 30 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 30
            embed.add_field(name='=================== Top 31 - 40 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')

            i = 40
            embed.add_field(name='=================== Top 41 - 50 ===================', value=
            '```' + str(player[i]['jatekosnev']) + ' ' * (lth-len(str(player[i]['jatekosnev']))) + ' ' * round(1 / len(str(player[i]['rank']))) + str(player[i]['rank']) + ' pont' + '  ' + str(player[i]['ranknev']) + '\n' +
            str(player[i+1]['jatekosnev']) + ' ' * (lth-len(str(player[i+1]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+1]['rank']))) + str(player[i+1]['rank']) + ' pont' + '  ' + str(player[i+1]['ranknev']) + '\n' +
            str(player[i+2]['jatekosnev']) + ' ' * (lth-len(str(player[i+2]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+2]['rank']))) + str(player[i+2]['rank']) + ' pont' + '  ' + str(player[i+2]['ranknev']) + '\n' +
            str(player[i+3]['jatekosnev']) + ' ' * (lth-len(str(player[i+3]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+3]['rank']))) + str(player[i+3]['rank']) + ' pont' + '  ' + str(player[i+3]['ranknev']) + '\n' +
            str(player[i+4]['jatekosnev']) + ' ' * (lth-len(str(player[i+4]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+4]['rank']))) + str(player[i+4]['rank']) + ' pont' + '  ' + str(player[i+4]['ranknev']) + '\n' +
            str(player[i+5]['jatekosnev']) + ' ' * (lth-len(str(player[i+5]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+5]['rank']))) + str(player[i+5]['rank']) + ' pont' + '  ' + str(player[i+5]['ranknev']) + '\n' +
            str(player[i+6]['jatekosnev']) + ' ' * (lth-len(str(player[i+6]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+6]['rank']))) + str(player[i+6]['rank']) + ' pont' + '  ' + str(player[i+6]['ranknev']) + '\n' +
            str(player[i+7]['jatekosnev']) + ' ' * (lth-len(str(player[i+7]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+7]['rank']))) + str(player[i+7]['rank']) + ' pont' + '  ' + str(player[i+7]['ranknev']) + '\n' +
            str(player[i+8]['jatekosnev']) + ' ' * (lth-len(str(player[i+8]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+8]['rank']))) + str(player[i+8]['rank']) + ' pont' + '  ' + str(player[i+8]['ranknev']) + '\n' +
            str(player[i+9]['jatekosnev']) + ' ' * (lth-len(str(player[i+9]['jatekosnev']))) + ' ' * round(1 / len(str(player[i+9]['rank']))) + str(player[i+9]['rank']) + ' pont' + '  ' + str(player[i+9]['ranknev']) + '\n' + '```')



            await ctx.send(embed=embed)

            toc()

        else:
            pass

    @guild_rang.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def Sort(a):
    return a['rank']

def fetchPlayerRanknev(player):
    i = 0
    n = int_(len(player))
    while i < n:
        cmd_rank.fetchPlayerRanknev(player[i])
        i += 1

    return player

def fetchGuildRoster(raw_guild):
    guilddata = []
    chardata_ally = []
    chardata_ally2 = []
    i: int = 0
    lth = int_(len(raw_guild[0]['roster']))
    lthp2 = int_(round(lth/2, 0))
    while i < lthp2:
        chardata_ally.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata = client.fetchPlayers(chardata_ally)

    while i < lth:
        chardata_ally2.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata += client.fetchPlayers(chardata_ally2)

    return guilddata


def fetchPlayerRoster(guilddata):
    player = [{'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0},
              {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}, {'jatekosnev': ' ', 'rank': 0}]

    k = 0
    for g in guilddata:
        player[k]['jatekosnev'] = guilddata[k]['name']
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
    bot.add_cog(GUILDRANK(bot))