from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import time
from discord.ext import commands
from db_handler import db_handler
import global_settings
import discord


class Raidcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Raidcheck'])
    @commands.has_any_role(global_settings.Role3)  # User need this role to run command (can have multiple)
    async def raid(self, ctx, raw_allycode):
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

            player = fetchPlayerP101(raw_player[0])

            embed = discord.Embed(title=player['jatekosnev'] + ' Heroic Rancor csapat áttekintő (hányzó karakterek)', url="https://swgoh.gg/p/", color=0x7289da)

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P1: Rey, Rex, Fives, C-3PO, Hoda (15%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P1: Rey, Rex, Fives, C-3PO, Hoda (15%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP102(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P1: SLKR, Zombie, Daka, Hux, Thrawn (12%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P1: SLKR, Zombie, Daka, Hux, Thrawn (12%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP103(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P1: Padmé, Ahsoka, Jedi Anakin, GK, GMY (3%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P1: Padmé, Ahsoka, Jedi Anakin, GK, GMY (3%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP104(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P1: SEE, Traya, Sion, Sith Empire Trooper, Sidious (3%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P1: SEE, Traya, Sion, Sith Empire Trooper, Sidious (3%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP201(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P2: SLKR, Hux, Thrawn, KRU, Sith Trooper (12%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P2: SLKR, Hux, Thrawn, KRU, Sith Trooper (12%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP202(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P2: Vader, Wat, Malak, Palpatine, Thrawn (10%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P2: Vader, Wat, Malak, Palpatine, Thrawn (10%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP203(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P2: Shaak Ti, Rex, ARC Trooper, Echo, Fives (4%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P2: Shaak Ti, Rex, ARC Trooper, Echo, Fives (4%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP204(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P2: JKR, JKL, JML, GAS, GMY (8%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P2: JKR, JKL, JML, GAS, GMY (8%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP205(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P2: JKR, JKL, GAS, GMY, Hoda (5%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P2: JKR, JKL, GAS, GMY, Hoda (5%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP401(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P4: CLS, Han, Chewbacca, C-3PO, 3Pac (1.5%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P4: CLS, Han, Chewbacca, C-3PO, 3Pac (1.5%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP402(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P4: Drevan, Fastila, HK-47, Malak, Marauder (1.5%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P4: Drevan, Fastila, HK-47, Malak, Marauder (1.5%+)', value='```' + "\n" + message4 + '```', inline='false')


            player = fetchPlayerP403(raw_player[0])

            player['miss'].sort()
            s3: str = '\n'.join(map(str, player['miss']))
            message3 = ""
            message3 += "\n" + str(s3)
            message4 = "Nincsen hátra semmi, készen állsz a csapattal! Gratulálok! 🍺"

            if message3 != "\n":
                embed.add_field(name='P4: GG, B1, B2, Droideka, MagnaGuard (1%+)', value='```' + "\n" + message3 + '```', inline='false')
            if message3 == "\n":
                embed.add_field(name='P4: GG, B1, B2, Droideka, MagnaGuard (1%+)', value='```' + "\n" + message4 + '```', inline='false')

            await ctx.send(embed=embed)

            toc()

        else:
            pass


    @raid.error
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


def fetchPlayerP101(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "GLREY", "Rey", 13, 0, 5, 1)
    fChar(player, raw_player, "CT7567", "Rex", 13, 0, 5, 1)
    fChar(player, raw_player, "CT5555", "Fives", 13, 0, 5, 1)
    fChar(player, raw_player, "C3POLEGENDARY", "C-3PO", 13, 0, 5, 1)
    fChar(player, raw_player, "HERMITYODA", "Hermit Yoda", 13, 0, 5, 1)

    return player


def fetchPlayerP102(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "SUPREMELEADERKYLOREN", "Supreme Leader Kylo Ren", 13, 0, 5, 1)
    fChar(player, raw_player, "NIGHTSISTERZOMBIE", "Nightsister Zombie", 13, 0, 5, 1)
    fChar(player, raw_player, "DAKA", "Old Daka", 13, 0, 5, 1)
    fChar(player, raw_player, "GENERALHUX", "General Hux", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDADMIRALTHRAWN", "Grand Admiral Thrawn", 13, 0, 5, 1)

    return player


def fetchPlayerP103(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "PADMEAMIDALA", "Padmé Amidala", 13, 0, 5, 1)
    fChar(player, raw_player, "AHSOKATANO", "Ahsoka Tano", 13, 0, 5, 1)
    fChar(player, raw_player, "ANAKINKNIGHT", "Jedi Knight Anakin", 13, 0, 5, 1)
    fChar(player, raw_player, "GENERALKENOBI", "General Kenobi", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 13, 0, 5, 1)

    return player


def fetchPlayerP104(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "SITHPALPATINE", "Sith Eternal Emperor", 13, 0, 5, 1)
    fChar(player, raw_player, "DARTHTRAYA", "Darth Traya", 13, 0, 5, 1)
    fChar(player, raw_player, "DARTHSION", "Darth Sion", 13, 0, 5, 1)
    fChar(player, raw_player, "SITHTROOPER", "Sith Empire Trooper", 13, 0, 5, 1)
    fChar(player, raw_player, "DARTHSIDIOUS", "Darth Sidious", 13, 0, 5, 1)

    return player


def fetchPlayerP201(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "SUPREMELEADERKYLOREN", "Supreme Leader Kylo Ren", 13, 0, 5, 1)
    fChar(player, raw_player, "GENERALHUX", "General Hux", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDADMIRALTHRAWN", "Grand Admiral Thrawn", 13, 0, 5, 1)
    fChar(player, raw_player, "KYLORENUNMASKED", "Kylo Ren (Unmasked)", 13, 0, 5, 1)
    fChar(player, raw_player, "FOSITHTROOPER", "Sith Trooper", 13, 0, 5, 1)

    return player


def fetchPlayerP202(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "VADER", "Darth Vader", 13, 0, 5, 1)
    fChar(player, raw_player, "WATTAMBOR", "Wat Tambor", 13, 0, 5, 1)
    fChar(player, raw_player, "DARTHMALAK", "Darth Malak", 13, 0, 5, 1)
    fChar(player, raw_player, "EMPERORPALPATINE", "Emperor Palpatine", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDADMIRALTHRAWN", "Grand Admiral Thrawn", 13, 0, 5, 1)

    return player


def fetchPlayerP203(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "SHAAKTI", "Shaak Ti", 13, 0, 5, 1)
    fChar(player, raw_player, "CT7567", "Rex", 13, 0, 5, 1)
    fChar(player, raw_player, "ARCTROOPER501ST", "ARC Trooper", 13, 0, 5, 1)
    fChar(player, raw_player, "CT210408", "Echo", 13, 0, 5, 1)
    fChar(player, raw_player, "CT5555", "Fives", 13, 0, 5, 1)

    return player


def fetchPlayerP204(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "JEDIKNIGHTREVAN", "Jedi Knight Revan", 13, 0, 5, 1)
    fChar(player, raw_player, "JEDIKNIGHTLUKE", "Jedi Knight Luke Skywalker", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDMASTERLUKE", "Jedi Master Luke Skywalker", 13, 0, 5, 1)
    fChar(player, raw_player, "GENERALSKYWALKER", "General Skywalker", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 13, 0, 5, 1)

    return player


def fetchPlayerP205(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "JEDIKNIGHTREVAN", "Jedi Knight Revan", 13, 0, 5, 1)
    fChar(player, raw_player, "JEDIKNIGHTLUKE", "Jedi Knight Luke Skywalker", 13, 0, 5, 1)
    fChar(player, raw_player, "GENERALSKYWALKER", "General Skywalker", 13, 0, 5, 1)
    fChar(player, raw_player, "GRANDMASTERYODA", "Grand Master Yoda", 13, 0, 5, 1)
    fChar(player, raw_player, "HERMITYODA", "Hermit Yoda", 13, 0, 5, 1)

    return player


def fetchPlayerP401(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "COMMANDERLUKESKYWALKER", "Commander Luke Skywalker", 13, 0, 5, 1)
    fChar(player, raw_player, "HANSOLO", "Han Solo", 13, 0, 5, 1)
    fChar(player, raw_player, "CHEWBACCALEGENDARY", "Chewbacca", 13, 0, 5, 1)
    fChar(player, raw_player, "C3POLEGENDARY", "C-3PO", 13, 0, 5, 1)
    fChar(player, raw_player, "C3POCHEWBACCA", "Threepio & Chewie", 13, 0, 5, 1)

    return player


def fetchPlayerP402(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "DARTHREVAN", "Darth Revan", 13, 0, 5, 1)
    fChar(player, raw_player, "BASTILASHANDARK", "Bastila Shan (Fallen)", 13, 0, 5, 1)
    fChar(player, raw_player, "HK47", "HK-47", 13, 0, 5, 1)
    fChar(player, raw_player, "DARTHMALAK", "Darth Malak", 13, 0, 5, 1)
    fChar(player, raw_player, "SITHMARAUDER", "Sith Marauder", 13, 0, 5, 1)

    return player


def fetchPlayerP403(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "chars": [],
        "miss": [],
    }

    player['jatekosnev'] = raw_player['name']

    fChar(player, raw_player, "GRIEVOUS", "General Grievous", 13, 0, 5, 1)
    fChar(player, raw_player, "B1BATTLEDROIDV2", "B1 Battle Droid", 13, 0, 5, 1)
    fChar(player, raw_player, "B2SUPERBATTLEDROID", "B2 Super Battle Droid", 13, 0, 5, 1)
    fChar(player, raw_player, "DROIDEKA", "Droideka", 13, 0, 5, 1)
    fChar(player, raw_player, "MAGNAGUARD", "IG-100 MagnaGuard", 13, 0, 5, 1)

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
    bot.add_cog(Raidcheck(bot))