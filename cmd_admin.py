import global_settings
from api_swgoh_help import api_swgoh_help, settings
from numpy import *
import time
from db_handler import db_handler
from discord.ext import commands
import discord

creds = settings()
client = api_swgoh_help(creds)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Játékos regisztrálása'])
    @commands.has_any_role(global_settings.Role1, global_settings.Role2)  # User need this role to run command (can have multiple)
    async def reg(self, ctx, userid:str, allycode:int):
        """Játékos regisztrálása
        Játékos Petőfi botba regisztrálása
        userid: taggelés
        allycode: játékos ally kódja"""

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

    @reg.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')



    @commands.command(aliases=['Játékos törlése'])
    @commands.has_any_role(global_settings.Role1, global_settings.Role2)  # User need this role to run command (can have multiple)
    async def torol(self, ctx, userid:str):
        """Játékos törlése
        Játékos törlése a Petőfi botból
        userid: taggelés"""

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

    @torol.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')


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
    bot.add_cog(Admin(bot))