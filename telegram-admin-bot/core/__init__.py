import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import get_settings


class States(StatesGroup):
    logged_in = State()
    edit_data = State()


bot = Bot(token=get_settings().API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)
