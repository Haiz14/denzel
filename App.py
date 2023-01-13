import os
import asyncio

from dotenv import load_dotenv

from denzel import Denzel
"""
Scuipt is used to run the bot locally for debugging
"""

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Denzel(COMMAND_PREFIX="!")
bot.run(BOT_TOKEN)

