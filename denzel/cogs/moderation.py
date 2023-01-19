import asyncio
from typing import Optional
import datetime

import discord
from discord import app_commands
from discord.ext import commands


class ModerationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="mute")
    async def mute(self, interaction: discord.Interaction , member_to_ban: discord.Member, seconds: int, reason: Optional[str] = None):
        author = interaction.user
        if self.has_role(role_name = "Admin", message_author = author) == False: 
            await interaction.response.send_message("you dont have **Admin** role, so, cant use the command", ephemeral=True)

            return

        timeout_until = discord.utils.utcnow()+ datetime.timedelta(seconds=seconds)

        await member_to_ban.timeout(timeout_until, reason=reason)
        await interaction.response.send_message(f"{member_to_ban} has been muted for {seconds} seconds", ephemeral=True)

        await member_to_ban.send(f"you have been banned for {reason} till {seconds} seconds")
        await asyncio.sleep(seconds)

        await self.bot.bot_channel.send(f"{member_to_ban.mention} has been unmuted  \n muted by: {author.mention}")



        
        await self.bot.bot_channel.send(f"{member.mention} has been unmuted {author.mention}  ")


    @commands.command(name="kick", description="to kick user type `!kick @user`")
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if self.has_role(role_name = "Admin", message_author = ctx.author) == False: 
            ctx.send("you dont have **Admin** role")
            return

        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked by {ctx.author.mention} for {reason}')

    @commands.command(name= "ban", description="bans user type `!ban @user`")
    async def ban(self, ctx, member: discord.Member, *, reason=None, delete_message_days=0):

        if self.has_role(role_name = "Admin", message_author = ctx.author) == False: 
            await ctx.send("you dont have **Admin** role")
            return

        await member.ban(reason=reason, delete_message_days=delete_message_days)

        await ctx.send(f'{member} has been banned from the server')

    @commands.command()
    async def kicki(self, ctx):
        await ctx.send("kicki is kicking")

    def has_role(self, role_name,  message_author):
        """
        returns true if mesage author has owner role
        else: false
        """
        roles = [role.name for role in message_author.roles]

        # check if user is Owner
        if role_name in roles:
            return True
        return False 

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))

