from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor

from core import States
from states import dispatcher
from states.auth_state.handlers import start_login


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: Message) -> None:
    await States.auth.set()
    await start_login(message)


@dispatcher.message_handler(state=None)
async def set_default_state(message: Message) -> None:
    await States.auth.set()
    await start_login(message)  # fixme


async def shutdown(dp: Dispatcher) -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_shutdown=shutdown)
