import random

import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands

from ..database import fetch_last_fish_collection_difference, fetch_leaderboard, fetch_total_fish_cakes
from ..database import add_fish_cakes, subtract_fish_cakes
from ..database import NoDataFetchedError, QueryNotExecutedException

from ..ui import BetUpDownView

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None



    def randomly_return_up_or_down(self, times: int):
        up_down_string = ""
        for _ in range(times): 
            up_down_string += random.choice(["⬇", "⬆"])

        return up_down_string

    @app_commands.command(name="balance")
    async def balance(self, interaction: discord.Interaction):
        if interaction.channel_id != self.bot.fish_cake_bets_channel_id:
            await interaction.response.send_message(f"you are not in {self.bot.fish_cake_bets_channel.mention}", ephemeral=True)
            return

        user_id = interaction.user.id
        total_fish_cake = fetch_total_fish_cakes(conn=self.bot.conn, user_id=user_id)
        await interaction.response.send_message(f"you have {total_fish_cake} 🍥")

    @app_commands.command(name="collect")
    async def collect(self, interaction: discord.Interaction):
        if interaction.channel_id != self.bot.fish_cake_bets_channel_id:
            await interaction.response.send_message(f"you are not in {self.bot.fish_cake_bets_channel.mention}", ephemeral=True)
            return


        user_id = interaction.user.id
        last_collection_till_now = fetch_last_fish_collection_difference(conn=self.bot.conn, user_id=user_id, update_collection_time=True) # in seconds

        cake_to_add = round(last_collection_till_now * 39) 
        add_fish_cakes(conn=self.bot.conn, user_id=user_id, fish_cakes_to_add=cake_to_add)
        users_total_fish_cake = fetch_total_fish_cakes(conn= self.bot.conn, user_id=user_id)

        await interaction.response.send_message(f"you have collected {cake_to_add}, currently you have {users_total_fish_cake} 🍥")

    @app_commands.command(name="bet")
    async def bet(self, interaction: discord.Interaction, bet_amount: int):
        if interaction.channel_id != self.bot.fish_cake_bets_channel_id:
            await interaction.response.send_message(f"you are not in {self.bot.fish_cake_bets_channel.mention}", ephemeral=True)
            return

        author_id = interaction.user.id

        user_balance = fetch_total_fish_cakes(conn=self.bot.conn, user_id=author_id)

        if (user_balance - bet_amount) >= 0:
            previous_five_prediction: str = self.randomly_return_up_or_down(times=5)
            correct_bet = self.randomly_return_up_or_down(times=1)
            print(correct_bet)
            await interaction.response.send_message(f"Predict the next \n the previous 5  were \n {previous_five_prediction}", view=BetUpDownView(database_conn=self.bot.conn, user_id=author_id, bet_amount=bet_amount, correct_bet=correct_bet, user_balance=user_balance), ephemeral=True)
            # TODO: add betting mechanis witj ui
        else:
            embed = Embed(title="Insufficient-balance", description=f"you missing {(bet_amount - user_balance):,} 🍥", color=0x0000ff)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return



    @app_commands.command(name="give")
    async def give(self, interaction: discord.Interaction, user_to_give: discord.Member, amount: int):

        author_id = interaction.user.id
        user_to_give_id = user_to_give.id

        user_balance = fetch_total_fish_cakes(conn=self.bot.conn, user_id=author_id)

        if (user_balance - amount) >= 0:
            try: 
                add_fish_cakes(conn=self.bot.conn, user_id=user_to_give_id, fish_cakes_to_add=amount)
                await interaction.response.send_message("🍥 sent")

            except QueryNotExecutedException:
                # reutrn back

                await interaction.response.send_message("User {user_to_give.name} has not joined fish cake, you can ask tuem to join here and start the cake magic 🍥")
                return
            except Exception as e:
                await interaction.response.send_message("an error occured")
            subtract_fish_cakes(conn=self.bot.conn, user_id=author_id, fish_cakes_to_subtract=amount)
            return


        else:
            embed = Embed(title="Insufficient-balance", description=f"you are missing {(bet_amount - user_balance):,} 🍥", color=0x0000ff)
            await interaction.response.send_message(embed=embed)
            return




    @app_commands.command(name="leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        if interaction.channel_id != self.bot.fish_cake_bets_channel_id:
            await interaction.response.send_message(f"you are not in {self.bot.fish_cake_bets_channel.mention}", ephemeral=True)
            return

        leaderbard = fetch_leaderboard(conn=self.bot.conn)
        await interaction.response.send_message("```" + leaderbard + "```")

    

async def setup(bot):
    await bot.add_cog(Economy(bot))
