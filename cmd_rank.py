from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import time
from discord.ext import commands
from db_handler import db_handler

class RANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['JatekosRang'])
    @commands.has_any_role('Member')  # User need this role to run command (can have multiple)
    async def rang(self, ctx, raw_allycode):

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

            player = fetchPlayerRoster(raw_player)

            player = fetchPlayerRanknev(player)

            player['chars'].sort()
            player['ships'].sort()

            s: str = '\n'.join(map(str, player['chars']))
            s2: str = '\n'.join(map(str, player['ships']))

            if s == "" and s2 == "":
                await ctx.send("**Nincsen beszámolható egységed, vagy hajód!**")
            else:
                await ctx.send(ctx.message.author.mention + " " + player['jatekosnev'] + " jelenlegi rang pontszáma: " + str('{:,}'.format(player['rank'])) + ".  A rangja pedig: " + str(player['ranknev']))
                await ctx.send("**Beszámolt karakterek:** \n" + s + "\n\n**Beszámolt hajók:** \n" + s2)

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

    if player['rank'] >= 0 and player['rank'] <= 5:
        player['ranknev'] = "Párafarmer"
    if player['rank'] > 5 and player['rank'] <= 10:
        player['ranknev'] = "Droid"
    if player['rank'] > 10 and player['rank'] <= 15:
        player['ranknev'] = "Scavenger / Roncsvadász"
    if player['rank'] > 15 and player['rank'] <= 20:
        player['ranknev'] = "Pirate / Kalóz"
    if player['rank'] > 20 and player['rank'] <= 25:
        player['ranknev'] = "Smuggler / Csempész"
    if player['rank'] > 25 and player['rank'] <= 30:
        player['ranknev'] = "Bounty Hunter / Fejvadász"
    if player['rank'] > 30 and player['rank'] <= 35:
        player['ranknev'] = "Rebel / Stormtrooper"
    if player['rank'] > 35 and player['rank'] <= 40:
        player['ranknev'] = "X-Wing Pilot / Tie-Fighter Pilot"

    return player

