from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor

from core import States
from core.keyboards import keyboard
from states import dispatcher


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: Message) -> None:
    await message.answer('Это бот для студентов ГУАП и нам нужны ваши данные', reply_markup=keyboard.auth_menu)
    await States.auth.set()


@dispatcher.message_handler(state=None)
async def set_default_state(message: Message) -> None:
    await States.auth.set()
    await process_start_command(message)


async def shutdown(dp: Dispatcher) -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_shutdown=shutdown)
