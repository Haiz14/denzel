import discord
from discord.ext import commands


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="list")
    async def list(self, ctx):
        """
        The commamd only works if user is Channel owner
        """

        # get user role
        member = ctx.message.author
        roles = [role.name for role in member.roles]

        # check if user is Owner
        if "Owner" in roles:
            await ctx.send("you are owner")
            extensions = self.bot.extensions.keys()

            extensions = "\n".join(extensions)
            await ctx.send(f'Loaded extensions are: {extensions}')
            print(extensions[3])
            try:
                # try to reload extension
                await self.bot.unload_extension(extensions[3])
                await self.bot.load_extension(extensions[3])
                print(f"Extension {extensions[3]} succesfull reloaded")
            except Exception as e:
                print("Couldn't reload because of", e)



        else:
            await ctx.send("you are not the **owner**, so can't use the command")
            

async def setup(bot):
    await bot.add_cog(Reload(bot))
