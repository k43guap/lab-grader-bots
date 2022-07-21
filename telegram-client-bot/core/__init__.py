from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config import get_settings

bot = Bot(token=get_settings().API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
