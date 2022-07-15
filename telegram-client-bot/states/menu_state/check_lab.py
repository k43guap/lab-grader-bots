from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from core import bot, dispatcher, States
from core.keyboards import keyboard
from core.models import AuthorizedStudent
from states.menu_state.utils import generate_courses_markup, generate_labs_markup, get_pinned_message


class MenuStates(StatesGroup):
    select_course = State()
    select_lab = State()
    wait_for_check = State()


@dispatcher.message_handler(content_types=['text'], text='Проверить лабу в курсе 🔍', state=States.main_menu)
async def check_lab(message: Message) -> None:
    pinned_message = await get_pinned_message(message.chat.id)
    courses = AuthorizedStudent.from_message(pinned_message['text']).courses
    await message.answer('Выберите курс 📚', reply_markup=generate_courses_markup(courses))
    await MenuStates.select_course.set()


@dispatcher.message_handler(content_types=['text'], text='Назад ⬅', state=MenuStates.select_course)
async def back_to_menu(message: Message) -> None:
    await message.answer('Главное меню 🎈', reply_markup=keyboard.main_menu)
    await States.main_menu.set()


@dispatcher.message_handler(state=MenuStates.select_course)
async def select_course(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['selected_course'] = message.text
    pinned_message = await get_pinned_message(message.chat.id)
    authorized_student = AuthorizedStudent.from_message(pinned_message['text'])
    # fixme: get labs here
    await MenuStates.select_lab.set()
    # fixme: select_course(labs_list)


@dispatcher.message_handler(state=MenuStates.select_lab)
async def select_lab(labs_list: list) -> None:
    await bot.send_message('Выберите работу 🔍', reply_markup=generate_labs_markup(labs_list))
    await MenuStates.wait_for_check.set()
