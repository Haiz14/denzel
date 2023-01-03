import os

from discord import Intents
from dotenv import load_dotenv

from denzel import Denzel

"""
Script is used to run the bot locally for debugging
"""

def run_bot(BOT_TOKEN):
    
    intents = Intents.default()
    intents.message_content = True

    bot = Denzel(command_prefix = '!', intents=intents)
    bot.run(BOT_TOKEN)
def main():
    
    # load bot token
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    run_bot(BOT_TOKEN)
    
if __name__ == "__main__":
    main()
