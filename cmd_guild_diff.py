from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import time
from discord.ext import commands
import discord
import cmd_guild_save
import global_settings

creds = settings()
client = api_swgoh_help(creds)


class Guildload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Guild rang betöltés és különbség számítás'])
    @commands.has_any_role(global_settings.Role1, global_settings.Role2)  # User need this role to run command (can have multiple)
    async def load(self, ctx, raw_allycode, month1="mth1", month2="mth2"):
        """Guild rang betöltés és különbség számítás
        Havi mentések visszanézésére és fejlődés számítására
        raw_allycode: me / taggelés / allykód
        month1: 1,2,3,.. / jan, feb, mar,...
        month2: 1,2,3,.. / jan, feb, mar,... Ez legyen a későbbi időpont."""

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

            if temp != -1 and myresult != None and (
                    month1 == 'jan' or month1 == '1' or month1 == 'feb' or month1 == '2' or month1 == 'mar' or month1 == '3' or \
                    month1 == 'apr' or month1 == '4' or month1 == 'may' or month1 == '5' or month1 == 'jun' or month1 == '6' or month1 == 'jul' or month1 == '7' or \
                    month1 == 'aug' or month1 == '8' or month1 == 'sep' or month1 == '9' or month1 == 'okt' or month1 == '10' or month1 == 'nov' or month1 == '11' or month1 == 'dec' or month1 == '12') and \
                    (month2 == 'jan' or month2 == '1' or month2 == 'feb' or month2 == '2' or month2 == 'mar' or month2 == '3' or \
                    month2 == 'apr' or month2 == '4' or month2 == 'may' or month2 == '5' or month2 == 'jun' or month2 == '6' or month2 == 'jul' or month2 == '7' or \
                    month2 == 'aug' or month2 == '8' or month2 == 'sep' or month2 == '9' or month2 == 'okt' or month2 == '10' or month2 == 'nov' or month2 == '11' or month2 == 'dec' or month2 == '12'):

                honap1 = cmd_guild_save.switch_month_names(month1)
                honap2 = cmd_guild_save.switch_month_names(month2)

                h1 = check_month(honap1)
                h2 = check_month(honap2)

                if h2 > h1:

                    await ctx.message.add_reaction("✅")

                    await ctx.send("Guild rang betöltés folyamatban. ⏳")
                    print("Guild rang betöltés folyamatban.")

                    player = fetchPlayerRoster(raw_guild)

                    i = 0
                    k = 0
                    y: int = 0
                    n = int_(len(player))

                    while k < n:
                        sql = "SELECT " + honap1 + ", " + honap2 + " FROM pilvax WHERE Allycode = %s"
                        adr = (player[k]['allycode'],)
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            player[k]['rank1'] = x[0]
                            player[k]['rank2'] = x[1]
                        player[k]['diff'] = player[k]['rank2'] - player[k]['rank1']
                        if player[k]['diff'] > 30:
                            player[k]['diff'] = -1
                        k += 1

                    player.sort(reverse=True, key=Sorta)

                    i = 0
                    lth = 0
                    while i < n:
                        lth2 = int_(len(player[i]['jatekosnev']))
                        if lth2 > lth:
                            lth = lth2
                        i += 1

                    embed = discord.Embed(title='Pilvax Hungary ' + honap2 + 'i fejlődése',
                                          url="https://swgoh.gg/g/1294/pilvax-hungary/",
                                          color=0x7289da)

                    i = 0
                    embed.add_field(name='======== Top 10 Rangú játékos ========', value=
                    '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['diff']) + ' pont' + '\n' +
                    str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['diff']) + ' pont' + '\n' +
                    str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['diff']) + ' pont' + '\n' +
                    str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['diff']) + ' pont' + '\n' +
                    str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['diff']) + ' pont' + '\n' +
                    str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['diff']) + ' pont' + '\n' +
                    str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['diff']) + ' pont' + '\n' +
                    str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['diff']) + ' pont' + '\n' +
                    str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['diff']) + ' pont' + '\n' +
                    str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['diff']) + ' pont' + '\n' + '```', inline='false')

                    i = 10
                    embed.add_field(name='============ Top 11 - 20 ============', value=
                    '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['diff']) + ' pont' + '\n' +
                    str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['diff']) + ' pont' + '\n' +
                    str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['diff']) + ' pont' + '\n' +
                    str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['diff']) + ' pont' + '\n' +
                    str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['diff']) + ' pont' + '\n' +
                    str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['diff']) + ' pont' + '\n' +
                    str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['diff']) + ' pont' + '\n' +
                    str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['diff']) + ' pont' + '\n' +
                    str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['diff']) + ' pont' + '\n' +
                    str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['diff']) + ' pont' + '\n' + '```', inline='false')

                    i = 20
                    embed.add_field(name='============ Top 21 - 30 ============', value=
                    '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['diff']) + ' pont' + '\n' +
                    str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['diff']) + ' pont' + '\n' +
                    str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['diff']) + ' pont' + '\n' +
                    str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['diff']) + ' pont' + '\n' +
                    str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['diff']) + ' pont' + '\n' +
                    str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['diff']) + ' pont' + '\n' +
                    str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['diff']) + ' pont' + '\n' +
                    str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['diff']) + ' pont' + '\n' +
                    str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['diff']) + ' pont' + '\n' +
                    str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['diff']) + ' pont' + '\n' + '```', inline='false')

                    i = 30
                    embed.add_field(name='============ Top 31 - 40 ============', value=
                    '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['diff']) + ' pont' + '\n' +
                    str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['diff']) + ' pont' + '\n' +
                    str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['diff']) + ' pont' + '\n' +
                    str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['diff']) + ' pont' + '\n' +
                    str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['diff']) + ' pont' + '\n' +
                    str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['diff']) + ' pont' + '\n' +
                    str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['diff']) + ' pont' + '\n' +
                    str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['diff']) + ' pont' + '\n' +
                    str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['diff']) + ' pont' + '\n' +
                    str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['diff']) + ' pont' + '\n' + '```', inline='false')

                    i = 40
                    embed.add_field(name='============ Top 41 - 50 ============', value=
                    '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['diff']) + ' pont' + '\n' +
                    str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['diff']) + ' pont' + '\n' +
                    str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['diff']) + ' pont' + '\n' +
                    str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['diff']) + ' pont' + '\n' +
                    str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['diff']) + ' pont' + '\n' +
                    str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['diff']) + ' pont' + '\n' +
                    str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['diff']) + ' pont' + '\n' +
                    str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['diff']) + ' pont' + '\n' +
                    str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['diff']) + ' pont' + '\n' +
                    str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['diff']) + ' pont' + '\n' + '```', inline='false')

                    await ctx.send(embed=embed)

                    await ctx.message.add_reaction("✅")
                    print("Guild rang betöltés kész!")

                else:
                    await ctx.send("Cseréld fel a hónapokat")
                    print("Hibás hónap sorrend. Az első nagyobb mint a második!")

            if temp != -1 and myresult != None and month2 == 'mth2' and (
                    month1 == 'jan' or month1 == '1' or month1 == 'feb' or month1 == '2' or month1 == 'mar' or month1 == '3' or \
                    month1 == 'apr' or month1 == '4' or month1 == 'may' or month1 == '5' or month1 == 'jun' or month1 == '6' or month1 == 'jul' or month1 == '7' or \
                    month1 == 'aug' or month1 == '8' or month1 == 'sep' or month1 == '9' or month1 == 'okt' or month1 == '10' or month1 == 'nov' or month1 == '11' or month1 == 'dec' or month1 == '12'):

                honap1 = cmd_guild_save.switch_month_names(month1)

                print(str(month1) + " " + str(month2) + " " + str(honap1))

                await ctx.message.add_reaction("✅")

                await ctx.send(honap1 + "i Guild rang betöltés folyamatban. ⏳")
                print("Guild rang betöltés folyamatban.")

                player = fetchPlayerRoster(raw_guild)

                i = 0
                k = 0
                y: int = 0
                n = int_(len(player))

                while k < n:
                    sql = "SELECT " + honap1 + " FROM pilvax WHERE Allycode = %s"
                    adr = (player[k]['allycode'],)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        player[k]['rank1'] = x[0]
                    if player[k]['rank1'] == 0:
                        player[k]['rank1'] = -1
                    k += 1

                player.sort(reverse=True, key=Sortb)

                i = 0
                lth = 0
                while i < n:
                    lth2 = int_(len(player[i]['jatekosnev']))
                    if lth2 > lth:
                        lth = lth2
                    i += 1

                embed = discord.Embed(title='Pilvax Hungary ' + honap1 + 'i rang táblázata',
                                      url="https://swgoh.gg/g/1294/pilvax-hungary/",
                                      color=0x7289da)

                i = 0
                embed.add_field(name='======== Top 10 Rangú játékos ========', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank1']) + ' pont' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['rank1']) + ' pont' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['rank1']) + ' pont' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['rank1']) + ' pont' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['rank1']) + ' pont' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['rank1']) + ' pont' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['rank1']) + ' pont' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['rank1']) + ' pont' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['rank1']) + ' pont' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['rank1']) + ' pont' + '\n' + '```', inline='false')

                i = 10
                embed.add_field(name='============ Top 11 - 20 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank1']) + ' pont' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['rank1']) + ' pont' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['rank1']) + ' pont' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['rank1']) + ' pont' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['rank1']) + ' pont' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['rank1']) + ' pont' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['rank1']) + ' pont' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['rank1']) + ' pont' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['rank1']) + ' pont' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['rank1']) + ' pont' + '\n' + '```', inline='false')

                i = 20
                embed.add_field(name='============ Top 21 - 30 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank1']) + ' pont' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['rank1']) + ' pont' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['rank1']) + ' pont' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['rank1']) + ' pont' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['rank1']) + ' pont' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['rank1']) + ' pont' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['rank1']) + ' pont' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['rank1']) + ' pont' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['rank1']) + ' pont' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['rank1']) + ' pont' + '\n' + '```', inline='false')

                i = 30
                embed.add_field(name='============ Top 31 - 40 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank1']) + ' pont' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['rank1']) + ' pont' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['rank1']) + ' pont' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['rank1']) + ' pont' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['rank1']) + ' pont' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['rank1']) + ' pont' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['rank1']) + ' pont' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['rank1']) + ' pont' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['rank1']) + ' pont' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['rank1']) + ' pont' + '\n' + '```', inline='false')

                i = 40
                embed.add_field(name='============ Top 41 - 50 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['rank1']) + ' pont' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['rank1']) + ' pont' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['rank1']) + ' pont' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['rank1']) + ' pont' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['rank1']) + ' pont' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['rank1']) + ' pont' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['rank1']) + ' pont' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['rank1']) + ' pont' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['rank1']) + ' pont' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['rank1']) + ' pont' + '\n' + '```', inline='false')

                await ctx.send(embed=embed)

                await ctx.message.add_reaction("✅")
                print("Guild rang betöltés kész!")

            else:
                await ctx.message.add_reaction("❌")

            mycursor.close()
            mydb.close()

            toc()

            if month1 == "mth1" and month2 == "mth2":
                await ctx.send("Nem adtál meg hónapot!")

        else:
            pass


    @load.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


def Sorta(a):
    return a['diff']

def Sortb(a):
    return a['rank1']

def fetchPlayerRoster(guilddata):
    player = [{'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, {'jatekosnev': ' ', 'allycode': 0, 'rank1': 0, 'rank2': 0, 'diff': 0}, ]

    k = 0
    lth = int_(len(guilddata[0]['roster']))

    while k < lth:
        player[k]['jatekosnev'] = guilddata[0]['roster'][k]['name']
        player[k]['allycode'] = guilddata[0]['roster'][k]['allyCode']
        k += 1

    return player

def check_month(month):
    if month == 'Januar':
        honap = 1
    if month == 'Februar':
        honap = 2
    if month == 'Marcius':
        honap = 3
    if month == 'Aprilis':
        honap = 4
    if month == 'Majus':
        honap = 5
    if month == 'Junius':
        honap = 6
    if month == 'Julius':
        honap = 7
    if month == 'Augusztus':
        honap = 8
    if month == 'Szeptember':
        honap = 9
    if month == 'Oktober':
        honap = 10
    if month == 'November':
        honap = 11
    if month == 'December':
        honap = 12
    return honap


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
    bot.add_cog(Guildload(bot))


