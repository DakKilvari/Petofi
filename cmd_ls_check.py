from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import time
from discord.ext import commands
from db_handler import db_handler
import global_settings
import discord


class LScheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['LScheck'])
    @commands.has_any_role(global_settings.Role3)  # User need this role to run command (can have multiple)
    async def lscheck(self, ctx, raw_allycode):
        """LS geo tb-hez egyéni készenlét ellenőrző
        Végigelemzi a szükséges csapatok készenléti állapotát combat és sm pályákra."""

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

            print("\n" + raw_player[0]['name'] + "-tól legendary lekérés.")

            await ctx.message.add_reaction("✅")

            player = fetchPlayerGR1(raw_player[0])

            embed = discord.Embed(title=player['jatekosnev'] + ' LS Geo TB roster áttekintő (hányzó karakterek)', url="https://swgoh.gg/p/", color=0x7289da)

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='1. GR csapat (Shaak Ti (r3), ARC (r6), Echo (r6), Rex (r5), Fives (r7)): ', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='1. GR csapat (Shaak Ti (r3), ARC (r6), Echo (r6), Rex (r5), Fives (r7)): ', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerGR2(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='2. GR csapata (Padme (r4), JKA (r7), GK (r7), Ahsoka (r4), C-3PO (r3)): ', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='2. GR csapata (Padme (r4), JKA (r7), GK (r7), Ahsoka (r4), C-3PO (r3)): ', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerJedi1(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='1. Jedi csapata (JML (r7), JKR (r3), GMY (r5), Jolee (r3), Bastila (r3)): ', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='1. Jedi csapata (JML (r7), JKR (r3), GMY (r5), Jolee (r3), Bastila (r3)): ', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerJedi2(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='2. Jedi csapata (JKL (r7), GAS (r7), Hoda (r3), OB (r5), Zariss (r5)): ', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='2. Jedi csapata (JKL (r7), GAS (r7), Hoda (r3), OB (r5), Zariss (r5)): ', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerResi(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='Resi csapata (Rey (r7), H.Finn (r5), Han (r4), Chewie (r4), L3 (r3)): ', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='Resi csapata (Rey (r7), H.Finn (r5), Han (r4), Chewie (r4), L3 (r3)): ', value='```' + "\n" + message4 + '```', inline='false')

            await ctx.send(embed=embed)

            toc()

        else:
            pass


    @lscheck.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def fChar(player, raw_player, defID, realName, gear, zeta, relic, pont):
    retval = 0
    missingZeta = 0
    missingChar = 1
    i = 0
    printName = realName
    l = len(printName)
    for a in raw_player['roster']:
        a = raw_player['roster'][i]
        if a['defId'] == defID:
            missingChar = 0
            temp = 0
            for b in a['skills']:
                if b['tier'] == b['tiers'] and b['isZeta'] == True:
                    temp += 1
            if temp >= zeta:
                missingZeta = 0
            else:
                missingZeta = 1

            if a['gear'] >= gear and (a['relic']['currentTier']-2) >= relic or (a['gear'] >= gear - 1 and pont > 1):
                l2 = len(str(a['gear']))
                if missingZeta == 0:
                        player['chars'].insert(player['rank'], printName)
                        if a['gear'] >= gear and (a['relic']['currentTier']-2) >= relic:
                            player['rank'] += pont
                        else:
                            player['rank'] += 1
                            if a['gear'] >= gear:
                                player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' R:' + str(a['relic']['currentTier']-2) + '/' + str(relic) + '')
                            if a['gear'] < gear:
                                player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' G:' + str(a['gear']) + '/' + str(gear) + '')
                        retval = 1
                else:
                    player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' Z:' + str(temp) + '/' + str(zeta) + '')
            else:
                l2 = len(str(a['gear']))
                if missingZeta == 0:
                    if a['gear'] >= gear:
                        player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' R:' + str(a['relic']['currentTier']-2) + '/' + str(relic) + '')
                    if a['gear'] < gear:
                        player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' G:' + str(a['gear']) + '/' + str(gear) + '')
                else:
                    if a['gear'] >= gear:
                        player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' R:' + str(a['relic']['currentTier']-2) + '/' + str(relic) + ' & Z:' + str(temp) + '/' + str(zeta) + '')
                    if a['gear'] < gear:
                        player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' G:' + str(a['gear']) + '/' + str(gear) + (2-l2)* ' ' + ' & Z:' + str(temp) + '/' + str(zeta) + '')
        i += 1
    if missingChar == 1:
        player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' L')
    return retval