def fetchPlayerRoster(raw_player):
    player = {
        "jatekosnev": " ",
        "rank": 0,
        "ranknev": " ",
        "chars": [],
        "ships": [],
    }

    player['jatekosnev'] = raw_player[0]['name']
    i = 0
    t = 0
    s = 0
    for a in raw_player[0]['roster']:
        a = raw_player[0]['roster'][i]
        if a['defId'] == "GEONOSIANBROODALPHA" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "Geonosian Brood Alpha")
                player['rank'] += 1
        if a['defId'] == "GEONOSIANSOLDIER" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Geonosian Soldier")
            player['rank'] += 1
        if a['defId'] == "GEONOSIANSPY" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Geonosian Spy")
            player['rank'] += 1
        if a['defId'] == "SUNFAC" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Sun Fac")
            player['rank'] += 1
        if a['defId'] == "POGGLETHELESSER" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Poggle the Lesser")
            player['rank'] += 1


        if a['defId'] == "GRIEVOUS" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "General Grievous")
                player['rank'] += 1
        if a['defId'] == "B1BATTLEDROIDV2" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "B1 Battle Droid")
                player['rank'] += 1
        if a['defId'] == "B2SUPERBATTLEDROID" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "B2 Super Battle Droid")
                player['rank'] += 1
        if a['defId'] == "MAGNAGUARD" and a['gear'] >= 13:
            player['chars'].insert(player['rank'], "IG-100 MagnaGuard")
            player['rank'] += 1
        if a['defId'] == "DROIDEKA" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Droideka")
            player['rank'] += 1


        if a['defId'] == "DARTHTRAYA" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "Darth Traya")
                player['rank'] += 1
        if a['defId'] == "DARTHSION" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Darth Sion")
                player['rank'] += 1
        if a['defId'] == "DARTHNIHILUS" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Darth Nihilus")
                player['rank'] += 1
        if a['defId'] == "GRANDADMIRALTHRAWN" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Grand Admiral Thrawn")
                player['rank'] += 1
        if a['defId'] == "COUNTDOOKU" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Count Dooku")
                player['rank'] += 1


        if a['defId'] == "DARTHREVAN" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 3:
                player['chars'].insert(player['rank'], "Darth Revan")
                player['rank'] += 1
        if a['defId'] == "BASTILASHANDARK" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Bastila Shan (Fallen)")
                player['rank'] += 1
        if a['defId'] == "SITHTROOPER" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Sith Trooper")
            player['rank'] += 1
        if a['defId'] == "SITHMARAUDER" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Sith Marauder")
            player['rank'] += 1
        if a['defId'] == "EMPERORPALPATINE" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "Emperor Palpatine")
                player['rank'] += 1


        if a['defId'] == "DARTHMALAK" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "Darth Malak")
                player['rank'] += 2
        if a['defId'] == "NUTEGUNRAY" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Nute Gunray")
                player['rank'] += 1


        if a['defId'] == "MOTHERTALZIN" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "Mother Talzin")
                player['rank'] += 1
        if a['defId'] == "ASAJVENTRESS" and a['gear'] >= 13:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 2:
                player['chars'].insert(player['rank'], "Asajj Ventress")
                player['rank'] += 1
        if a['defId'] == "NIGHTSISTERZOMBIE" and a['gear'] >= 12:
            player['chars'].insert(player['rank'], "Nightsister Zombie")
            player['rank'] += 1
        if a['defId'] == "DAKA" and a['gear'] >= 13:
            player['chars'].insert(player['rank'], "Old Daka")
            player['rank'] += 1
        if a['defId'] == "TALIA" and a['gear'] >= 12 and s == 0:
            t = 1
            player['chars'].insert(player['rank'], "Talia")
            player['rank'] += 1
        if a['defId'] == "NIGHTSISTERSPIRIT" and a['gear'] >= 12 and t == 0:
            s = 1
            player['chars'].insert(player['rank'], "Nightsister Spirit")
            player['rank'] += 1


        if a['defId'] == "WATTAMBOR" and a['gear'] >= 12:
            temp = 0
            for b in a['skills']:
                if b['tier'] == 8 and b['isZeta'] == True:
                    temp += 1
            if temp >= 1:
                player['chars'].insert(player['rank'], "Wat Tambor")
                player['rank'] += 1


        if a['defId'] == "CAPITALCHIMAERA" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GRANDADMIRALTHRAWN" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp == 5:
                        player['ships'].insert(player['rank'], "Chimaera")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "CAPITALSTARDESTROYER" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GRANDMOFFTARKIN" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp == 5:
                        player['ships'].insert(player['rank'], "Executrix")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "CAPITALNEGOTIATOR" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GENERALKENOBI" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp == 5:
                        player['ships'].insert(player['rank'], "Negotiator")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "GEONOSIANSTARFIGHTER2" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GEONOSIANSOLDIER" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['ships'].insert(player['rank'], "Geonosian Soldier's Starfighter")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "GEONOSIANSTARFIGHTER3" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "GEONOSIANSPY" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['ships'].insert(player['rank'], "Geonosian Spy's Starfighter")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "HOUNDSTOOTH" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "BOSSK" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['ships'].insert(player['rank'], "Hound's Tooth")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "GEONOSIANSTARFIGHTER1" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "SUNFAC" and b['gear'] >= 12:
                    temp = 0
                    for c in a['skills']:
                        if c['tier'] == 8:
                            temp += 1
                    if temp >= 3:
                        player['ships'].insert(player['rank'], "Sun Fac's Geonosian Starfighter")
                        player['rank'] += 1
                j += 1
        if a['defId'] == "MILLENNIUMFALCON" and a['rarity'] == 7 and a['level'] == 85:
            j = 0
            d = 0
            e = 0
            for b in raw_player[0]['roster']:
                b = raw_player[0]['roster'][j]
                if b['defId'] == "HANSOLO" and b['gear'] >= 12:
                    d = 1
                if b['defId'] == "CHEWBACCALEGENDARY" and b['gear'] >= 12:
                    e = 1
                j += 1
            if d == 1 and e == 1:
                temp = 0
                for c in a['skills']:
                    if c['tier'] == 8:
                        temp += 1
                if temp == 4:
                    player['ships'].insert(player['rank'], "Han's Millennium Falcon")
                    player['rank'] += 1
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
    bot.add_cog(RANK(bot))
