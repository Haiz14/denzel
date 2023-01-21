import os
import sqlite3

import discord
from discord.ext.commands import Bot
from better_profanity import profanity


"""
Code Overview 

Denzel main class to run bot

init: adds the intent, command_prefix to the bot Class
on_ready: 
    - prints when bot has logged in google
    - loads cogs into the bot

"""
class Denzel(Bot):

    """
     to use the bot :
     from denzel import Denzel
     bot = Denzel( COMMAND_PREFIX = "<the command prefix e.g. '!'>"
     bot.run(<BOT_TOKEN>)
    """

    def __init__(self, COMMAND_PREFIX, *args, **kwargs):

          
        intents = discord.Intents.all()

        # add intents and commamd prefix to super class
        super().__init__(intents=intents, command_prefix= COMMAND_PREFIX)


        profanity.load_censor_words()
        self.profanity = profanity

        self.bot_channel = None
        self.test_server_id = 1059338776146612254
        self.fish_cake_bets_channel_id = 1062994259034251314

        self.conn = sqlite3.connect("cake.db")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        # add guild and bot_channel
        self.bot_channel = self.get_channel(1063387085966413855)
        self.fish_cake_bets_channel = self.get_channel(self.fish_cake_bets_channel_id)
        self.test_server = self.get_guild(self.test_server_id)

        # add slash commands to only test_guild
        self.tree.copy_global_to(guild=self.test_server)

        # todo: load_cogs form  dezel/_cogs/__init__.py insted of direct file


        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"denzel.cogs.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")



    """
    async def on_message(self, message):
        

        if message.author == self.user:
            return

        elif self.profanity.contains_profanity(message.content):
            # replace the bad word with asterisks
            new_message = self.profanity.censor(message.content)
            await message.delete()
            embed = discord.Embed(title="Prohibited message", description=f"The new message is : {new_message}", color=0xff0000)
            await message.channel.send(embed=embed)

        print("a message was sent")
    """


