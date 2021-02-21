import global_settings
from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import time
from db_handler import db_handler
from discord.ext import commands
import discord

creds = settings()
client = api_swgoh_help(creds)


class Bakery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Süti / zacc hozzáadása'])
    @commands.has_any_role(global_settings.Role4)  # User need this role to run command (can have multiple)
    async def add(self, ctx, userid: str, number: int, tipus: str):
        """Süti / zacc hozzáadása
        Süti vagy zacc kiosztása
        userid: taggelés
        number: darabszám (süti: 1-5, zacc: 1-3)
        tipus: suti vagy zacc"""

        AuthorID = str(ctx.author.id)
        try:
            DiscordID = str(ctx.message.mentions[0].id)
        except:
            DiscordID = "000000000"

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if myresult != None:
                if tipus == "suti":
                    sql = "SELECT Suti FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    if n + number > 6:
                        n = 6 - number

                    sql = "UPDATE pilvax SET Suti = %s WHERE DiscordID = %s"
                    val = (n + number, DiscordID)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    await ctx.message.add_reaction("✅")
                    print(mycursor.rowcount, "record(s) affected")
                    t = n + number
                    await ctx.send("<@" + DiscordID + ">" + " kapott " + str(number) + " 🍪-t, így van neki " + str(t))

                if tipus == "zacc":
                    sql = "SELECT Zacc FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    sql = "UPDATE pilvax SET Zacc = %s WHERE DiscordID = %s"
                    val = (n + number, DiscordID)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    await ctx.message.add_reaction("✅")
                    print(mycursor.rowcount, "record(s) affected")
                    t = n + number
                    await ctx.send("<@" + DiscordID + ">" + " kapott " + str(number) + " ☕-t, így van neki " + str(t))

                if tipus != "suti" and tipus != "zacc":
                    await ctx.message.add_reaction("❌")

            else:
                await ctx.message.add_reaction("❌")
                await ctx.send(DiscordID + " nincs az adatbázisban.")

            mycursor.close()
            mydb.close()

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Hibás beviteli érték!")

    @add.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

    @commands.command(aliases=['Süti megevése / Zacc beváltása'])
    @commands.has_any_role(global_settings.Role4)  # User need this role to run command (can have multiple)
    async def rem(self, ctx, userid: str, number: int, tipus: str):
        """Süti megevése / Zacc beváltása
        Süti vagy zacc elvétele. Zacc esetén levon 2 sütit
        userid: taggelés
        number: darabszám (süti: 1-5, zacc: 1-2)
        tipus: suti vagy zacc"""

        AuthorID = str(ctx.author.id)
        try:
            DiscordID = str(ctx.message.mentions[0].id)
        except:
            DiscordID = "000000000"

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if myresult != None:
                if tipus == "suti":
                    sql = "SELECT Suti FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    sql = "UPDATE pilvax SET Suti = %s WHERE DiscordID = %s"
                    val = (n - number, DiscordID)
                    t = n - number

                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record(s) affected")
                    await ctx.send(
                        "<@" + DiscordID + ">" + " megevett " + str(number) + " 🍪-t, így van neki " + str(t))

                if tipus == "zacc":
                    sql = "SELECT Suti FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    if n >= 3:

                        sql = "UPDATE pilvax SET Suti = %s WHERE DiscordID = %s"
                        val = (n - 1, DiscordID)

                        mycursor.execute(sql, val)
                        mydb.commit()
                        sql = "SELECT Zacc FROM pilvax WHERE DiscordID = %s"
                        adr = (DiscordID,)
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchone()
                        for x in myresult:
                            n = x

                        sql = "UPDATE pilvax SET Zacc = %s WHERE DiscordID = %s"
                        val = (n - number, DiscordID)
                        t = n - number

                        mycursor.execute(sql, val)
                        mydb.commit()

                        print(mycursor.rowcount, "record(s) affected")
                        await ctx.send(
                            "<@" + DiscordID + ">" + " beváltott két 🍪-t egy ☕ kiváltására, így van neki " + str(t))
                    else:
                        await ctx.message.add_reaction("❌")
                        await ctx.send("<@" + DiscordID + ">" + " Nincs elegendő sütid a beváltásra!")

                if tipus != "suti" and tipus != "zacc":
                    await ctx.message.add_reaction("❌")

            else:
                await ctx.message.add_reaction("❌")
                await ctx.send(DiscordID + " nincs az adatbázisban.")

            mycursor.close()
            mydb.close()

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Hibás beviteli érték!")

    @rem.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

    @commands.command(aliases=['Zacc elévülése'])
    @commands.has_any_role(global_settings.Role4)  # User need this role to run command (can have multiple)
    async def exp(self, ctx, userid: str, number: int, tipus: str):
        """Zacc elévülése
        Zacc elévülése, nem von le sütit
        userid: taggelés
        number: darabszám (1-3)
        tipus: zacc"""

        AuthorID = str(ctx.author.id)
        try:
            DiscordID = str(ctx.message.mentions[0].id)
        except:
            DiscordID = "000000000"

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if myresult != None:
                if tipus == "zacc":
                    sql = "SELECT Zacc FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    sql = "UPDATE pilvax SET Zacc = %s WHERE DiscordID = %s"
                    val = (n - number, DiscordID)
                    t = n - number

                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record(s) affected")
                    await ctx.send(
                        "<@" + DiscordID + ">" + "-nak elévült " + str(number) + " ☕-a, így van neki " + str(t))

                if tipus != "zacc":
                    await ctx.message.add_reaction("❌")

            else:
                await ctx.message.add_reaction("❌")
                await ctx.send(DiscordID + " nincs az adatbázisban.")

            mycursor.close()
            mydb.close()

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Hibás beviteli érték!")

    @exp.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

    @commands.command(aliases=['Süti és zaccok számának lekérése'])
    @commands.has_any_role(global_settings.Role3)  # User need this role to run command (can have multiple)
    async def mennyi(self, ctx, raw_allycode):
        """Süti és zaccok számának lekérése
        Süti vagy zacc lekérése
        raw_allycode: me, taggelés, vagy allykód"""

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
        print(str(temp))

        try:
            raw_guild['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        DiscordID = m1
        AuthorID = m2

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if myresult != None:
                n: int
                sql = "SELECT Suti FROM pilvax WHERE DiscordID = %s"
                adr = (DiscordID,)
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchone()
                for x in myresult:
                    n = x

                z: int
                sql = "SELECT Zacc FROM pilvax WHERE DiscordID = %s"
                adr = (DiscordID,)
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchone()
                for x in myresult:
                    z = x

                await ctx.send("<@" + DiscordID + ">" + " -nak " + str(n) + " 🍪-e és " + str(z) + " ☕-a van.")

                await ctx.message.add_reaction("✅")

            else:
                await ctx.message.add_reaction("❌")

            mycursor.close()
            mydb.close()

            toc()

        else:
            pass

    @mennyi.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

    @commands.command(aliases=['Kinek van 3 zacca a guildben'])
    @commands.has_any_role(global_settings.Role1,
                           global_settings.Role2)  # User need this role to run command (can have multiple)
    async def zaccosodott(self, ctx, raw_allycode):
        """Kinek van 3 zacca a guildben
        Válasz: az összes játékos, akinek 3 vagy több zacca van"""

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
        print(str(temp))

        try:
            raw_guild['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        DiscordID = m1
        AuthorID = m2

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if temp != -1 and myresult != None:

                await ctx.send("Sütik és zaccok betöltése folyamatban. ⏳")
                print("Sütik és zaccok betöltése folyamatban")

                player = fetchPlayerRoster(raw_guild)

                i = 0
                k = 0
                y: int = 0
                n = int_(len(player))

                while k < n:
                    sql = "SELECT DiscordName, Zacc FROM pilvax WHERE Allycode = %s"
                    adr = (player[k]['allycode'],)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        player[k]['jatekosnev'] = x[0]
                        player[k]['zacc'] = x[1]
                    k += 1

                    player.sort(reverse=False, key=Sort)
                    s: str = '\n'.join(map(str, player['jatekosnev']))

                    message1 += "\n**Meglévő karakterek:** \n" + str("```ini\n" + s + "```")
                    if message1 != "":
                        await ctx.send(message1)
                    else:
                        await ctx.send("Senki nincs veszélyben!")

                    await ctx.message.add_reaction("✅")

                else:
                    await ctx.message.add_reaction("❌")

                mycursor.close()
                mydb.close()

                toc()

            else:
                pass

                player.sort(reverse=False, key=Sort)
        if n == []:
            await ctx.send("Juhhú, senki nincs veszélyben!")
        else:
            s: str = '\n'.join(map(str, n))
            await ctx.send("Akiknek 3, vagy több zaccuk van: \n" + s)

        mycursor.close()
        mydb.close()

    @zaccosodott.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

    @commands.command(aliases=['Összes süti és zacc'])
    @commands.has_any_role(global_settings.Role1,
                           global_settings.Role2)  # User need this role to run command (can have multiple)
    async def osszes(self, ctx, raw_allycode):
        """Összes süti és zacc
        Guild szinten listázza az összes sütit és zaccot minden játékosra
        raw_allycode: me, taggelés, vagy allykód"""

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
        print(str(temp))

        try:
            raw_guild['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        DiscordID = m1
        AuthorID = m2

        if DiscordID != "000000000":
            database = db_handler(AuthorID, DiscordID)
            mydb = database.myDb()
            mycursor = mydb.cursor()

            sql = "SELECT DiscordID FROM pilvax WHERE DiscordID = %s"
            adr = (DiscordID,)
            mycursor.execute(sql, adr)
            myresult = mycursor.fetchone()

            if temp != -1 and myresult != None:

                await ctx.send("Sütik és zaccok betöltése folyamatban. ⏳")
                print("Sütik és zaccok betöltése folyamatban")

                player = fetchPlayerRoster(raw_guild)

                i = 0
                k = 0
                y: int = 0
                n = int_(len(player))

                while k < n:
                    sql = "SELECT Suti, Zacc FROM pilvax WHERE Allycode = %s"
                    adr = (player[k]['allycode'],)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        player[k]['suti'] = x[0]
                        player[k]['zacc'] = x[1]
                    k += 1

                player.sort(reverse=False, key=Sort)

                i = 0
                n = int_(len(player))
                lth = 0
                while i < n:
                    lth2 = int_(len(player[i]['jatekosnev']))
                    if lth2 > lth:
                        lth = lth2
                    i += 1

                embed = discord.Embed(title='Pilvax Hungary süti és zacctábla',
                                      url="https://swgoh.gg/g/1294/pilvax-hungary/",
                                      color=0x7289da)

                i = 0
                embed.add_field(name='============ Süti és Zacctáblázat 1/5 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```',
                                inline='false')

                i = 10
                embed.add_field(name='============ Süti és Zacctáblázat 2/5 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```',
                                inline='false')

                i = 20
                embed.add_field(name='============ Süti és Zacctáblázat 3/5 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```',
                                inline='false')

                i = 30
                embed.add_field(name='============ Süti és Zacctáblázat 4/5 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```',
                                inline='false')

                i = 40
                embed.add_field(name='============ Süti és Zacctáblázat 5/5 ============', value=
                '```' + str(player[i]['jatekosnev']) + ' ' * (lth - len(str(player[i]['jatekosnev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 1]['jatekosnev']) + ' ' * (lth - len(str(player[i + 1]['jatekosnev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 2]['jatekosnev']) + ' ' * (lth - len(str(player[i + 2]['jatekosnev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 3]['jatekosnev']) + ' ' * (lth - len(str(player[i + 3]['jatekosnev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 4]['jatekosnev']) + ' ' * (lth - len(str(player[i + 4]['jatekosnev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 5]['jatekosnev']) + ' ' * (lth - len(str(player[i + 5]['jatekosnev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 6]['jatekosnev']) + ' ' * (lth - len(str(player[i + 6]['jatekosnev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 7]['jatekosnev']) + ' ' * (lth - len(str(player[i + 7]['jatekosnev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 8]['jatekosnev']) + ' ' * (lth - len(str(player[i + 8]['jatekosnev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
                str(player[i + 9]['jatekosnev']) + ' ' * (lth - len(str(player[i + 9]['jatekosnev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```',
                                inline='false')

                await ctx.send(embed=embed)

                await ctx.message.add_reaction("✅")

            else:
                await ctx.message.add_reaction("❌")

            mycursor.close()
            mydb.close()

            toc()

        else:
            pass

    @osszes.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


def Sort(a):
    return a['jatekosnev']


def fetchPlayerRoster(guilddata):
    player = [{'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0},
              {'jatekosnev': ' ', 'allycode': 0, 'suti': 0, 'zacc': 0}]

    k = 0
    lth = int_(len(guilddata[0]['roster']))

    while k < lth:
        player[k]['jatekosnev'] = guilddata[0]['roster'][k]['name']
        player[k]['allycode'] = guilddata[0]['roster'][k]['allyCode']
        k += 1

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
    bot.add_cog(Bakery(bot))