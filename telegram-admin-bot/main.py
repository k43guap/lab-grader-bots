from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import executor

from core import States, bot
from core.keyboards import keyboard
from states import dispatcher
from core.models import AuthorizedStudent
from lab_grader_client.models import NonAuthorizedStudent


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: Message) -> None:
    await message.answer(
        'Это бот для преподавателей ГУАП для контроля корректной регистрации студентов в suai-client-bot',
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer('Здесь будут появляться сообщения с информацией о регистрации студентов')
    await States.logged_in.set()


@dispatcher.message_handler(state=None)
async def set_default_state(message: Message) -> None:
    await process_start_command(message)


@dispatcher.message_handler(state=States.logged_in)
async def get_auth_message(message: Message, state: FSMContext) -> None:
    authorized_student = AuthorizedStudent(
        fullname='Бондаренко Константин Андреевич',
        github_username='Gost',
        group='4936',
        course_names=['ОС'],
        email='mail.ru',
    )
    async with state.proxy() as data:
        data['fullname'] = authorized_student.fullname
        data['github_username'] = authorized_student.github_username
        data['group'] = authorized_student.group
        data['course_name'] = authorized_student.course_names
        data['email'] = authorized_student.email
    auth_message = await message.answer(authorized_student.to_message(), reply_markup=keyboard.inline_edit_menu)
    message_id = auth_message['message_id']



async def shutdown(dp: Dispatcher) -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_shutdown=shutdown)
