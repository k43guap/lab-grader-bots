import logging
import os
from config import get_settings
from core import bot

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('ID:', bot.user.id)


if __name__ == '__main__':
    for folder in os.listdir("cogs"):
        if folder.endswith('.py') and not folder.startswith('_'):
            bot.load_extension(f"cogs.{folder[:-3]}")
    bot.run(get_settings().API_TOKEN)
