import discord
from discord.ext import commands

class ModerationCog(commands.Cog):

    """
    
    ROLE_CHANNEL_ID = 
    FIRST_MESSAGE_ID = 
    ROLE_ID = 
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if the reaction is a 💤 emoji
        if payload.emoji.name == "💤":
            # Check if the reaction is in the "roles" channel and is on the first message
            print('emoji entered')
            if payload.channel_id == "1060544257225674752 "and payload.message_id == "1060547841166155828":
                # Get the guild and user from the payload
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                # Get the role from the guild
                print('going to aff role')
                role = guild.get_role("1060551694976557157")
                print('found the role')
                # Add the role to the user
                await user.add_roles(role)
                print('added the role')

    
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        whenever "denzel" is written in any channel, it will reply "yes sir denzel is online"
        """
            # Don't respond to ourselves
        if message.author == self.bot.user:
            return

        if message.content.startswith('denzel'):
            await message.channel.send('Yes sir! denzel is online')

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))


