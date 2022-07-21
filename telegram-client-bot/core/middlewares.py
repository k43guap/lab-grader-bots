from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, ReplyKeyboardRemove

from core.keyboards import keyboard
from core.models import AuthorizedStudent
from core.states import States
from states.auth_state.handlers import LoginForm
from states.menu_state.utils import get_pinned_message


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict) -> None:
        dispatcher = Dispatcher.get_current()
        state = await dispatcher.current_state().get_state()
        if state and self.__is_login_form(state):
            return
        try:
            pinned_message = await get_pinned_message(message.chat.id)
            student = AuthorizedStudent.from_message(pinned_message['text'])
        except:  # noqa
            await message.answer('Это бот для студентов ГУАП', reply_markup=ReplyKeyboardRemove())
            await message.answer('📝 Для начала нужно пройти регистрацию 📝', reply_markup=keyboard.auth_menu)
            await States.auth.set()
            raise CancelHandler()
        else:
            data['student'] = student
            if not state or self.__is_auth_state(state):
                await message.answer('Главное меню 🎈', reply_markup=keyboard.main_menu)
                await States.main_menu.set()
                raise CancelHandler()

    def __is_login_form(self, state: str) -> bool:
        return str(LoginForm()) in state

    def __is_auth_state(self, state: str) -> bool:
        return state == 'States:auth'