def fShip(player, raw_player, defID, realName, skills, pilot1, pilot2, pilot3, pont):
    missingChar = 1
    printName = realName
    i = 0
    for a in raw_player['roster']:
        a = raw_player['roster'][i]
        if a['defId'] == defID:
            missingChar = 0
            if a['rarity'] >= 5 and a['level'] == 85:

                j = 0
                p1 = 0
                p2 = 0
                p3 = 0

                for b in raw_player['roster']:
                    b = raw_player['roster'][j]
                    if b['defId'] == pilot1 and b['gear'] >= 12 or pilot1 == "":
                        p1 = 1
                    if b['defId'] == pilot2 and b['gear'] >= 12 or pilot2 == "":
                        p2 = 1
                    if b['defId'] == pilot3 and b['gear'] >= 12 or pilot3 == "":
                        p3 = 1
                    j = j + 1

                if p1 == 1 and p2 == 1 and p3 == 1:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] >= 6:
                            temp += 1
                    if temp >= skills:
                        player['ships'].insert(player['rank'], printName)
                        player['rank'] += pont
                    else:
                        player['missShips'].insert(player['rank'],
                                                   printName + 'S:' + str(temp) + '/' + str(skills) + '')
                else:
                    needpilots = 0
                    if pilot1 != "":
                        needpilots += 1
                    if pilot2 != "":
                        needpilots += 1
                    if pilot3 != "":
                        needpilots += 1

                    sumpilots = 0
                    if p1 == 1:
                        sumpilots += 1
                        if p2 == 1:
                            sumpilots += 1
                            if p3 == 1:
                                sumpilots += 1
                    player['missShips'].insert(player['rank'],
                                               printName + ' P:' + str(sumpilots) + '/' + str(needpilots) + ' & S:' + str(a['rarity']) + '/5' + '')
            else:
                player['missShips'].insert(player['rank'], printName + ' S:' + str(a['rarity']) + '/5' + '')
        i += 1
    if missingChar == 1:
        player['missShips'].insert(player['rank'], printName + ' L')
    return


def fetchPlayerGR1(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']


    fChar(player, raw_player, "SHAAKTI", "Shaak Ti", 13, 2, 3, 1)
    fChar(player, raw_player, "ARCTROOPER501ST", "ARC Trooper", 13, 1, 6, 1)
    fChar(player, raw_player, "CT210408", "Echo", 13, 1, 6, 1)
    fChar(player, raw_player, "CT7567", "Rex", 13, 1, 5, 1)
    fChar(player, raw_player, "CT5555", "Fives", 13, 2, 7, 1)

    return player


def fetchPlayerGR2(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "PADMEAMIDALA", "Padme Amidala", 13, 2, 4, 3)
    fChar(player, raw_player, "ANAKINKNIGHT", "Jedi Knight Anakin", 13, 1, 7, 1)
    fChar(player, raw_player, "GENERALKENOBI", "General Kenobi", 13, 1, 7, 2)
    fChar(player, raw_player, "AHSOKATANO", "Ahsoka Tano", 13, 1, 4, 2)
    fChar(player, raw_player, "C3POLEGENDARY", "C-3PO", 13, 0, 3, 1)

    return player

def fetchPlayerJedi1(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "GRANDMASTERLUKE", "Jedi Master Luke Skywalker", 13, 6, 7, 5)
    fChar(player, raw_player, "JEDIKNIGHTREVAN", "Jedi Knight Revan", 13, 3, 3, 3)
    fChar(player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 13, 1, 5, 1)
    fChar(player, raw_player, "JOLEEBINDO", "Jolee Bindo", 13, 1, 3, 1)
    fChar(player, raw_player, "BASTILASHAN", "Bastila Shan", 13, 1, 3, 1)

    return player

def fetchPlayerJedi2(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "JEDIKNIGHTLUKE", "Jedi Knight Luke Skywalker", 13, 2, 7, 4)
    fChar(player, raw_player, "GENERALSKYWALKER", "General Skywalker", 13, 4,  7, 4)
    fChar(player, raw_player, "HERMITYODA", "Hermit Yoda", 13, 1, 3, 1)
    fChar(player, raw_player, "OLDBENKENOBI", "Obi-Wan Kenobi (Old Ben)", 13, 0, 5, 1)
    fChar(player, raw_player, "BARRISSOFFEE", "Barriss Offee", 13, 0, 1, 1)

    return player

def fetchPlayerResi(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "GLREY", "Rey", 13, 6, 7, 5)
    fChar(player, raw_player, "FINN", "Finn", 13, 0, 5, 1)
    fChar(player, raw_player, "HANSOLO", "Han Solo", 13, 1, 4, 1)
    fChar(player, raw_player, "CHEWBACCALEGENDARY", "Chewbacca", 13, 2, 4, 2)
    fChar(player, raw_player, "L3_37", "L3-37", 13, 0, 3, 1)

    return player

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
    bot.add_cog(LScheck(bot))