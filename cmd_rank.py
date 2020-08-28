from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import time
from discord.ext import commands
import global_settings


class RANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['JatekosRang'])
    @commands.has_any_role(global_settings.Role3)  # User need this role to run command (can have multiple)
    async def rang(self, ctx, raw_allycode, show="b"):

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

            player = fetchPlayerRoster(raw_player[0])

            player = fetchPlayerRanknev(player)

            player['chars'].sort()
            player['ships'].sort()
            player['miss'].sort()
            player['missShips'].sort()

            s: str = '\n'.join(map(str, player['chars']))
            s2: str = '\n'.join(map(str, player['ships']))
            s3: str = '\n'.join(map(str, player['miss']))
            s4: str = '\n'.join(map(str, player['missShips']))

            if s == "" and s2 == "":
                await ctx.send("**Nincsen beszámolható egységed, vagy hajód!**")
            else:
                await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " jelenlegi rang pontszáma: " + str('{:,}'.format(player['rank'])) + ".  A rangja pedig: " + str(player['ranknev']))

                message1 = ""
                message2 = ""
                message3 = ""
                message4 = ""

                if show == "b" or show == "m":
                    message1 += "\n**Meglévő karakterek:** \n" + str("```ini\n" + s + "```")
                    message2 += "\n**Meglévő hajók:** \n" + str("```ini\n" + s2 + "```")

                if show == "b" or show == "h":
                    message3 += "\n**Hiányzó karakterek:** \n" + str("```ini\n" + s3 + "```")
                    message4 += "\n**Hiányzó hajók:** \n" + str("```ini\n" + s4 + "```")

                if message1 != "":
                    await ctx.send(message1)
                if message2 != "":
                    await ctx.send(message2)
                if message3 != "":
                    await ctx.send(message3)
                if message4 != "":
                    await ctx.send(message4)

            toc()

        else:
            pass

    @rang.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


def fetchPlayerRanknev(player):

    if 0 <= player['rank'] <= 10:
        player['ranknev'] = "Párafarmer"
    if 10 < player['rank'] <= 20:
        player['ranknev'] = "Droid"
    if 20 < player['rank'] <= 30:
        player['ranknev'] = "Scavenger / Roncsvadász"
    if 30 < player['rank'] <= 40:
        player['ranknev'] = "Pirate / Kalóz"
    if 40 < player['rank'] <= 50:
        player['ranknev'] = "Smuggler / Csempész"
    if 50 < player['rank'] <= 60:
        player['ranknev'] = "Bounty Hunter / Fejvadász"
    if 60 < player['rank'] <= 70:
        player['ranknev'] = "Rebel / Stormtrooper"
    if 70 < player['rank'] <= 80:
        player['ranknev'] = "X-Wing Pilot / Tie-Fighter Pilot"
    if 80 < player['rank'] <= 90:
        player['ranknev'] = "Rebel Officer / Imperial Officer"
    if 90 < player['rank'] <= 100:
        player['ranknev'] = "Senator / Moff"
    if 100 < player['rank'] <= 110:
        player['ranknev'] = "Padavan / Apprentice"
    if 110 < player['rank'] <= 120:
        player['ranknev'] = "Jedi / Sith"
    if 120 < player['rank'] <= 130:
        player['ranknev'] = "Jedi Master / Sith Master"
    if 130 < player['rank'] <= 140:
        player['ranknev'] = "Grandmaster / Sith Lord"
    if 140 < player['rank'] <= 150:
        player['ranknev'] = "Mandalorian"
    if player['rank'] > 150:
        player['ranknev'] = "Petőfi"

    return player


def fChar(player, raw_player, defID, realName, gear, zeta, pont):
    retval = 0
    missingZeta = 0
    missingChar = 1
    i=0
    printName = realName
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

            if a['gear'] >= gear or (a['gear'] >= gear-1 and pont > 1):
                if missingZeta == 0:
                    player['chars'].insert(player['rank'], printName)
                    if a['gear'] >= gear:
                        player['rank'] += pont
                    else:
                        player['rank'] += 1
                        player['miss'].insert(player['rank'], printName + ' (1P) G:' + str(a['gear']) + '/' + str(gear) + '')
                    retval = 1
                else:
                    player['miss'].insert(player['rank'], printName + ' Z:' + str(temp) + '/' + str(zeta) + '')
            else:
                if missingZeta == 0:
                   player['miss'].insert(player['rank'], printName + ' G:' + str(a['gear']) + '/' + str(gear) + '')
                else:
                   player['miss'].insert(player['rank'], printName + ' G:' + str(a['gear']) + '/' + str(gear) + ' Z:' + str(temp) + '/' + str(zeta) + '')
        i += 1
    if missingChar == 1:
        player['miss'].insert(player['rank'], printName + ' L')
    return retval


