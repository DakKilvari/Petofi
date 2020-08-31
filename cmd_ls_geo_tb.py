from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
from discord.ext import commands
import discord
import time
import global_settings

creds = settings()
client = api_swgoh_help(creds)

class LsGeoTb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['LS geo tb-hez guild készenlét ellenőrző'])
    @commands.has_any_role(global_settings.Role1, global_settings.Role2)  # User need this role to run command (can have multiple)
    async def lsgeotb(self, ctx, raw_allycode):
        """LS geo tb-hez guild készenlét ellenőrző
        Végigelemzi az egyes fázisok készenléti állapotát combat és sm pályákra.
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

            print("\n" + "LS Geo TB lekérés folyamatban.")

            guilddata = fetchGuildRoster(raw_guild)

            embed = discord.Embed(title='LS Geo TB Ki-Adi-Mundi áttekintő',
                                  url="https://swgoh.gg/p/" + str(raw_guild[0]['roster'][0]['allyCode']) + "/",
                                  color=0x7289da)

            player = character_data_search_Ki_Adi_Mundi(guilddata)

            n = int_(len(player))

            guild_meglevo = []
            guild_hianyzo = []

            i = 0
            k = 0
            j = 0
            for n in player:
                if player[i]['chars'] == 1:
                    guild_meglevo.insert(k, player[i]['jatekosnev'])
                    k += 1
                else:
                    guild_hianyzo.insert(j, player[i]['jatekosnev'])
                    j += 1
                i += 1

            guild_meglevo.sort()
            guild_hianyzo.sort()

            s1: str = '\n'.join(map(str, guild_meglevo))
            n1: int = len(guild_meglevo)
            s2: str = '\n'.join(map(str, guild_hianyzo))
            n2: int = len(guild_hianyzo)

            embed.add_field(name=str(n1) + ' játékos áll készen Ki-Adi-Mundi shard megszerzésére:',
                            value='```' + "\n" + s1 + '```', inline='false')
            embed.add_field(name=str(n2) + ' játékos nem áll készen Ki-Adi-Mundi shard megszerzésére:',
                            value='```' + "\n" + s2 + '```', inline='false')

            await ctx.send(embed=embed)

            toc()

        else:
            pass


    @lsgeotb.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


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


def character_data_search_Ki_Adi_Mundi(guilddata):
    i = 0
    player = [{'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0},
              {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}, {'jatekosnev': ' ', 'chars': 0}]

    for a in guilddata:
        chardata = guilddata[i]['roster']
        aa = 0
        ab = 0
        ac = 0
        ad = 0
        ae = 0
        j = 0
        for b in chardata:
            if chardata[j]['defId'] == "CT210408" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                aa = 1
            if chardata[j]['defId'] == "CT5555" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ab = 1
            if chardata[j]['defId'] == "CT7567" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ac = 1
            if chardata[j]['defId'] == "ARCTROOPER501ST" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ad = 1
            if chardata[j]['defId'] == "SHAAKTI" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            player[i]['jatekosnev'] = guilddata[i]['name']
        else:
            player[i]['jatekosnev'] = guilddata[i]['name']
            player[i]['chars'] += 1
        i += 1

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
    bot.add_cog(LsGeoTb(bot))