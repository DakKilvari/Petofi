from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import time
from discord.ext import commands
from db_handler import db_handler


class LENGEDARY(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['PanicFigyelo'])
    @commands.has_any_role('Member')  # User need this role to run command (can have multiple)
    async def panic(self, ctx, raw_allycode, show="b"):
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

            print("\n" + raw_player[0]['name'] + "-tól rang lekérés.")

            await ctx.message.add_reaction("✅")

            if show == "Rey":
                player = fetchPlayerRey(raw_player[0])

                player['chars'].sort()
                player['ships'].sort()
                player['miss'].sort()
                player['missShips'].sort()

                await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " Galactic Legends Rey eventre állása: ")

                s: str = '\n'.join(map(str, player['chars']))
                s2: str = '\n'.join(map(str, player['ships']))
                s3: str = '\n'.join(map(str, player['miss']))
                s4: str = '\n'.join(map(str, player['missShips']))

                message1 = ""
                message2 = ""
                message3 = ""
                message4 = ""

                message1 += "\n**Meglévő karakterek:** \n" + str("```ini\n" + s + "```")
                message2 += "\n**Meglévő hajók:** \n" + str("```ini\n" + s2 + "```")
                message3 += "\n**Hiányzó karakterek:** \n" + str("```ini\n" + s3 + "```")
                message4 += "\n**Hiányzó hajók:** \n" + str("```ini\n" + s4 + "```")

                if message1 != "\n**Meglévő karakterek:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message1)
                if message2 != "\n**Meglévő hajók:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message2)
                if message3 != "\n**Hiányzó karakterek:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message3)
                if message4 != "\n**Hiányzó hajók:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message4)



            if show == "SLKR" or show == "slkr":
                player = fetchPlayerSLKR(raw_player[0])

                player['chars'].sort()
                player['ships'].sort()
                player['miss'].sort()
                player['missShips'].sort()

                await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " Galactic Legends SLKR eventre állása: ")

                s: str = '\n'.join(map(str, player['chars']))
                s2: str = '\n'.join(map(str, player['ships']))
                s3: str = '\n'.join(map(str, player['miss']))
                s4: str = '\n'.join(map(str, player['missShips']))

                message1 = ""
                message2 = ""
                message3 = ""
                message4 = ""

                message1 += "\n**Meglévő karakterek:** \n" + str("```ini\n" + s + "```")
                message2 += "\n**Meglévő hajók:** \n" + str("```ini\n" + s2 + "```")
                message3 += "\n**Hiányzó karakterek:** \n" + str("```ini\n" + s3 + "```")
                message4 += "\n**Hiányzó hajók:** \n" + str("```ini\n" + s4 + "```")

                if message1 != "\n**Meglévő karakterek:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message1)
                if message2 != "\n**Meglévő hajók:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message2)
                if message3 != "\n**Hiányzó karakterek:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message3)
                if message4 != "\n**Hiányzó hajók:** \n" + str("```ini\n" + "```"):
                    await ctx.send(message4)


            if show != "Rey" and show != "SLKR":
                await ctx.send(ctx.message.author.mention + " Nem adtál meg parancsot! / Ilyen parancs nincs még. :)")

            toc()

        else:
            pass

    @panic.error
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
    if pont > 1:
        printName += ' ' + str(pont)

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

            if a['gear'] >= gear and a['relic']['currentTier'] >= relic or (a['gear'] >= gear - 1 and pont > 1):
                l2 = len(str(a['gear']))
                if missingZeta == 0:
                        player['chars'].insert(player['rank'], printName)
                        if a['gear'] >= gear and a['relic']['currentTier'] >= relic:
                            player['rank'] += pont
                        else:
                            player['rank'] += 1
                            player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' (1P) G:' + str(a['gear']) + '/' + str(gear) + (2-l2)* ' ' + ' & R:' + str(a['relic']['currentTier']-1) + '/' + str(relic) + '')
                        retval = 1
                else:
                    player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' Z:' + str(temp) + '/' + str(zeta) + '')
            else:
                l2 = len(str(a['gear']))
                if missingZeta == 0:
                    player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' G:' + str(a['gear']) + '/' + str(gear) + (2-l2)* ' ' + ' & R:' + str(a['relic']['currentTier']-1) + '/' + str(relic) + '')
                else:
                    player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' G:' + str(a['gear']) + '/' + str(gear) + (2-l2)* ' ' + ' & R:' + str(a['relic']['currentTier']-1) + '/' + str(relic) + ' & Z:' + str(temp) + '/' + str(zeta) + '')
        i += 1
    if missingChar == 1:
        player['miss'].insert(player['rank'], printName + (26-l)* ' ' + ' L')
    return retval


