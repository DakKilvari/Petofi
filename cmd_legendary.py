from api_swgoh_help import api_swgoh_help, settings
from numpy import *
from discord.utils import get
import time
from discord.ext import commands
from db_handler import db_handler
import global_settings


class Legendary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Pánik figyelő'])
    @commands.has_any_role(global_settings.Role3)  # User need this role to run command (can have multiple)
    async def panic(self, ctx, raw_allycode, show="b", show2="b"):
        """Pánik figyelő
        Legfrissebb kulcskarakterek megszerzéséhez
        raw_allycode: me / taggelés / allykód
        show: slkr, rey, jkl, jml, see, kam"""

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

        if isinstance(raw_player, str):
            await ctx.send("Api error: " + raw_player)

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

            if show == "örökélet":
                await ctx.send("Még legalább 1 GL-t ki kell farmolnod hozzá! 🍺")
                return
            if show == "ingyensör":
                await ctx.send("Azt az új belépők fizetik! 🍺")
                return

            if show != "Rey" and show != "rey" and show != "SLKR" and show != "slkr" and show != "JMK" and show != "jmk" and show != "KAM" and show != "kam" and show != "JKL" and show != "jkl" and show != "JML" and show != "jml" and show != "SEE" and show != "see" and show != "lordvader" and show != "LORDVADER" and show != "executor" and show != "EXECUTOR":
                await ctx.send(ctx.message.author.mention + " Nem adtál meg parancsot! / Ilyen parancs nincs még. :)")
            else:
                if show == "Rey" or show == "rey":
                    player = fetchPlayerRey(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " Galactic Legends Rey eventre állása: ")

                if show == "SLKR" or show == "slkr":
                    player = fetchPlayerSLKR(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " Galactic Legends SLKR eventre állása: ")

                if show == "KAM" or show == "kam":
                    player = fetchPlayerKAM(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " KAM SM-re állása: ")

                if show == "JKL" or show == "jkl":
                    player = fetchPlayerJKL(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " JKL legendary eventre állása: ")

                if show == "JML" or show == "jml":
                    player = fetchPlayerJML(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " JML legendary eventre állása: ")

                if show == "SEE" or show == "see":
                    player = fetchPlayerSEE(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " SEE legendary eventre állása: ")

                if show == "JMK" or show == "jmk":
                    player = fetchPlayerJMK(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " JMK legendary eventre állása: ")

                if show == "LORDVADER" or show == "lordvader":
                    player = fetchPlayerLVD(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " Lord Vader legendary eventre állása: ")

                if show == "EXECUTOR" or show == "executor":
                    player = fetchPlayerExec(ctx, raw_player[0])
                    await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " Executor legendary eventre állása: ")

                player['chars'].sort()
                player['ships'].sort()
                player['miss'].sort()
                player['missShips'].sort()

                message1 = "\n**Meglévő karakterek:** \n"
                message2 = "\n**Meglévő hajók:** \n"
                message3 = "\n**Hiányzó karakterek:** \n"
                message4 = "\n**Hiányzó hajók:** \n"

                for c in player['chars']:
                    message1 += '`' + c.ljust(40, ' ') + '`\n'
                for c in player['ships']:
                    message2 += '`' + c.ljust(40, ' ') + '`\n'
                for c in player['miss']:
                    message3 += '`' + c.ljust(40, ' ') + '`\n'
                for c in player['missShips']:
                    message4 += '`' + c.ljust(40, ' ') + '`\n'


                if show2 == "b" or show2 == "m":
                    if message1 != "\n**Meglévő karakterek:** \n":
                        await ctx.send(message1)
                    if message2 != "\n**Meglévő hajók:** \n":
                        await ctx.send(message2)
                if show2 == "b" or show2 == "h":
                    if message3 != "\n**Hiányzó karakterek:** \n":
                        await ctx.send(message3)
                    if message4 != "\n**Hiányzó hajók:** \n":
                        await ctx.send(message4)
                    if (message3 == "\n**Hiányzó karakterek:** \n" ) and (message4 == "\n**Hiányzó hajók:** \n"  ):
                        await ctx.send("Nincsen hátra semmi, készen állsz az eventre! Gratulálok! 🍺")

            toc()

        else:
            pass

    @panic.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def fChar(ctx, player, raw_player, defID, realName, gear, zeta, relic, pont):
    retval = 0
    missingChar = 1
    i = 0

    relicE = '`' + str(get(ctx.bot.emojis, name="relic")) + '`'
    gearE = '`:gear:`'
    lockE = '`:lock:`'
    starE = '`:star:`'

    printName = realName
    l = len(printName)
    
    for a in raw_player['roster']:
        a = raw_player['roster'][i]

        if a['defId'] == defID:
            missingChar = 0
            if a['rarity'] < 7:
                player['miss'].insert(player['rank'], printName + (31-l)* ' ' + str(starE) + ': ' + str(a['rarity']) + '/ ' + str(7) + '')
            else:
                printrelic = str(a['relic']['currentTier']-2)
                if printrelic == '-1':
                    printrelic = '0'
    
                printgear = str(a['gear'])
                if a['gear'] < 10:
                    printgear = ' ' + str(a['gear'])

                if a['gear'] >= gear and (a['relic']['currentTier']-2) >= relic:
                    l2 = len(str(a['gear']))
                    player['chars'].insert(player['rank'], printName)
              
                    retval = 1
                else:
                    l2 = len(str(a['gear']))
                    if a['gear'] >= gear:
                        player['miss'].insert(player['rank'], printName + (30-l)* ' ' + ' ' + str(relicE) + ': ' + printrelic + '/ ' + str(relic))
                    else:
                        player['miss'].insert(player['rank'], printName + (30-l)* ' ' + ' ' + str(gearE) + ':' + printgear + '/' + str(gear))
        i += 1
    if missingChar == 1:
        player['miss'].insert(player['rank'], printName + (30-l)* ' ' + ' ' + str(lockE) + '      ')
    return retval


