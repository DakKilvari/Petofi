from api_swgoh_help import api_swgoh_help, settings
from numpy import *
from discord.ext.commands import Bot
import discord
import time

creds = settings('USERNAME', 'PASSWORD')

client = api_swgoh_help(creds)

class DS_Geo_TB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['DS Geo TB'])
    @commands.has_any_role('CobraAdmin')  # User need this role to run command (can have multiple)
    async def DS_Geo_TB(self, ctx, allycode: int):
        tic()
        await ctx.message.add_reaction("⏳")

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

            guilddata = fetchGuildRoster(raw_guild)

            embed = discord.Embed(title='DS Geo TB Wat Tambor special mission', url="https://swgoh.gg/p/" + str(raw_guild[0]['roster'][0]['allyCode']) + "/", color=0x7289da)


            guild_members = character_data_search_P2(guilddata)

            s:str = '\n'.join(map(str, guild_members))
            n:int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen P2 Dooku & Asajj pályára:', value='```' + s + '```')

            guild_members = character_data_search_P3(guilddata)

            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen P3 szepa droidos pályára:', value='```' + s + '```')

            guild_members = character_data_search_Wat_Tambor(guilddata)

            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen Wat Tambor shard megszerzésére:', value='```' + s + '```')



            await ctx.send(embed=embed)

            toc()

        else:
            pass


    @DS_Geo_TB.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("Permission error!!!")
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


def character_data_search_Wat_Tambor(guilddata):
    k = 0
    i = 0
    chardata_ally = []
    for a in guilddata:
        chardata = guilddata[i]['roster']
        aa = 0
        ab = 0
        ac = 0
        ad = 0
        ae = 0
        j = 0
        for b in chardata:
            if chardata[j]['defId'] == "GEONOSIANBROODALPHA" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                aa = 1
            if chardata[j]['defId'] == "GEONOSIANSOLDIER" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                ab = 1
            if chardata[j]['defId'] == "GEONOSIANSPY" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                ac = 1
            if chardata[j]['defId'] == "POGGLETHELESSER" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                ad = 1
            if chardata[j]['defId'] == "SUNFAC" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally

def character_data_search_P3(guilddata):
    k = 0
    i = 0
    chardata_ally = []
    for a in guilddata:
        chardata = guilddata[i]['roster']
        aa = 0
        ab = 0
        ac = 0
        ad = 0
        ae = 0
        j = 0
        for b in chardata:
            if chardata[j]['defId'] == "GRIEVOUS" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 9:
                aa = 1
            if chardata[j]['defId'] == "B1BATTLEDROIDV2" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 9:
                ab = 1
            if chardata[j]['defId'] == "B2SUPERBATTLEDROID" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 9:
                ac = 1
            if chardata[j]['defId'] == "DROIDEKA" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 9:
                ad = 1
            if chardata[j]['defId'] == "MAGNAGUARD" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] >= 9:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally

def character_data_search_P2(guilddata):
    k = 0
    i = 0
    chardata_ally = []
    for a in guilddata:
        chardata = guilddata[i]['roster']
        aa = 0
        ab = 0
        ac = 0
        ad = 0
        ae = 0
        j = 0
        for b in chardata:
            if chardata[j]['defId'] == "COUNTDOOKU" and chardata[j]['rarity'] == 6 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                aa = 1
            if chardata[j]['defId'] == "ASAJVENTRESS" and chardata[j]['rarity'] == 6 and chardata[j]['gear'] >= 11 and chardata[j]['gp'] > 16499:
                ab = 1
            j += 1
        if aa != 1 or ab != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally



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
    bot.add_cog(TW(bot))
