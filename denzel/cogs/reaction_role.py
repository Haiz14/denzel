import discord
from discord.ext import commands


class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "🍥":
            print("it is fish cake")
        if payload.message_id == 1062994674085797908:
            print('role message id')
        else: print('not role message id')
        return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name="fish_cake")
        await member.add_roles(role)


async def setup(bot):
    await bot.add_cog(ReactionRole(bot))
