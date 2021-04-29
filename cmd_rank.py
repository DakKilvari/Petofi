from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
import time
from discord.ext import commands
import global_settings


class Rang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Aktuális rang pontszám kiszámítása'])
    @commands.has_any_role(global_settings.Role3, global_settings.Role5, global_settings.Role6)  # User need this role to run command (can have multiple)
    async def rang(self, ctx, raw_allycode, show="b"):
        """Aktuális rang pontszám kiszámítása
        Aktuális rang pontszám kiszámítása adott játékosra
        raw_allycode: me / taggelés / allykód
        show: m (meglévő) / h (hiányzó) / üresen hagyva (csak pontszám és rang)"""

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

                if show == "m":
                    message1 += "\n**Meglévő karakterek:** \n" + str("```ini\n" + s + "```")
                    message2 += "\n**Meglévő hajók:** \n" + str("```ini\n" + s2 + "```")

                if show == "h":
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

    if 0 <= player['rank'] <= 39: player['ranknev'] = "Gungan"
    if 40 <= player['rank'] <= 79: player['ranknev'] = "Ewok"
    if 80 <= player['rank'] <= 99: player['ranknev'] = "Cadet (Kadét)"
    if 100 <= player['rank'] <= 119: player['ranknev'] = "Trooper (Katona)"
    if 120 <= player['rank'] <= 134: player['ranknev'] = "Sergeant (Őrmester)"
    if 135 <= player['rank'] <= 149: player['ranknev'] = "Commander (Parancsnok)"
    if 150 <= player['rank'] <= 159: player['ranknev'] = "Scoundrel / Operative"
    if 160 <= player['rank'] <= 169: player['ranknev'] = "Commando / Power Tech"
    if 170 <= player['rank'] <= 179: player['ranknev'] = "Gunslinger / Sniper"
    if 180 <= player['rank'] <= 189: player['ranknev'] = "Vanguard / Mercenary"
    if 190 <= player['rank'] <= 199: player['ranknev'] = "Lieutenant (Hadnagy)"
    if 200 <= player['rank'] <= 209: player['ranknev'] = "Captain (Százados)"
    if 210 <= player['rank'] <= 219: player['ranknev'] = "Major (Őrnagy)"
    if 220 <= player['rank'] <= 229: player['ranknev'] = "Colonel (Ezredes)"
    if 230 <= player['rank'] <= 239: player['ranknev'] = "Jedi / Sith Apprentice (Jedi tanonc)"
    if 240 <= player['rank'] <= 249: player['ranknev'] = "Jedi / Sith Acolyte (Oltárszolga)"
    if 250 <= player['rank'] <= 259: player['ranknev'] = "Jedi / Sith Padawan (Padavan)"
    if 260 <= player['rank'] <= 269: player['ranknev'] = "Jedi Knight / Sith Warrior (Lovag / Harcos)"
    if 270 <= player['rank'] <= 279: player['ranknev'] = "Jedi Sage / Sith Sorcerer (Varázsló)"
    if 280 <= player['rank'] <= 289: player['ranknev'] = "Jedi Shadow / Sith Assassin (Orgyilkos)"
    if 290 <= player['rank'] <= 299: player['ranknev'] = "Jedi Guard / Sith Juggernaut (Őr)"
    if 300 <= player['rank'] <= 309: player['ranknev'] = "Jedi Sentinel / Sith Marauder (Őrszem / Martalóc)"
    if 310 <= player['rank'] <= 319: player['ranknev'] = "Jedi Consular / Sith Inquisitor (Vizsgálóbíró)"
    if 320 <= player['rank'] <= 329: player['ranknev'] = "General (Tábornok)"
    if 330 <= player['rank'] <= 339: player['ranknev'] = "Muff (Moff)"
    if 340 <= player['rank'] <= 349: player['ranknev'] = "Admiral (Admirális)"
    if 350 <= player['rank'] <= 359: player['ranknev'] = "Jedi / Sith Master"
    if 360 <= player['rank'] <= 369: player['ranknev'] = "Jedi Grand Master / Sith Lord"
    if 370 <= player['rank'] <= 379: player['ranknev'] = "Supreme Commander / Leader"
    if 380 <= player['rank']: player['ranknev'] = "Supreme Chancellor (Mongi)"

    return player

