from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core import bot, dispatcher
from core.keyboards import keyboard
from core.models import AuthorizedStudent
from core.states import States


@dispatcher.message_handler(content_types=['text'], text='Профиль 🚀', state=States.main_menu)
async def check_lab(message: Message) -> None:
    await message.answer('Ваш профиль 🚀', reply_markup=keyboard.profile_menu)
    await States.profile.set()


@dispatcher.message_handler(content_types=['text'], text='Назад ⬅', state=States.profile)
async def back_to_menu(message: Message) -> None:
    await message.answer('Главное меню 🎈', reply_markup=keyboard.main_menu)
    await States.main_menu.set()


@dispatcher.message_handler(content_types=['text'], text='Добавить курс ➕', state=States.profile)
async def add_course(message: Message, state: FSMContext) -> None:
    await message.answer('Введите имя курса, который хотите добавить')
    await States.add_course.set()


@dispatcher.message_handler(state=States.add_course)
async def get_course(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['course'] = message.text
    chat_id = message.chat.id
    chat = await bot.get_chat(chat_id)
    pinned_message = chat.pinned_message
    student_info = AuthorizedStudent.from_message(pinned_message['text'])
    student_info.course_names.append(data['course'])

    auth_message = await message.answer(student_info.to_message())
    message_id = auth_message['message_id']
    await bot.unpin_all_chat_messages(message.chat.id)
    await bot.pin_chat_message(message.chat.id, message_id)

    await message.answer('Курс добавлен', reply_markup=keyboard.profile_menu)
    await States.profile.set()
