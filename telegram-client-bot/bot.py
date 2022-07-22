import logging

from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram.utils import executor

from core.middlewares import AuthMiddleware
from states import dispatcher

logging.basicConfig(level=logging.INFO)


@dispatcher.message_handler(state=None)
async def set_default_state(message: Message) -> None:
    pass


async def bot_shutdown(dp: Dispatcher) -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()


def bot_configure() -> None:
    dispatcher.middleware.setup(LoggingMiddleware())
    dispatcher.middleware.setup(AuthMiddleware())
    executor.start_polling(dispatcher, on_shutdown=bot_shutdown)


if __name__ == '__main__':
    bot_configure()