def fChar(player, raw_player, defID, realName, pont):
    retval = 0
    missingChar = 1
    i=0
    printName = realName
    if pont > 1:
        printName += ' ' + str(pont)

    for a in raw_player['roster']:
        a = raw_player['roster'][i]
        if a['defId'] == defID:
            missingChar = 0

            if a['gear'] >= 13:
                player['rank'] += pont
                if a['relic']['currentTier']-2 >= 5:
                    printName = realName + ' ' + str(pont+1)
                    player['rank'] += 1
                if a['relic']['currentTier']-2 >= 8:
                    printName = realName + ' ' + str(pont+2)
                    player['rank'] += 1
                player['chars'].insert(player['rank'], printName)
                retval = 1
            else:
                player['miss'].insert(player['rank'], printName + ' G:' + str(a['gear']) + '/13')
        i += 1
    if missingChar == 1:
        player['miss'].insert(player['rank'], printName + ' L')
    return retval

def fShip(player, raw_player, defID, realName, skills, pilot1, pilot2, pilot3, gear, pont):
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
                    if b['defId'] == pilot1 and b['gear'] >= gear or pilot1 == "":
                        p1 = 1
                    if b['defId'] == pilot2 and b['gear'] >= gear or pilot2 == "":
                        p2 = 1
                    if b['defId'] == pilot3 and b['gear'] >= gear or pilot3 == "":
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
                        player['missShips'].insert(player['rank'], printName + ' S:' + str(temp) + '/' + str(skills) + '')
                else:
                    needpilots = 0
                    if pilot1 != "":
                        needpilots += 1
                    if pilot2 != "":
                        needpilots += 1
                    if pilot3 != "":
                        needpilots += 1

                    sumpilots = 0
                    if p1 == 1 and pilot1 != "":
                        sumpilots += 1
                    if p2 == 1  and pilot2 != "":
                        sumpilots += 1
                    if p3 == 1  and pilot3 != "":
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

    fChar(player, raw_player, "GRANDMASTERLUKE", "Jedi Master Luke Skywalker", 5)
    fChar(player, raw_player, "GLREY", "Rey", 5)
    fChar(player, raw_player, "SITHPALPATINE", "Sith Eternal Emperor", 5)
    fChar(player, raw_player, "SUPREMELEADERKYLOREN", "Supreme Leader Kylo Ren", 5)
    fChar(player, raw_player, "DARTHMALAK", "Darth Malak", 4)
    fChar(player, raw_player, "DARTHREVAN", "Darth Revan", 4)
    fChar(player, raw_player, "GENERALSKYWALKER", "General Skywalker", 4)
    fChar(player, raw_player, "JEDIKNIGHTLUKE", "Jedi Knight Luke Skywalker", 4)
    fChar(player, raw_player, "ARCTROOPER501ST", "ARC Trooper", 3)
    fChar(player, raw_player, "COMMANDERLUKESKYWALKER", "Commander Luke Skywalker", 3)
    fChar(player, raw_player, "VADER", "Darth Vader", 3)
    fChar(player, raw_player, "CT210408", "CT-21-0408 Echo", 3)
    fChar(player, raw_player, "CT5555", "CT-5555 Fives", 3)
    fChar(player, raw_player, "JEDIKNIGHTREVAN", "Jedi Knight Revan", 3)
    fChar(player, raw_player, "PADMEAMIDALA", "Padmé Amidala", 3)
    fChar(player, raw_player, "CT7567", "CT-7567 Rex", 3)
    fChar(player, raw_player, "SHAAKTI", "Shaak Ti", 3)
    fChar(player, raw_player, "AHSOKATANO", "Ahsoka Tano", 2)
    fChar(player, raw_player, "C3POLEGENDARY", "C-3PO", 2)
    fChar(player, raw_player, "CHEWBACCALEGENDARY", "Chewbacca", 2)
    fChar(player, raw_player, "EMPERORPALPATINE", "Emperor Palpatine", 2)
    fChar(player, raw_player, "GENERALKENOBI", "General Kenobi", 2)
    fChar(player, raw_player, "GEONOSIANBROODALPHA", "Geonosian Brood Alpha", 2)
    fChar(player, raw_player, "GRANDADMIRALTHRAWN", "Grand Admiral Thrawn", 2)
    fChar(player, raw_player, "KIADIMUNDI", "Ki-Adi-Mundi", 2)
    fChar(player, raw_player, "R2D2_LEGENDARY", "R2-D2", 2)
    fChar(player, raw_player, "C3POCHEWBACCA", "Threepio & Chewie", 2)
    fChar(player, raw_player, "WATTAMBOR", "Wat Tambor", 2)
    fChar(player, raw_player, "ADMIRALPIETT", "Admiral Piett", 1)
    fChar(player, raw_player, "AMILYNHOLDO", "Amilyn Holdo", 1)
    fChar(player, raw_player, "ASAJVENTRESS", "Asajj Ventress", 1)
    fChar(player, raw_player, "B1BATTLEDROIDV2", "B1 Battle Droid", 1)
    fChar(player, raw_player, "B2SUPERBATTLEDROID", "B2 Super Battle Droid", 1)
    fChar(player, raw_player, "BASTILASHAN", "Bastila Shan", 1)
    fChar(player, raw_player, "BASTILASHANDARK", "Bastila Shan (Fallen)", 1)
    fChar(player, raw_player, "BB8", "BB-8", 1)
    fChar(player, raw_player, "BIGGSDARKLIGHTER", "Biggs Darklighter", 1)
    fChar(player, raw_player, "HOTHHAN", "Captain Han Solo", 1)
    fChar(player, raw_player, "PHASMA", "Captain Phasma", 1)
    fChar(player, raw_player, "CLONESERGEANTPHASEI", "Clone Sergeant - Phase I", 1)
    fChar(player, raw_player, "CC2224", "CC-2224 Cody", 1)
    fChar(player, raw_player, "COLONELSTARCK", "Colonel Starck", 1)
    fChar(player, raw_player, "COUNTDOOKU", "Count Dooku", 1)
    fChar(player, raw_player, "DARKTROOPER", "Dark Trooper", 1)
    fChar(player, raw_player, "MAUL", "Darth Maul", 1)
    fChar(player, raw_player, "DARTHNIHILUS", "Darth Nihilus", 1)
    fChar(player, raw_player, "DARTHSIDIOUS", "Darth Sidious", 1)
    fChar(player, raw_player, "DARTHSION", "Darth Sion", 1)
    fChar(player, raw_player, "DARTHTRAYA", "Darth Traya", 1)
    fChar(player, raw_player, "DIRECTORKRENNIC", "Director Krennic", 1)
    fChar(player, raw_player, "DROIDEKA", "Droideka", 1)
    fChar(player, raw_player, "FINN", "Finn", 1)
    fChar(player, raw_player, "FIRSTORDEREXECUTIONER", "First Order Executioner", 1)
    fChar(player, raw_player, "FIRSTORDEROFFICERMALE", "First Order Officer", 1)
    fChar(player, raw_player, "FIRSTORDERSPECIALFORCESPILOT", "First Order SF TIE Pilot", 1)
    fChar(player, raw_player, "FIRSTORDERTROOPER", "First Order Stormtrooper", 1)
    fChar(player, raw_player, "FIRSTORDERTIEPILOT", "First Order TIE Pilot", 1)
    fChar(player, raw_player, "GRIEVOUS", "General Grievous", 1)
    fChar(player, raw_player, "GENERALHUX", "General Hux", 1)
    fChar(player, raw_player, "VEERS", "General Veers", 1)
    fChar(player, raw_player, "GEONOSIANSOLDIER", "Geonosian Soldier", 1)
    fChar(player, raw_player, "GEONOSIANSPY", "Geonosian Spy", 1)
    fChar(player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 1)
    fChar(player, raw_player, "GRANDMOFFTARKIN", "Grand Moff Tarkin", 1)
    fChar(player, raw_player, "HANSOLO", "Han Solo", 1)
    fChar(player, raw_player, "HERMITYODA", "Hermit Yoda", 1)
    fChar(player, raw_player, "MAGNAGUARD", "IG-100 MagnaGuard", 1)
    fChar(player, raw_player, "ANAKINKNIGHT", "Jedi Knight Anakin", 1)
    fChar(player, raw_player, "JOLEEBINDO", "Jolee Bindo", 1)
    fChar(player, raw_player, "KYLOREN", "Kylo Ren", 1)
    fChar(player, raw_player, "KYLORENUNMASKED", "Kylo Ren (Unmasked)", 1)
    fChar(player, raw_player, "ADMINISTRATORLANDO", "Lando Calrissian", 1)
    fChar(player, raw_player, "MOFFGIDEONS1", "Moff Gideon", 1)
    fChar(player, raw_player, "MONMOTHMA", "Mon Mothma", 1)
    fChar(player, raw_player, "MOTHERTALZIN", "Mother Talzin", 1)
    fChar(player, raw_player, "NIGHTSISTERSPIRIT", "Nightsister Spirit", 1)
    fChar(player, raw_player, "NIGHTSISTERZOMBIE", "Nightsister Zombie", 1)
    fChar(player, raw_player, "NUTEGUNRAY", "Nute Gunray", 1)
    fChar(player, raw_player, "OLDBENKENOBI", "Obi-Wan Kenobi (Old Ben)", 1)
    fChar(player, raw_player, "DAKA", "Old Daka", 1)
    fChar(player, raw_player, "POE", "Poe Dameron", 1)
    fChar(player, raw_player, "POGGLETHELESSER", "Poggle the Lesser", 1)
    fChar(player, raw_player, "PRINCESSLEIA", "Princess Leia", 1)
    fChar(player, raw_player, "HOTHLEIA", "Rebel Officer Leia Organa", 1)
    fChar(player, raw_player, "EPIXFINN", "Resistance Hero Finn", 1)
    fChar(player, raw_player, "EPIXPOE", "Resistance Hero Poe", 1)
    fChar(player, raw_player, "RESISTANCEPILOT", "Resistance Pilot", 1)
    fChar(player, raw_player, "RESISTANCETROOPER", "Resistance Trooper", 1)
    fChar(player, raw_player, "REYJEDITRAINING", "Rey (Jedi Training)", 1)
    fChar(player, raw_player, "REY", "Rey (Scavenger)", 1)
    fChar(player, raw_player, "ROSETICO", "Rose Tico", 1)
    fChar(player, raw_player, "ROYALGUARD", "Royal Guard", 1)
    fChar(player, raw_player, "SITHTROOPER", "Sith Empire Trooper", 1)
    fChar(player, raw_player, "SITHMARAUDER", "Sith Marauder", 1)
    fChar(player, raw_player, "FOSITHTROOPER", "Sith Trooper", 1)
    fChar(player, raw_player, "SUNFAC", "Sun Fac", 1)
    fChar(player, raw_player, "ARMORER", "The Armorer", 1)
    fChar(player, raw_player, "SMUGGLERCHEWBACCA", "Veteran Smuggler Chewbacca", 1)
    fChar(player, raw_player, "SMUGGLERHAN", "Veteran Smuggler Han Solo", 1)
    fChar(player, raw_player, "WAMPA", "Wampa", 1)
    fChar(player, raw_player, "WEDGEANTILLES", "Wedge Antilles", 1)
    fChar(player, raw_player, "RANGETROOPER", "Range Trooper", 1)
    fChar(player, raw_player, "MACEWINDU", "Mace Windu", 1)
    fChar(player, raw_player, "AAYLASECURA", "Aayla Secura", 1)
    fChar(player, raw_player, "BOKATAN", "Bo-Katan Kryze", 1)

    fShip(player, raw_player, "CAPITALCHIMAERA", "Chimaera", 5, "GRANDADMIRALTHRAWN", "", "", 12, 2)
    fShip(player, raw_player, "CAPITALNEGOTIATOR", "Negotiator", 5, "GENERALKENOBI", "", "", 13, 3)
    fShip(player, raw_player, "GEONOSIANSTARFIGHTER2", "Geonosian Soldier's Starfighter", 3, "GEONOSIANSOLDIER", "", "", 12, 1)
    fShip(player, raw_player, "GEONOSIANSTARFIGHTER3", "Geonosian Spy's Starfighter", 3, "GEONOSIANSPY", "", "", 12, 1)
    fShip(player, raw_player, "HOUNDSTOOTH", "Hound's Tooth", 3, "BOSSK", "", "", 12, 2)
    fShip(player, raw_player, "GEONOSIANSTARFIGHTER1", "Sun Fac's Geonosian Starfighter", 3, "SUNFAC", "", "", 12, 1)
    fShip(player, raw_player, "MILLENNIUMFALCON", "Han's Millennium Falcon", 4, "HANSOLO", "CHEWBACCALEGENDARY", "", 13, 2)
    fShip(player, raw_player, "CAPITALMALEVOLENCE", "Malevolance", 5, "GRIEVOUS", "", "", 13, 3)
    fShip(player, raw_player, "VULTUREDROID", "Vulture Droid", 3, "", "", "", 0, 2)
    fShip(player, raw_player, "HYENABOMBER", "Hyena Bomber", 3, "", "", "", 0, 2)
    fShip(player, raw_player, "CAPITALMONCALAMARICRUISER", "Home One", 5, "ADMIRALACKBAR", "", "", 12, 1)
    fShip(player, raw_player, "PHANTOM2", "Phantom II", 5, "SABINEWRENS3", "EZRABRIDGERS3", "CHOPPERS3", 11, 1)
    fShip(player, raw_player, "GHOST", "Ghost", 5, "HERASYNDULLAS3", "KANANJARRUSS3", "ZEBS3", 11, 1)
    fShip(player, raw_player, "JEDISTARFIGHTERANAKIN", "Anakin's Eta-2 Starfighter", 3, "ANAKINKNIGHT", "", "", 13, 2)
    fShip(player, raw_player, "JEDISTARFIGHTERAHSOKATANO", "Ahsoka Tano’s Jedi Starfighter", 3, "AHSOKATANO", "", "", 13, 2)
    fShip(player, raw_player, "BLADEOFDORIN", "Plo Koon’s Jedi Starfighter", 3, "PLOKOON", "", "", 12, 1)
    fShip(player, raw_player, "UMBARANSTARFIGHTER", "Umbaran Starfighter", 3, "CT5555", "", "", 13, 2)
    fShip(player, raw_player, "ARC170CLONESERGEANT", "Clone Sergant’s ARC-170", 3, "CLONESERGEANTPHASEI", "", "", 12, 1)
    fShip(player, raw_player, "YWINGCLONEWARS", "BTL-B Y-wing Starfighter", 3, "", "", "", 0, 2)
    fShip(player, raw_player, "ARC170REX", "Rex’s ARC-170", 3, "CT7567", "", "", 13, 2)
    fShip(player, raw_player, "TIEBOMBERIMPERIAL", "Imperial TIE Bomber", 3, "", "", "", 0, 2)
    fShip(player, raw_player, "YWINGREBEL", "Rebel Y-wing", 3, "", "", "", 0, 2)
    fShip(player, raw_player, "CAPITALFINALIZER", "Finalizer", 5, "GENERALHUX", "", "", 12, 1)
    fShip(player, raw_player, "CAPITALRADDUS", "Raddus", 5, "AMILYNHOLDO", "", "", 12, 1)
    fShip(player, raw_player, "TIESILENCER", "TIE Silencer", 3, "KYLORENUNMASKED", "", "", 13, 1)
    fShip(player, raw_player, "XWINGRED3", "Biggs Darklighter's X-wing", 3, "BIGGSDARKLIGHTER", "", "", 12, 1)    
    fShip(player, raw_player, "EMPERORSSHUTTLE", "Emperor's Shuttle", 4, "EMPERORPALPATINE", "ROYALGUARD", "", 12, 1)
    fShip(player, raw_player, "TIEFIGHTERFOSF", "First Order SF TIE Fighter", 3, "FIRSTORDERSPECIALFORCESPILOT", "", "", 12, 1)
    fShip(player, raw_player, "TIEFIGHTERFIRSTORDER", "First Order TIE Fighter", 3, "FIRSTORDERTIEPILOT", "", "", 12, 1)
    fShip(player, raw_player, "COMMANDSHUTTLE", "Kylo Ren's Command Shuttle", 5, "KYLOREN", "PHASMA", "FIRSTORDERTROOPER", 12, 1)

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
    bot.add_cog(Rang(bot))
