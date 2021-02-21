from discord.ext.commands import Bot
import discord

BOT_PREFIX = (".")
TOKEN = "NjExODc0Mjc4NjE0MzY4Mjc1.XbDZLw.XxVgpIkYJy8VcyXzQQKRhWYY3Gk"
TOKEN2 = "NjExODc0Mjc4NjE0MzY4Mjc1.XbDZLw.XxVgpIkYJy8VcyXzQQKRhWYY3Gk"
bot = Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    game = discord.Game(".help")
    await bot.change_presence(status=discord.Status.online, activity=game)

extensions = ['cmd_admin', 'cmd_ds_geo_tb', 'cmd_guild_diff', 'cmd_guild_rank', 'cmd_bakery', 'cmd_guild_save', 'cmd_kam', 'cmd_legendary',
              'cmd_ls_check', 'cmd_ls_geo_tb', 'cmd_rank', 'cmd_top80', 'cmd_tw', 'error_handler']


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('{} is loaded.'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

bot.run(TOKEN)
