# for typing
import sqlite3

import discord
from discord import Embed
from ..database import add_fish_cakes, subtract_fish_cakes


class BetUpDownView(discord.ui.View):
    """
    before inititalisng check if user has sufficient balance
    """
    def __init__(self, database_conn: sqlite3.Connection, user_id: int, bet_amount: int, correct_bet: str, user_balance: int):
        super().__init__()

        self.database_conn: sqlite3.Connection = database_conn
        self.user_id: int = user_id
        self.bet_amount: int = bet_amount
        self.correct_bet: str = correct_bet
        self.user_balance: int = user_balance

        self.bet_value: str = None

    @discord.ui.button(label='up ⬆', style=discord.ButtonStyle.blurple)
    async def high(self, interaction: discord.Interaction, button: discord.ui.Button):

        self.bet_value = "⬆"
        await self.handle_bet(button_interaction=interaction)
        
        
        self.stop()

    @discord.ui.button(label='down ⬇', style=discord.ButtonStyle.blurple)
    async def low(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bet_value = "⬇"
        await self.handle_bet(button_interaction=interaction)
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message( "you cancelled the bet", ephemeral=True)
        self.bet_cancelled = True
        self.stop()


    async def handle_bet(self,  button_interaction: discord.Interaction):
        """
        subtracts the bet valie and sends appropriate message
        """
        print('in ui')
        print("correct bert:", self.correct_bet)
        if self.bet_value == self.correct_bet: await self.handle_winnings(button_interaction) 
        else: await self.handle_loss(button_interaction)


    async def handle_winnings(self, button_interaction: discord.Interaction):

        """
        adds the bet valie and sends appropriate message
        """
        add_fish_cakes(conn= self.database_conn, user_id=self.user_id, fish_cakes_to_add=(self.bet_amount))

        embed = Embed(title="Fish-cake-bet-won", description=f"you betted right and won {(self.bet_amount):,} 🍥, your current balance is {(self.user_balance + (self.bet_amount * 2)):,} 🍥", color=0x00ff00)
        await button_interaction.response.send_message(embed=embed)


    async def handle_loss(self, button_interaction: discord.Interaction):
        subtract_fish_cakes(conn= self.database_conn, user_id=self.user_id, fish_cakes_to_subtract=(self.bet_amount))

        embed = Embed(title="fish-cake-bet-lost", description=f"you lost {(self.bet_amount * 2):,} 🍥, your current balance is {self.user_balance - (self.bet_amount * 2):,} 🍥", color=0xff0000)
        await button_interaction.response.send_message(embed=embed)



