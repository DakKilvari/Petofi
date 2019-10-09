import discord
from discord.ext.commands import Bot

BOT_PREFIX = (".")
TOKEN = "YOUR TOKEN"

bot = Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    game = discord.Game(".help")
    await bot.change_presence(status=discord.Status.online, activity=game)

extensions = ['cmd_DS_Geo_TB', 'cmd_TW', 'cmd_Top80', 'error_handler']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('{} is loaded.'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

bot.run(TOKEN)
