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

            embed = discord.Embed(title='LS Geo TB P1-P2-P3 áttekintő', url="https://swgoh.gg/p/" + str(raw_guild[0]['roster'][0]['allyCode']) + "/", color=0x7289da)

            guild_members = character_data_search_GR1(guilddata)

            guild_members.sort()
            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen 1. GR csapattal (Shaak Ti, ARC, Echo, Rex, Fives):', value='```' + "\n" + s + '```', inline='true')


            guild_members = character_data_search_GR2(guilddata)

            guild_members.sort()
            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen 2. GR csapattal (Padme, JKA, GK, Ahsoka, C-3PO)', value='```' + "\n" + s + '```', inline='true')


            guild_members = character_data_search_Jedi1(guilddata)

            guild_members.sort()
            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen 1. Jedi csapattal (JML, JKR, GMY, Jolee, Bastila):', value='```' + "\n" + s + '```', inline='true')


            guild_members = character_data_search_Jedi2(guilddata)

            guild_members.sort()
            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen 2. Jedi csapattal (JKL, GAS, Hoda, OB, Zariss):', value='```' + "\n" + s + '```', inline='true')


            guild_members = character_data_search_Resi(guilddata)

            guild_members.sort()
            s: str = '\n'.join(map(str, guild_members))
            n: int = len(guild_members)
            embed.add_field(name=str(n) + ' játékos nem áll készen Resi csapattal (Rey, H.Finn, Han, Chewie, L3):', value='```' + "\n" + s + '```', inline='true')

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


def character_data_search_GR1(guilddata):
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
            if chardata[j]['defId'] == "SHAAKTI" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                aa = 1
            if chardata[j]['defId'] == "ARCTROOPER501ST" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 6:
                ab = 1
            if chardata[j]['defId'] == "CT210408" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 6:
                ac = 1
            if chardata[j]['defId'] == "CT7567" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ad = 1
            if chardata[j]['defId'] == "CT5555" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally


def character_data_search_GR2(guilddata):
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
            if chardata[j]['defId'] == "PADMEAMIDALA" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 4:
                aa = 1
            if chardata[j]['defId'] == "ANAKINKNIGHT" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                ab = 1
            if chardata[j]['defId'] == "GENERALKENOBI" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                ac = 1
            if chardata[j]['defId'] == "AHSOKATANO" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 4:
                ad = 1
            if chardata[j]['defId'] == "C3POLEGENDARY" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally


def character_data_search_Jedi1(guilddata):
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
            if chardata[j]['defId'] == "GRANDMASTERLUKE" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                aa = 1
            if chardata[j]['defId'] == "JEDIKNIGHTREVAN" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ab = 1
            if chardata[j]['defId'] == "GRANDMASTERYODA" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ac = 1
            if chardata[j]['defId'] == "JOLEEBINDO" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ad = 1
            if chardata[j]['defId'] == "BASTILASHAN" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally


def character_data_search_Jedi2(guilddata):
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
            if chardata[j]['defId'] == "JEDIKNIGHTLUKE" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                aa = 1
            if chardata[j]['defId'] == "GENERALSKYWALKER" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                ab = 1
            if chardata[j]['defId'] == "HERMITYODA" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ac = 1
            if chardata[j]['defId'] == "OLDBENKENOBI" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ad = 1
            if chardata[j]['defId'] == "BARRISSOFFEE" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
            chardata_ally.insert(k, guilddata[i]['name'])
            k += 1
        i += 1

    return chardata_ally


def character_data_search_Resi(guilddata):
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
            if chardata[j]['defId'] == "GLREY" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 7:
                aa = 1
            if chardata[j]['defId'] == "EPIXFINN" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 5:
                ab = 1
            if chardata[j]['defId'] == "HANSOLO" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 4:
                ac = 1
            if chardata[j]['defId'] == "CHEWBACCALEGENDARY" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 4:
                ad = 1
            if chardata[j]['defId'] == "L3_37" and chardata[j]['rarity'] == 7 and chardata[j]['gear'] == 13 and (chardata[j]['relic']['currentTier']-2) >= 3:
                ae = 1
            j += 1
        if aa != 1 or ab != 1 or ac != 1 or ad != 1 or ae != 1:
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
    bot.add_cog(LsGeoTb(bot))