from db_handler import db_handler
from numpy import *
import discord
from discord.ext import commands


class CG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Regisztracio'])
    @commands.has_any_role('Leader', 'Officer', 'Commander')  # User need this role to run command (can have multiple)
    async def register(self, ctx, userid:str, allycode:int):

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

            if myresult == None:
                DiscordName: str = str(ctx.message.mentions[0])
                DiscordName = DiscordName[:-5]
                print(DiscordID)
                print(DiscordName)
                sql = "INSERT INTO pilvax (DiscordID, DiscordName, Allycode) VALUES (%s, %s, %s)"
                val = (DiscordID, DiscordName, allycode)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.message.add_reaction("✅")
                print(mycursor.rowcount, "record inserted.")
            else:
                await ctx.message.add_reaction("❌")
                await ctx.send("<@" + DiscordID + ">" + " már regisztrált.")

            mycursor.close()
            mydb.close()

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Hibás beviteli érték!")

    @register.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



    @commands.command(aliases=['Torles'])
    @commands.has_any_role('Leader', 'Officer', 'Commander')  # User need this role to run command (can have multiple)
    async def delete(self, ctx, userid:str):

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
                sql = "DELETE FROM pilvax WHERE DiscordID = %s"
                id = (DiscordID,)
                mycursor.execute(sql, id)
                mydb.commit()
                await ctx.message.add_reaction("✅")
                print(mycursor.rowcount, "record(s) deleted")
            else:
                await ctx.message.add_reaction("❌")
                await ctx.send("<@" + DiscordID + ">" + " nincs az adatbázisban.")

            mycursor.close()
            mydb.close()

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Hibás beviteli érték!")

    @delete.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



    @commands.command(aliases=['Hozzaadas'])
    @commands.has_any_role('Cukrosnéni')  # User need this role to run command (can have multiple)
    async def add(self, ctx, userid:str, number:int, tipus:str):

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
                    sql = "SELECT Cookie FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    if n + number > 5:
                        n = 5 - number

                    sql = "UPDATE pilvax SET Cookie = %s WHERE DiscordID = %s"
                    val = (n + number, DiscordID)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    await ctx.message.add_reaction("✅")
                    print(mycursor.rowcount, "record(s) affected")
                    t = n + number
                    await ctx.send("<@" + DiscordID + ">" + " kapott " + str(number) + " 🍪-t, így van neki " + str(t))

                if tipus == "zacc":
                    sql = "SELECT Ground FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    sql = "UPDATE pilvax SET Ground = %s WHERE DiscordID = %s"
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



    @commands.command(aliases=['Elvonas'])
    @commands.has_any_role('Cukrosnéni')  # User need this role to run command (can have multiple)
    async def remove(self, ctx, userid:str, number:int, tipus:str):

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
                    sql = "SELECT Cookie FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    sql = "UPDATE pilvax SET Cookie = %s WHERE DiscordID = %s"
                    val = (n - number, DiscordID)
                    t = n - number

                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record(s) affected")
                    await ctx.send(
                        "<@" + DiscordID + ">" + " megevett " + str(number) + " 🍪-t, így van neki " + str(t))

                if tipus == "zacc":
                    sql = "SELECT Cookie FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    if n >= 2:

                        sql = "UPDATE pilvax SET Cookie = %s WHERE DiscordID = %s"
                        val = (n - 1, DiscordID)

                        mycursor.execute(sql, val)
                        mydb.commit()
                        sql = "SELECT Ground FROM pilvax WHERE DiscordID = %s"
                        adr = (DiscordID,)
                        mycursor.execute(sql, adr)
                        myresult = mycursor.fetchone()
                        for x in myresult:
                            n = x

                        sql = "UPDATE pilvax SET Ground = %s WHERE DiscordID = %s"
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

    @remove.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



    @commands.command(aliases=['Lejart'])
    @commands.has_any_role('Cukrosnéni')  # User need this role to run command (can have multiple)
    async def expire(self, ctx, userid:str, number:int, tipus:str):

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
                    sql = "SELECT Ground FROM pilvax WHERE DiscordID = %s"
                    adr = (DiscordID,)
                    mycursor.execute(sql, adr)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        n = x

                    sql = "UPDATE pilvax SET Ground = %s WHERE DiscordID = %s"
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

    @expire.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



    @commands.command(aliases=['Lekeres'])
    @commands.has_any_role('Member')  # User need this role to run command (can have multiple)
    async def mennyi(self, ctx, userid:str):

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
                n: int
                sql = "SELECT Cookie FROM pilvax WHERE DiscordID = %s"
                adr = (DiscordID,)
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchone()
                for x in myresult:
                    n = x

                z: int
                sql = "SELECT Ground FROM pilvax WHERE DiscordID = %s"
                adr = (DiscordID,)
                mycursor.execute(sql, adr)
                myresult = mycursor.fetchone()
                for x in myresult:
                    z = x

                await ctx.send("<@" + DiscordID + ">" + " -nak " + str(n) + " 🍪-e és " + str(z) + " ☕-a van.")

            else:
                await ctx.message.add_reaction("❌")
                await ctx.send("<@" + DiscordID + ">" + " nincs az adatbázisban.")

            mycursor.close()
            mydb.close()

        else:
            await ctx.message.add_reaction("❌")
            await ctx.send("Hibás beviteli érték!")

    @mennyi.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



    @commands.command(aliases=['Zaccok'])
    @commands.has_any_role('Leader', 'Officer', 'Commander')  # User need this role to run command (can have multiple)
    async def zaccosodott(self, ctx):

        AuthorID = "0"
        DiscordID = "0"
        database = db_handler(AuthorID, DiscordID)
        mydb = database.myDb()
        mycursor = mydb.cursor()

        sql = "SELECT DiscordName FROM pilvax WHERE Ground > 2"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        n = []
        i: int = 0
        for x in myresult:
            n.insert(i, x[0])
            i += 1
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



    @commands.command(aliases=['Osszes suti es zacc'])
    @commands.has_any_role('Leader', 'Officer', 'Commander')  # User need this role to run command (can have multiple)
    async def osszes(self, ctx):

        await ctx.message.add_reaction("⏳")

        AuthorID = "0"
        DiscordID = "0"
        database = db_handler(AuthorID, DiscordID)
        mydb = database.myDb()
        mycursor = mydb.cursor()

        i: int = 0
        player = [{'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},
                  {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0}, {'nev': ' ', 'suti': 0, 'zacc': 0},]

        sql = "SELECT DiscordName, Cookie, Ground FROM pilvax"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            player[i]['nev'] = x[0][:-5]
            player[i]['suti'] = x[1]
            player[i]['zacc'] = x[2]
            print(str(player[i]['nev']) + "  " + str(player[i]['suti']) + "  " + str(player[i]['zacc']))
            i += 1

        mycursor.close()
        mydb.close()

        player.sort(reverse=False, key=Sort)

        i = 0
        n = int_(len(player))
        lth = 0
        while i < n:
            lth2 = int_(len(player[i]['nev']))
            if lth2 > lth:
                lth = lth2
            i += 1

        embed = discord.Embed(title='Pilvax Hungary',
                              url="https://swgoh.gg/g/1294/pilvax-hungary/",
                              color=0x7289da)

        i = 0
        embed.add_field(name='============== Süti és Zacctáblázat 1/5 ==============', value=
        '```' + str(player[i]['nev']) + ' ' * (lth - len(str(player[i]['nev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 1]['nev']) + ' ' * (lth - len(str(player[i + 1]['nev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 2]['nev']) + ' ' * (lth - len(str(player[i + 2]['nev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 3]['nev']) + ' ' * (lth - len(str(player[i + 3]['nev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 4]['nev']) + ' ' * (lth - len(str(player[i + 4]['nev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 5]['nev']) + ' ' * (lth - len(str(player[i + 5]['nev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 6]['nev']) + ' ' * (lth - len(str(player[i + 6]['nev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 7]['nev']) + ' ' * (lth - len(str(player[i + 7]['nev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 8]['nev']) + ' ' * (lth - len(str(player[i + 8]['nev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 9]['nev']) + ' ' * (lth - len(str(player[i + 9]['nev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```', inline='false')

        i = 10
        embed.add_field(name='============== Süti és Zacctáblázat 2/5 ==============', value=
        '```' + str(player[i]['nev']) + ' ' * (lth - len(str(player[i]['nev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 1]['nev']) + ' ' * (lth - len(str(player[i + 1]['nev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 2]['nev']) + ' ' * (lth - len(str(player[i + 2]['nev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 3]['nev']) + ' ' * (lth - len(str(player[i + 3]['nev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 4]['nev']) + ' ' * (lth - len(str(player[i + 4]['nev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 5]['nev']) + ' ' * (lth - len(str(player[i + 5]['nev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 6]['nev']) + ' ' * (lth - len(str(player[i + 6]['nev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 7]['nev']) + ' ' * (lth - len(str(player[i + 7]['nev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 8]['nev']) + ' ' * (lth - len(str(player[i + 8]['nev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 9]['nev']) + ' ' * (lth - len(str(player[i + 9]['nev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```', inline='false')

        i=20
        embed.add_field(name='============== Süti és Zacctáblázat 3/5 ==============', value=
        '```' + str(player[i]['nev']) + ' ' * (lth - len(str(player[i]['nev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 1]['nev']) + ' ' * (lth - len(str(player[i + 1]['nev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 2]['nev']) + ' ' * (lth - len(str(player[i + 2]['nev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 3]['nev']) + ' ' * (lth - len(str(player[i + 3]['nev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 4]['nev']) + ' ' * (lth - len(str(player[i + 4]['nev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 5]['nev']) + ' ' * (lth - len(str(player[i + 5]['nev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 6]['nev']) + ' ' * (lth - len(str(player[i + 6]['nev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 7]['nev']) + ' ' * (lth - len(str(player[i + 7]['nev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 8]['nev']) + ' ' * (lth - len(str(player[i + 8]['nev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 9]['nev']) + ' ' * (lth - len(str(player[i + 9]['nev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```', inline='false')

        i=30
        embed.add_field(name='============== Süti és Zacctáblázat 4/5 ==============', value=
        '```' + str(player[i]['nev']) + ' ' * (lth - len(str(player[i]['nev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 1]['nev']) + ' ' * (lth - len(str(player[i + 1]['nev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 2]['nev']) + ' ' * (lth - len(str(player[i + 2]['nev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 3]['nev']) + ' ' * (lth - len(str(player[i + 3]['nev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 4]['nev']) + ' ' * (lth - len(str(player[i + 4]['nev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 5]['nev']) + ' ' * (lth - len(str(player[i + 5]['nev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 6]['nev']) + ' ' * (lth - len(str(player[i + 6]['nev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 7]['nev']) + ' ' * (lth - len(str(player[i + 7]['nev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 8]['nev']) + ' ' * (lth - len(str(player[i + 8]['nev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 9]['nev']) + ' ' * (lth - len(str(player[i + 9]['nev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```', inline='false')

        i=40
        embed.add_field(name='============== Süti és Zacctáblázat 5/5 ==============', value=
        '```' + str(player[i]['nev']) + ' ' * (lth - len(str(player[i]['nev']))) + ' ' + str(player[i]['suti']) + ' 🍪' + '  ' + str(player[i]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 1]['nev']) + ' ' * (lth - len(str(player[i + 1]['nev']))) + ' ' + str(player[i + 1]['suti']) + ' 🍪' + '  ' + str(player[i + 1]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 2]['nev']) + ' ' * (lth - len(str(player[i + 2]['nev']))) + ' ' + str(player[i + 2]['suti']) + ' 🍪' + '  ' + str(player[i + 2]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 3]['nev']) + ' ' * (lth - len(str(player[i + 3]['nev']))) + ' ' + str(player[i + 3]['suti']) + ' 🍪' + '  ' + str(player[i + 3]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 4]['nev']) + ' ' * (lth - len(str(player[i + 4]['nev']))) + ' ' + str(player[i + 4]['suti']) + ' 🍪' + '  ' + str(player[i + 4]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 5]['nev']) + ' ' * (lth - len(str(player[i + 5]['nev']))) + ' ' + str(player[i + 5]['suti']) + ' 🍪' + '  ' + str(player[i + 5]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 6]['nev']) + ' ' * (lth - len(str(player[i + 6]['nev']))) + ' ' + str(player[i + 6]['suti']) + ' 🍪' + '  ' + str(player[i + 6]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 7]['nev']) + ' ' * (lth - len(str(player[i + 7]['nev']))) + ' ' + str(player[i + 7]['suti']) + ' 🍪' + '  ' + str(player[i + 7]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 8]['nev']) + ' ' * (lth - len(str(player[i + 8]['nev']))) + ' ' + str(player[i + 8]['suti']) + ' 🍪' + '  ' + str(player[i + 8]['zacc']) + ' ♨️' + '\n' +
        str(player[i + 9]['nev']) + ' ' * (lth - len(str(player[i + 9]['nev']))) + ' ' + str(player[i + 9]['suti']) + ' 🍪' + '  ' + str(player[i + 9]['zacc']) + ' ♨️' + '\n' + '```', inline='false')

        await ctx.send(embed=embed)

        await ctx.message.add_reaction("✅")


    @osszes.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def Sort(a):
    return a['nev']


def setup(bot):
    bot.add_cog(CG(bot))