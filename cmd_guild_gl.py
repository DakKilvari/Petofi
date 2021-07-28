from api_swgoh_help import api_swgoh_help, settings
from db_handler import db_handler
from numpy import *
from discord.utils import get
import discord
import time
from discord.ext import commands
import cmd_rank
import global_settings

creds = settings()
client = api_swgoh_help(creds)


class GuildGpl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Aktuális guild gl állás'])
    @commands.has_any_role(global_settings.Role1, global_settings.Role2, global_settings.Role3, global_settings.Role5)  # User need this role to run command (can have multiple)
    async def gpl(self, ctx, raw_allycode):
        """Aktuális guild gl állás"""

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

        if isinstance(raw_guild, str):
            await ctx.send("Api error: " + raw_player)

        temp = 0

        try:
            raw_guild['status_code'] == 404
            await ctx.send("Hibás ally kód!")
            await ctx.message.add_reaction("❌")
            temp = -1
        except:
            pass

        if temp != -1:
            print("\n" + "Guild GL lekérés folyamatban.")

            guilddata = fetchGuildRoster(raw_guild)
            player = fetchPlayerRoster(guilddata)
            player.sort(reverse=True, key=Sort)

            kylo1 = get(ctx.bot.emojis, name="kylo1")
            rey1 = get(ctx.bot.emojis, name="rey1")
            jml1 = get(ctx.bot.emojis, name="jml1")
            see1 = get(ctx.bot.emojis, name="see1")
            jmk1 = get(ctx.bot.emojis, name="jmk1")
            blank = get(ctx.bot.emojis, name="blank")

            slkr = 0
            rey = 0
            jml = 0
            see = 0
            jmk = 0

            k=0

            while k < int_(len(player)) and player[k]['ranknev']!='end':
                if player[k]['slkr'] == 1:
                    player[k]['ranknev'] += str(kylo1) 
                    slkr += 1 
                else:
                    player[k]['ranknev'] += str(blank) 
               
                if player[k]['rey'] == 1:
                    player[k]['ranknev'] += str(rey1)
                    rey += 1 
                else:
                    player[k]['ranknev'] += str(blank) 
                
                if player[k]['jml'] == 1:
                    player[k]['ranknev'] += str(jml1)
                    jml += 1 
                else:
                    player[k]['ranknev'] += str(blank) 
                
                if player[k]['see'] == 1:
                    player[k]['ranknev'] += str(see1)
                    see += 1 
                else:
                    player[k]['ranknev'] += str(blank) 

                if player[k]['jmk'] == 1:
                    player[k]['ranknev'] += str(jmk1)
                    jmk += 1 
                else:
                    player[k]['ranknev'] += str(blank) 

                k += 1


            print("\n" + "Done.")

            message = raw_guild[0]['name'] + ' guild GL készlete \nGP: '+ '{:,}'.format(raw_guild[0]['gp'])+'\n'
            message += '-==============================-\n'

            message += str(kylo1) + ': ' + str(slkr) + ' db\n' 
            message += str(rey1) + ': ' + str(rey) + ' db\n' 
            message += str(jml1) + ': ' + str(jml) + ' db\n' 
            message += str(see1) + ': ' + str(see) + ' db\n' 
            message += str(jmk1) + ': ' + str(jmk) + ' db\n'

            i = 0
            maxgl = 5
            
            while maxgl>0:
                message += '-============== ' + str(maxgl) + ' GL ==============-\n'
                while i<int_(len(player)) and player[i]['gl']==maxgl:
                    message += '`' + player[i]['jatekosnev'].ljust(26, ' ') + '`'+ player[i]['ranknev'] + '\n'
                    i +=1
                maxgl -=1

            lines = message.splitlines(True)  
            currmessage = ''
            for line in lines:
                if len(currmessage)+len(line)>2000:
                    await ctx.send(currmessage)
                    currmessage = line
                else:
                    currmessage +=line
            
            await ctx.message.add_reaction("✅")

            await ctx.send(currmessage)

            toc()

        else:
            pass

    @gpl.error
    async def josoultsag_hiba(self, ctx, error):
        self.ctx = ctx
        if isinstance(error, commands.CheckFailure):
            print("\n" + "Jogosultság hiba!")
            await self.ctx.send('⛔ - Nincsen hozzá jogosultságod!')

def Sort(a):
    return a['gl']

def fetchPlayerRanknev(player):
    i = 0
    n = int_(len(player))
    while i < n:
        cmd_rank.fetchPlayerRanknev(player[i])
        i += 1

    return player

def fetchGuildRoster(raw_guild):
    guilddata = []
    chardata_ally = []
    chardata_ally2 = []
    i: int = 0
    lth = int_(len(raw_guild[0]['roster']))
    lthp2 = int_(round(lth/2, 0))
    while i < lthp2:
        chardata_ally.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata = client.fetchPlayers(chardata_ally)

    while i < lth:
        chardata_ally2.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata += client.fetchPlayers(chardata_ally2)

    return guilddata


def fetchPlayerRoster(guilddata):
    player = [{'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0},
              {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}, {'jatekosnev': ' ', 'gl': 0, 'slkr' : 0, 'rey' : 0, 'jml' : 0, 'see' : 0, 'jmk' : 0}]

    k=0
    for g in guilddata:
        raw_player = guilddata[k]
        player[k]['jatekosnev'] = guilddata[k]['name']
        player[k]['slkr'] = fEChar(raw_player, 'SUPREMELEADERKYLOREN')
        player[k]['rey'] = fEChar(raw_player, 'GLREY')
        player[k]['jml'] = fEChar(raw_player, 'GRANDMASTERLUKE')
        player[k]['see'] = fEChar(raw_player, 'SITHPALPATINE')
        player[k]['jmk'] = fEChar(raw_player, 'JEDIMASTERKENOBI')

        player[k]['gl'] = player[k]['slkr'] + player[k]['rey'] + player[k]['jml'] + player[k]['see'] + player[k]['jmk']

        player[k]['ranknev'] = ''

        k += 1
    
    if k<50:
        player[k]['ranknev'] = 'end'

    return player

def fEChar(raw_player, defID):
    retval = 0

    i=0
    for a in raw_player['roster']:
        a = raw_player['roster'][i]
        if a['defId'] == defID:
            retval = 1
        i += 1
    return retval


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
    bot.add_cog(GuildGpl(bot))