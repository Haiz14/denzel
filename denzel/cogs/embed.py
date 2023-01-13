
import discord
from discord.ext import commands

class EmbedCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gpt")
    async def gpt_command(self, ctx):
        # Create a new embed object
        embed = discord.Embed(title="My Link", description="This is a link to my website")

        # Add a field to the embed
        embed.add_field(name="Link", value="https://example.com", inline=False)

        # Set the color of the embed
        embed.color = 0xFF0000

        # Send the embed to the channel
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        print('message sent')

async def setup(bot):
    await bot.add_cog(EmbedCogs(bot))
