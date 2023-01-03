import discord
from discord.ext import commands

class Denzel(commands.Bot):
    """
    main class for bot

    """

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    """
    async def on_member_join(self, member):
        guild = mem

    """


    