def fShip(ctx, player, raw_player, defID, realName, rarity):
    missingChar = 1
    printName = realName
    l = len(printName)

    starE = '`:star:`'
    lockE = '`:lock:`'

    i = 0
    for a in raw_player['roster']:
        a = raw_player['roster'][i]
        if a['defId'] == defID:
            missingChar = 0
            if a['rarity'] < rarity:
                player['missShips'].insert(player['rank'], printName + (31-l)* ' ' + str(starE) + ': ' + str(a['rarity']) + '/ ' + str(rarity) + '')
            else:
                player['ships'].insert(player['rank'], printName)
        i += 1
    if missingChar == 1:
        player['missShips'].insert(player['rank'], printName + (31-l)* ' ' + str(lockE) + '      ')
    return


def fetchPlayerRey(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']
    fChar(ctx, player, raw_player, "REYJEDITRAINING", "Rey (Jedi Training)", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "BB8", "BB-8", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "FINN", "Finn", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "POE", "Poe Dameron", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "EPIXFINN", "Resistance Hero Finn", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "EPIXPOE", "Resistance Hero Poe", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "RESISTANCEPILOT", "Resistance Pilot", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "RESISTANCETROOPER", "Resistance Trooper", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "REY", "Rey (Scavenger)", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "ROSETICO", "Rose Tico", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "SMUGGLERCHEWBACCA", "Veteran Smuggler Chewbacca", 13, 0, 3, 1)
    fShip(ctx, player, raw_player, "CAPITALRADDUS", "Raddus", 5)
    return player

def fetchPlayerSLKR(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "KYLORENUNMASKED", "Kylo Ren (Unmasked)", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "FIRSTORDEREXECUTIONER", "First Order Executioner", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "FIRSTORDEROFFICERMALE", "First Order Officer", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "FIRSTORDERSPECIALFORCESPILOT", "First Order SF TIE Pilot", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "FIRSTORDERTROOPER", "First Order Stromtrooper", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "FIRSTORDERTIEPILOT", "First Order TIE Pilot", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "KYLOREN", "Kylo Ren", 13, 1, 7, 1)
    fChar(ctx, player, raw_player, "PHASMA", "Captain Phasma", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "SMUGGLERHAN", "Veteran Smuggler Han Solo", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "FOSITHTROOPER", "Sith Trooper", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "GENERALHUX", "General Hux", 13, 1, 5, 1)
    fChar(ctx, player, raw_player, "EMPERORPALPATINE", "Emperor Palpatine", 13, 2, 7, 1)

    fShip(ctx, player, raw_player, "CAPITALFINALIZER", "Finalizer", 5)

    return player

def fetchPlayerKAM(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "SHAAKTI", "Shaak Ti", 13, 2, 3, 1)
    fChar(ctx, player, raw_player, "CT210408", "Echo", 13, 1, 6, 1)
    fChar(ctx, player, raw_player, "CT7567", "Rex", 13, 1, 5, 1)
    fChar(ctx, player, raw_player, "CT5555", "Fives", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "ARCTROOPER501ST", "ARC Trooper", 13, 1, 6, 1)

    return player

def fetchPlayerJKL(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "COMMANDERLUKESKYWALKER", "Commander Luke Skywalker", 13, 3, 3, 1)
    fChar(ctx, player, raw_player, "HOTHLEIA", "Rebel Officer Leia Organa", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "HOTHHAN", "Captain Han Solo", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "WAMPA", "Wampa", 13, 1, 3, 1)
    fChar(ctx, player, raw_player, "CHEWBACCALEGENDARY", "Chewbacca", 13, 2, 3, 1)
    fChar(ctx, player, raw_player, "VADER", "Darth Vader", 13, 3, 3, 1)
    fChar(ctx, player, raw_player, "C3POLEGENDARY", "C3PO", 13, 1, 3, 1)
    fChar(ctx, player, raw_player, "ADMINISTRATORLANDO", "Lando Calrissian", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "HERMITYODA", "Hermit Yoda", 13, 1, 3, 1)

    return player

def fetchPlayerJML(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "REYJEDITRAINING", "Rey (Jedi Training)", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "BIGGSDARKLIGHTER", "Biggs Darklighter", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "C3POLEGENDARY", "C3PO", 13, 1, 5, 1)
    fChar(ctx, player, raw_player, "CHEWBACCALEGENDARY", "Chewbacca", 13, 2, 6, 1)
    fChar(ctx, player, raw_player, "HANSOLO", "Han Solo", 13, 1, 6, 1)
    fChar(ctx, player, raw_player, "HERMITYODA", "Hermit Yoda", 13, 1, 5, 1)
    fChar(ctx, player, raw_player, "JEDIKNIGHTLUKE", "Jedi Knight Luke Skywalker", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "ADMINISTRATORLANDO", "Lando Calrissian", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "PRINCESSLEIA", "Princess Leia", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "MONMOTHMA", "Mon Mothma", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "OLDBENKENOBI", "Obi-Wan Kenobi (Old Ben)", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "R2D2_LEGENDARY", "R2D2", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "C3POCHEWBACCA", "Threepio & Chewie", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "WEDGEANTILLES", "Wedge Antilles", 13, 0, 3, 1)

    fShip(ctx, player, raw_player, "YWINGREBEL", "Rebel Y-wing", 6)

    return player

def fetchPlayerSEE(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "COUNTDOOKU", "Count Dooku", 13, 1, 6, 1)
    fChar(ctx, player, raw_player, "EMPERORPALPATINE", "Emperor Palpatine", 13, 2, 7, 1)
    fChar(ctx, player, raw_player, "ANAKINKNIGHT", "Anakin Skywalker", 13, 1, 7, 1)
    fChar(ctx, player, raw_player, "DIRECTORKRENNIC", "Director Krennic", 13, 0, 4, 1)
    fChar(ctx, player, raw_player, "SITHMARAUDER", "Sith Marauder", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "MAUL", "Darth Maul", 13, 0, 4, 1)
    fChar(ctx, player, raw_player, "ADMIRALPIETT", "Admiral Piett", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "ROYALGUARD", "Royal Guard", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "DARTHSIDIOUS", "Darth Sidious", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "COLONELSTARCK", "Colonel Starck", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "GRANDMOFFTARKIN", "Grand Moff Tarkin", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "GRANDADMIRALTHRAWN", "Grand Admiral Thrawn", 13, 1, 6, 1)
    fChar(ctx, player, raw_player, "VADER", "Darth Vader", 13, 3, 7, 1)
    fChar(ctx, player, raw_player, "VEERS", "General Veers", 13, 0, 3, 1)

    fShip(ctx, player, raw_player, "TIEBOMBERIMPERIAL", "Imperial TIE Bomber", 6)

    return player


def fetchPlayerJMK(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "GENERALKENOBI", "General Kenobi", 13, 0, 8, 1)
    fChar(ctx, player, raw_player, "MACEWINDU", "Mace Windu", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "AAYLASECURA", "Aayla Secura", 13, 0, 3, 1)
    fChar(ctx, player, raw_player, "BOKATAN", "Bo-Katan Kryze", 13, 0, 5, 1)

    fShip(ctx, player, raw_player, "CAPITALNEGOTIATOR", "Negotiator", 6)

    fChar(ctx, player, raw_player, "GRIEVOUS", "General Grievous", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "WATTAMBOR", "Wat Tambor", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "CLONESERGEANTPHASEI", "Clone Sergeant - Phase I", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "MAGNAGUARD", "IG-100 MagnaGuard", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "QUIGONJINN", "Qui-Gon Jinn", 13, 0, 3, 1)

    fChar(ctx, player, raw_player, "JANGOFETT", "Jango Fett", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "CADBANE", "Cad Bane", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "SHAAKTI", "Shaak Ti", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "CC2224", "CC-2224 Cody", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 13, 0, 8, 1)

    return player

def fetchPlayerLVD(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "PADMEAMIDALA", "Padme Amidala", 13, 0, 8, 1)
    fChar(ctx, player, raw_player, "GENERALSKYWALKER", "General Skywalker", 13, 0, 8, 1)
    fChar(ctx, player, raw_player, "BADBATCHHUNTER", "Hunter ", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "BADBATCHTECH", "Tech", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "BADBATCHWRECKER", "Wrecker", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "TUSKENRAIDER", "Tusken Raider", 13, 0, 5, 1)

    return player

def fetchPlayerExec(ctx, raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(ctx, player, raw_player, "VADER", "Darth Vader", 13, 0, 7, 1)
    fChar(ctx, player, raw_player, "ADMIRALPIETT", "Admiral Piett", 13, 0, 8, 1)
    fChar(ctx, player, raw_player, "BOBAFETT", "Boba Fett ", 13, 0, 8, 1)
    fChar(ctx, player, raw_player, "TIEFIGHTERPILOT", "TIE Fighter Pilot", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "BOSSK", "Bossk", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "IG88", "IG88", 13, 0, 5, 1)
    fChar(ctx, player, raw_player, "DENGAR", "Dengar", 13, 0, 5, 1)

    fShip(ctx, player, raw_player, "RAZORCREST", "Razor Crest", 7)
    fShip(ctx, player, raw_player, "SLAVE1", "Slave I", 7)
    fShip(ctx, player, raw_player, "IG2000", "IG-2000", 7)
    fShip(ctx, player, raw_player, "HOUNDSTOOTH", "Hound's Tooth", 7)
    fShip(ctx, player, raw_player, "TIEADVANCED", "TIE Advanced", 7)
    fShip(ctx, player, raw_player, "TIEBOMBERIMPERIAL", "TIE Bomber", 7)
    fShip(ctx, player, raw_player, "TIEFIGHTERIMPERIAL", "Imperial TIE Fighter", 7)

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
    bot.add_cog(Legendary(bot))
