from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from core import bot, dispatcher
from core.keyboards import keyboard
from core.models import AuthorizedStudent
from core.states import States
from states.menu_state.utils import (
    generate_courses_markup,
    generate_labs_markup,
    get_labs,
)


class MenuStates(StatesGroup):
    select_course = State()
    select_lab = State()
    wait_for_check = State()


@dispatcher.message_handler(content_types=['text'], text='Проверить лабу в курсе 🔍', state=States.main_menu)
async def check_lab(message: Message, student: AuthorizedStudent) -> None:
    courses = student.course_names
    await message.answer('Выберите курс 📚', reply_markup=generate_courses_markup(courses))
    await MenuStates.select_course.set()


@dispatcher.message_handler(content_types=['text'], text='Назад ⬅', state='*')
async def back_to_menu(message: Message) -> None:
    await message.answer('Главное меню 🎈', reply_markup=keyboard.main_menu)
    await States.main_menu.set()


@dispatcher.message_handler(state=MenuStates.select_course)
async def select_course(message: Message, state: FSMContext, student: AuthorizedStudent) -> None:
    async with state.proxy() as data:
        data['selected_course'] = message.text
    selected_course = data['selected_course']
    chat_id = message.chat.id
    labs = await get_labs(selected_course, student)
    await MenuStates.select_lab.set()
    await select_lab(chat_id, labs)


@dispatcher.message_handler(state=MenuStates.select_lab)
async def select_lab(chat_id: int, labs: list) -> None:
    await bot.send_message(chat_id, 'Выберите работу 🔍', reply_markup=generate_labs_markup(labs))
    await MenuStates.wait_for_check.set()


@dispatcher.message_handler(state=MenuStates.wait_for_check)
async def process_lastname(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['selected_lab'] = message.text
    await message.answer(f"Проверяем работу №{data['selected_lab']}", reply_markup=keyboard.main_menu)
    await States.main_menu.set()
