from discord.ext import commands
import os

description = '''Tabletop Games Discord Bot'''

if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    bot.load_extension('cogs.character')
    bot.run(os.environ['DISCORD_TOKEN'])