def fShip(player, raw_player, defID, realName, skills, pilot1, pilot2, pilot3, pont):
    missingChar = 1
    printName = realName
    if pont > 1:
        printName += ' ' + str(pont)
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


def fetchPlayerRey(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "REYJEDITRAINING", "Rey (Jedi Training)", 13, 2, 7, 1)
    fChar(player, raw_player, "BB8", "BB-8", 13, 2, 7, 1)
    fChar(player, raw_player, "FINN", "Finn", 13, 0, 5, 1)
    fChar(player, raw_player, "POE", "Poe Dameron", 13, 0, 5, 1)
    fChar(player, raw_player, "EPIXFINN", "Resistance Hero Finn", 13, 0, 5, 1)
    fChar(player, raw_player, "EPIXPOE", "Resistance Hero Poe", 13, 0, 5, 1)
    fChar(player, raw_player, "RESISTANCEPILOT", "Resistance Pilot", 13, 0, 3, 1)
    fChar(player, raw_player, "RESISTANCETROOPER", "Resistance Trooper", 13, 0, 5, 1)
    fChar(player, raw_player, "REY", "Rey (Scavenger)", 13, 0, 7, 1)
    fChar(player, raw_player, "ROSETICO", "Rose Tico", 13, 0, 5, 1)
    fChar(player, raw_player, "SMUGGLERCHEWBACCA", "Veteran Smuggler Chewbacca", 13, 0, 3, 1)

    fShip(player, raw_player, "CAPITALRADDUS", "Raddus", 5, "AMILYNHOLDO", "", "", 1)

    return player

def fetchPlayerSLKR(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "KYLORENUNMASKED", "Kylo Ren (Unmasked)", 13, 2, 7, 1)
    fChar(player, raw_player, "FIRSTORDEREXECUTIONER", "First Order Executioner", 13, 0, 5, 1)
    fChar(player, raw_player, "FIRSTORDEROFFICERMALE", "First Order Officer", 13, 0, 5, 1)
    fChar(player, raw_player, "FIRSTORDERSPECIALFORCESPILOT", "First Order SF TIE Pilot", 13, 0, 5, 1)
    fChar(player, raw_player, "FIRSTORDERTROOPER", "First Order Stromtrooper", 13, 0, 5, 1)
    fChar(player, raw_player, "FIRSTORDERTIEPILOT", "First Order TIE Pilot", 13, 0, 3, 1)
    fChar(player, raw_player, "KYLOREN", "Kylo Ren", 13, 1, 7, 0)
    fChar(player, raw_player, "PHASMA", "Captain Phasma", 13, 0, 5, 1)
    fChar(player, raw_player, "SMUGGLERHAN", "Veteran Smuggler Han Solo", 13, 0, 3, 1)
    fChar(player, raw_player, "FOSITHTROOPER", "Sith Trooper", 13, 0, 5, 1)
    fChar(player, raw_player, "GENERALHUX", "General Hux", 13, 1, 5, 1)
    fChar(player, raw_player, "EMPERORPALPATINE", "Emperor Palpatine", 13, 2, 7, 1)

    fShip(player, raw_player, "CAPITALFINALIZER", "Finalizer", 5, "GENERALHUX", "", "", 1)

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
    bot.add_cog(LENGEDARY(bot))
