import discord
from discord import app_commands
from discord.ext import commands
from better_profanity import profanity


class WordFilter(commands.Cog):

    profanity.load_censor_words()
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.last_message = None
        self.last_second_message = None
        self.last_third_message= None
        self._last_member = None



    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        

        if message.author == self.bot.user:
            return

        elif profanity.contains_profanity(message.content):
            # replace the bad word with asterisks
            new_message = profanity.censor(message.content)
            await message.delete()
            embed = discord.Embed(title="Prohibited message", description=f"The new message is : {new_message}", color=0xff0000)
            await message.channel.send(embed=embed)


        self.last_third_message = self.last_second_message
        self.last_second_message = self.last_message
        self.last_message = message.content

        print(f'1: {self.last_message} \n 2: {self.last_second_message} \n 3: {self.last_third_message}')
        if self.last_message == self.last_second_message == self.last_third_message:
            await message.channel.send(f"{message.author.mention} you are spamming plss stop")

    

async def setup(bot):
    await bot.add_cog(WordFilter(bot))