def fShip(player, raw_player, defID, realName, skills, pilot1, pilot2, pilot3, pont):
    missingChar = 1
    printName = realName
    if pont > 1:
        printName += ' ' + str(pont)
    i=0
    for a in raw_player['roster']:
        a = raw_player['roster'][i]
        if a['defId'] == defID:
            missingChar = 0
            if a['rarity'] == 7 and a['level'] == 85:

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
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= skills:
                        player['ships'].insert(player['rank'], printName)
                        player['rank'] += pont
                    else:
                        player['missShips'].insert(player['rank'], printName + 'S:' + str(temp) + '/' + str(skills) + '')
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
                    player['missShips'].insert(player['rank'], printName + ' P:'+str(sumpilots) + '/' + str(needpilots) + '')
            else:
                player['missShips'].insert(player['rank'], printName + ' R:' + str(a['rarity']) + '/7' + '')
        i += 1
    if missingChar == 1:
        player['missShips'].insert(player['rank'], printName + ' L')
    return


def fetchPlayerRoster(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "ranknev": " ",
        "chars": [],
        "ships": [],
        "miss": [],
        "missShips": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "GEONOSIANBROODALPHA", "Geonosian Brood Alpha", 13, 2, 2)
    fChar(player, raw_player, "GEONOSIANSOLDIER", "Geonosian Soldier", 12, 0, 1)
    fChar(player, raw_player, "GEONOSIANSPY", "Geonosian Spy", 12, 0, 1)
    fChar(player, raw_player, "SUNFAC", "Sun Fac", 12, 0, 1)
    fChar(player, raw_player, "POGGLETHELESSER", "Poggle the Lesser", 12, 0, 1)
    fChar(player, raw_player, "GRIEVOUS", "General Grievous", 13, 2, 1)
    fChar(player, raw_player, "B1BATTLEDROIDV2", "B1 Battle Droid", 13, 1, 1)
    fChar(player, raw_player, "B2SUPERBATTLEDROID", "B2 Super Battle Droid", 13, 1, 1)
    fChar(player, raw_player, "MAGNAGUARD", "IG-100 MagnaGuard", 13, 0, 1)
    fChar(player, raw_player, "DROIDEKA", "Droideka", 12, 0, 1)
    fChar(player, raw_player, "DARTHTRAYA", "Darth Traya", 12, 2, 1)
    fChar(player, raw_player, "DARTHSION", "Darth Sion", 13, 1, 1)
    fChar(player, raw_player, "DARTHNIHILUS", "Darth Nihilus", 12, 1, 1)
    fChar(player, raw_player, "GRANDADMIRALTHRAWN", "Grand Admiral Thrawn", 13, 1, 2)
    fChar(player, raw_player, "COUNTDOOKU", "Count Dooku", 12, 1, 1)
    fChar(player, raw_player, "DARTHREVAN", "Darth Revan", 13, 3, 4)
    fChar(player, raw_player, "BASTILASHANDARK", "Bastila Shan (Fallen)", 13, 1, 1)
    fChar(player, raw_player, "SITHTROOPER", "Sith Trooper", 12, 0, 1)
    fChar(player, raw_player, "SITHMARAUDER", "Sith Marauder", 12, 0, 1)
    fChar(player, raw_player, "EMPERORPALPATINE", "Emperor Palpatine", 12, 2, 1)
    fChar(player, raw_player, "DARTHMALAK", "Darth Malak", 13, 2, 4)
    fChar(player, raw_player, "NUTEGUNRAY", "Nute Gunray", 12, 1, 1)
    fChar(player, raw_player, "MOTHERTALZIN", "Mother Talzin", 12, 2, 1)
    fChar(player, raw_player, "ASAJVENTRESS", "Asajj Ventress", 13, 1, 1)
    fChar(player, raw_player, "NIGHTSISTERZOMBIE", "Nightsister Zombie", 12, 0, 1)
    fChar(player, raw_player, "DAKA", "Old Daka", 13, 0, 1)
    fChar(player, raw_player, "WATTAMBOR", "Wat Tambor", 13, 1, 2)
    fChar(player, raw_player, "NIGHTSISTERSPIRIT", "Nightsister Spirit", 12, 0, 1)
    fChar(player, raw_player, "PADMEAMIDALA", "Padme Amidala", 13, 2, 3)
    fChar(player, raw_player, "GENERALSKYWALKER", "General Skywalker", 13, 4, 4)
    fChar(player, raw_player, "GENERALKENOBI", "General Kenobi", 13, 1, 2)
    fChar(player, raw_player, "AHSOKATANO", "Ahsoka Tano", 13, 1, 2)
    fChar(player, raw_player, "ANAKINKNIGHT", "Anakin Skywalker", 13, 1, 1)
    fChar(player, raw_player, "C3POLEGENDARY", "C3PO", 13, 1, 2)
    fChar(player, raw_player, "JEDIKNIGHTREVAN", "Jedi Knight Revan", 13, 3, 3)
    fChar(player, raw_player, "BASTILASHAN", "Bastila Shan", 13, 1, 1)
    fChar(player, raw_player, "JOLEEBINDO", "Jolee Bindo", 13, 1, 1)
    fChar(player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 13, 1, 1)
    fChar(player, raw_player, "HERMITYODA", "Hermit Yoda", 13, 1, 1)
    fChar(player, raw_player, "SHAAKTI", "Shaak Ti", 13, 2, 2)
    fChar(player, raw_player, "CT5555", "Fives", 13, 2, 1)
    fChar(player, raw_player, "CC2224", "Cody", 13, 0, 1)
    fChar(player, raw_player, "CT7567", "Rex", 13, 1, 1)
    fChar(player, raw_player, "CT210408", "Echo", 13, 1, 1)
    fChar(player, raw_player, "ARCTROOPER501ST", "ARC Trooper", 13, 1, 1)
    fChar(player, raw_player, "CLONESERGEANTPHASEI", "Clone Sergant", 13, 0, 1)
    fChar(player, raw_player, "KIADIMUNDI", "Ki-Adi-Mundi", 13, 1, 1)
    fChar(player, raw_player, "R2D2_LEGENDARY", "R2D2", 13, 2, 2)
    fChar(player, raw_player, "REYJEDITRAINING", "Rey (Jedi Training)", 13, 2, 1)
    fChar(player, raw_player, "BB8", "BB-8", 13, 2, 1)
    fChar(player, raw_player, "FINN", "Finn", 13, 0, 1)
    fChar(player, raw_player, "COMMANDERLUKESKYWALKER", "Commander Luke Skywalker", 13, 3, 3)
    fChar(player, raw_player, "HANSOLO", "Han Solo", 13, 1, 1)
    fChar(player, raw_player, "CHEWBACCALEGENDARY", "Chewbacca", 13, 2, 2)
    fChar(player, raw_player, "AMILYNHOLDO", "Amilyn Holdo", 13, 0, 1)
    fChar(player, raw_player, "HOTHHAN", "Captain Han Solo", 13, 0, 1)
    fChar(player, raw_player, "PHASMA", "Captain Phasma", 13, 0, 1)
    fChar(player, raw_player, "VADER", "Darth Vader", 13, 3, 3)
    fChar(player, raw_player, "FIRSTORDEREXECUTIONER", "First Order Executioner", 13, 0, 1)
    fChar(player, raw_player, "FIRSTORDEROFFICERMALE", "First Order Officer", 13, 0, 1)
    fChar(player, raw_player, "FIRSTORDERSPECIALFORCESPILOT", "First Order SF TIE Pilot", 13, 0, 1)
    fChar(player, raw_player, "FIRSTORDERTROOPER", "First Order Stromtrooper", 13, 0, 1)
    fChar(player, raw_player, "FIRSTORDERTIEPILOT", "First Order TIE Pilot", 13, 0, 1)
    fChar(player, raw_player, "GENERALHUX", "General Hux", 13, 1, 1)
    fChar(player, raw_player, "KYLOREN", "Kylo Ren", 13, 1, 0)
    fChar(player, raw_player, "KYLORENUNMASKED", "Kylo Ren (Unmasked)", 13, 2, 1)
    fChar(player, raw_player, "ADMINISTRATORLANDO", "Lando Calrissian", 13, 0, 1)
    fChar(player, raw_player, "POE", "Poe Dameron", 13, 0, 1)
    fChar(player, raw_player, "HOTHLEIA", "Rebel Officer Leia Organa", 13, 0, 1)
    fChar(player, raw_player, "EPIXFINN", "Resistance Hero Finn", 13, 0, 1)
    fChar(player, raw_player, "EPIXPOE", "Resistance Hero Poe", 13, 0, 1)
    fChar(player, raw_player, "RESISTANCEPILOT", "Resistance Pilot", 13, 0, 1)
    fChar(player, raw_player, "RESISTANCETROOPER", "Resistance Trooper", 13, 0, 1)
    fChar(player, raw_player, "REY", "Rey (Scavenger)", 13, 0, 1)
    fChar(player, raw_player, "ROSETICO", "Rose Tico", 13, 0, 1)
    fChar(player, raw_player, "FOSITHTROOPER", "Sith Trooper", 13, 0, 1)
    fChar(player, raw_player, "SUPREMELEADERKYLOREN", "Supreme Leader Kylo Ren", 13, 6, 5)
    fChar(player, raw_player, "SMUGGLERCHEWBACCA", "Veteran Smuggler Chewbacca", 13, 0, 1)
    fChar(player, raw_player, "SMUGGLERHAN", "Veteran Smuggler Han Solo", 13, 0, 1)
    fChar(player, raw_player, "WAMPA", "Wampa", 13, 1, 1)
    fChar(player, raw_player, "GLREY", "Rey", 13, 6, 5)
    fChar(player, raw_player, "JEDIKNIGHTLUKE", "Jedi Knight Luke Skywalker", 13, 2, 4)

    fShip(player, raw_player, "CAPITALCHIMAERA", "Chimaera", 5, "GRANDADMIRALTHRAWN", "", "", 1)
    fShip(player, raw_player, "CAPITALSTARDESTROYER", "Executrix", 5, "GRANDMOFFTARKIN", "", "", 1)
    fShip(player, raw_player, "CAPITALNEGOTIATOR", "Negotiator", 5, "GENERALKENOBI", "", "", 2)
    fShip(player, raw_player, "GEONOSIANSTARFIGHTER2", "Geonosian Soldier's Starfighter", 3, "GEONOSIANSOLDIER", "", "", 1)
    fShip(player, raw_player, "GEONOSIANSTARFIGHTER3", "Geonosian Spy's Starfighter", 3, "GEONOSIANSPY", "", "", 1)
    fShip(player, raw_player, "HOUNDSTOOTH", "Hound's Tooth", 3, "BOSSK", "", "", 2)
    fShip(player, raw_player, "GEONOSIANSTARFIGHTER1", "Sun Fac's Geonosian Starfighter", 3, "SUNFAC", "", "", 1)
    fShip(player, raw_player, "MILLENNIUMFALCON", "Han's Millennium Falcon", 4, "HANSOLO", "CHEWBACCALEGENDARY", "", 2)
    fShip(player, raw_player, "CAPITALMALEVOLENCE", "Malevolance", 5, "GRIEVOUS", "", "", 2)
    fShip(player, raw_player, "VULTUREDROID", "Vulture Droid", 3, "", "", "", 1)
    fShip(player, raw_player, "HYENABOMBER", "Hyena Bomber", 3, "", "", "", 1)
    fShip(player, raw_player, "CAPITALMONCALAMARICRUISER", "Home One", 5, "ADMIRALACKBAR", "", "", 1)
    fShip(player, raw_player, "CAPITALJEDICRUISER", "Endurance", 5, "MACEWINDU", "", "", 1)
    fShip(player, raw_player, "PHANTOM2", "Phantom II", 5, "SABINEWRENS3", "EZRABRIDGERS3", "CHOPPERS3", 1)
    fShip(player, raw_player, "GHOST", "Ghost", 5, "HERASYNDULLAS3", "KANANJARRUSS3", "ZEBS3", 1)
    fShip(player, raw_player, "JEDISTARFIGHTERANAKIN", "Anakin's Eta-2 Starfighter", 3, "ANAKINKNIGHT", "", "", 1)
    fShip(player, raw_player, "JEDISTARFIGHTERAHSOKATANO", "Ahsoka Tano’s Jedi Starfighter", 3, "AHSOKATANO", "", "", 1)
    fShip(player, raw_player, "BLADEOFDORIN", "Plo Koon’s Jedi Starfighter", 3, "PLOKOON", "", "", 1)
    fShip(player, raw_player, "UMBARANSTARFIGHTER", "Umbaran Starfighter", 3, "CT5555", "", "", 1)
    fShip(player, raw_player, "ARC170CLONESERGEANT", "Clone Sergant’s ARC-170", 3, "CLONESERGEANTPHASEI", "", "", 1)
    fShip(player, raw_player, "YWINGCLONEWARS", "BTL-B Y-wing Starfighter", 3, "", "", "", 1)
    fShip(player, raw_player, "ARC170REX", "Rex’s ARC-170", 3, "CT7567", "", "", 1)
    fShip(player, raw_player, "CAPITALRADDUS", "Raddus", 5, "AMILYNHOLDO", "", "", 1)
    fShip(player, raw_player, "CAPITALFINALIZER", "Finalizer", 5, "GENERALHUX", "", "", 1)


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
    bot.add_cog(RANK(bot))