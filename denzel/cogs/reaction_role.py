import discord
from discord.ext import commands
from ..database import create_new_user, UserExistsError


class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # if reaction is not on role message return
        if payload.message_id != 1062994674085797908: 
            
            return

        # get guold and member

        if payload.emoji.name == "🍥":
            await self.add_role( role_name = "fish_cake", payload=payload)

            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            try:
                create_new_user( conn= self.bot.conn, user_id = member.id, user_name=member.name)
                await self.bot.bot_channel.send(f"{member.mention} !you got 5000 fishcakes, continue your adventure in #fish-cake-bets")

            except UserExistsError:
                await self.bot.bot_channel.send(f"{member.mention} !you alread got your first  5000 🍥, you womt get anore of these delicious cakes, rather do `!collect` to collect your secondly income of 39🍥 a second in #fish-cake-bets")


        elif payload.emoji.name == "🅰️": 

            await self.add_role( role_name = "Admin", payload=payload)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        # if reaction is not on role message return
        if payload.message_id != 1062994674085797908: 
            
            return

        # get guold and member

        if payload.emoji.name == "🍥":
            await self.remove_role( role_name = "fish_cake", payload=payload)

        elif payload.emoji.name == "🅰️": 

            await self.remove_role( role_name = "Admin", payload=payload)

    async def add_role(self, role_name, payload):

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        role = discord.utils.get(guild.roles, name=role_name)
        try:
            await member.add_roles(role)
            await self.bot.bot_channel.send(f"{member.mention}  got {role_name} role")
        except Exception as e:
            await bot.bot_channel.send(f"error couldn't add role cause ```{e}```")
            
    async def remove_role(self, role_name, payload):

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        role = discord.utils.get(guild.roles, name=role_name)
        try:
            await member.remove_roles(role)
            await self.bot.bot_channel.send(f"{member.mention} left {role_name} role")
        except Exception as e:
            await bot.bot_channel.send(f"error couldn't remove role cause ```{e}```")
            



async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
