import discord
from discord import app_commands
from discord.ext import commands
from better_profanity import profanity


class WordFilter(commands.Cog):

    profanity.load_censor_words()
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None



    @commands.Cog.listener()
    async def on_message(self, message):
        

        if message.author == self.bot.user:
            return

        elif profanity.contains_profanity(message.content):
            # replace the bad word with asterisks
            new_message = profanity.censor(message.content)
            await message.delete()
            embed = discord.Embed(title="Prohibited message", description=f"The new message is : {new_message}", color=0xff0000)
            await message.channel.send(embed=embed)

        print("a message was sent")

    

async def setup(bot):
    await bot.add_cog(WordFilter(bot))
