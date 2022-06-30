from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import get_settings


class States(StatesGroup):
    auth = State()
    select_lab = State()
    select_course = State()
    main_menu = State()
    profile = State()
    add_course = State()
    change_github = State()


bot = Bot(token=get_settings().API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())
