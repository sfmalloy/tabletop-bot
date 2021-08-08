from discord.ext import commands
import asyncio
import json

class character_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock()
        with open('chars.json', 'r') as f:
            self.char_json = json.load(f)
    
    def __del__(self):
        with open('chars.json', 'w') as f:
            json.dump(self.char_json, f)
        print('Characters exported successfully')

    @commands.command(
        name = 'add_character',
        description = 'Add a new character to speak as',
        usage='add_character <character_name> [<profile_picture_url>]',
        example='add_character Bob https://example.org/profile_picture.jpg'
    )
    async def add_character(self, ctx, *args):
        await ctx.message.delete()
        
        pfp = None
        if args[-1][0:4] == 'http':
            pfp = args[-1]
        name = ' '.join(args[:-1])

        obj = {'name':name, 'pfp':pfp}
        self.char_json.append(obj)

        await ctx.send(f'{name} succesfully added!')
    
    @commands.command(
        name = 'say',
        description = 'Send a message under a different alias. If character name has been added using ' + 
            'the "add" command with a profile picture, that picture will be used',
        usage='say <character_name>:<message>',
        example='say Bob:Hello there my name is Bob!'
    )
    async def say(self, ctx, *args):
        # Delete message containing command
        await ctx.message.delete()

        # Format and send message from custom username
        try:
            name, msg = ' '.join(args).split(':')
        except:
            await ctx.channel.send('Please include a colon (i.e. :) after the name of the character')
        webhook = await ctx.channel.create_webhook(name=name)

        name_found = False
        pfp = ''
        for char in self.char_json:
            if char['name'] == name:
                name_found = True
                pfp = char['pfp']
                break
        if name_found:
            await webhook.send(msg, username=name, avatar_url=pfp)
        else:
            await webhook.send(msg, username=name)
        
        # Clean up webhooks
        for wh in await ctx.channel.webhooks():
            await wh.delete()

def setup(bot):
    print('Setting up test')
    bot.add_cog(character_cog(bot))