import os
import asyncio
import sys

from dotenv import load_dotenv

from denzel import Denzel
"""
Scuipt is used to run the bot locally for debugging
"""

load_dotenv()
BOT_TOKEN = sys.argv[1]
bot = Denzel(COMMAND_PREFIX="!")
bot.run(BOT_TOKEN)

