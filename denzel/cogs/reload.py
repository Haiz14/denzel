import discord
from discord.ext import commands


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="reload", aliases=["ree"], description="reloads extension")
    async def reload(self, ctx, arg1):
        """
        works only if user has "Owner" role

        - check if user has owner role and send message if user is not owner
        - check if arg provided is in, if not send that the argument is not int
        """

        

        if self.is_owner(ctx.message.author):
            # convert arg to int
            try:
                arg1 = int(arg1)
            except Exception as e:
                await ctx.send(f"The argument {arg1} has some problems (is not a number) \n{e}")
                return

            self.reload_extension_list()
            extension_to_reload = self.extensions_list[arg1]

            try:
                await self.reload_extension(extension_to_reload)
                success_string = f"Extension {extension_to_reload} succesfull reloaded"

                print(success_string)
                await ctx.send(success_string)

            except Exception as e:
                print("Couldn't reload because of", e)
            extension_to_reload = self.extensions_list[arg1]
            await self.reload_extension(extension_to_reload)

        else:
            await ctx.send("you are not the **owner**, so can't use the command")





    @commands.command(name="list_extensions", aliases = ["ls"], description="lists extensions loaded in the bot")
    async def list_extensions(self, ctx):
        """
        The commamd only works if user is Channel owner
        """
        # get user role
        message_author = ctx.message.author

        if self.is_owner(message_author):

            self.reload_extension_list()

            await ctx.send(f'Loaded extensions are:\n {self.extensions_string}')


        else:
            await ctx.send("you are not the **owner**, so can't use the command")


    async def reload_extension(self, extension_to_reload):

        await self.bot.unload_extension(extension_to_reload)
        await self.bot.load_extension(extension_to_reload)

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send(f"hello {ctx.author.mention}")



    def reload_extension_list(self):
        # get extension list
        self.extensions_list = list(self.bot.extensions.keys())

        # converts Convert ["apple", "banana"] to 
        # "0) apple \n 1) banana"
        self.extensions_string = "\n".join(f"{i}) {fruit}" for i,fruit in enumerate(self.extensions_list))


    def  is_owner(self, message_author):
        """
        returns true if mesage author has owner role
        else: false
        """
        roles = [role.name for role in message_author.roles]

        # check if user is Owner
        if "Owner" in roles:
            return True
        return False 

async def setup(bot):
    await bot.add_cog(Reload(bot))
