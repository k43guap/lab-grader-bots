from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from api_clients import lab_grader_client
from core import bot, dispatcher, States
from core.keyboards import keyboard
from core.models import AuthorizedStudent
from core.utils import parse_unexpected_exception
from lab_grader_client.exceptions import UnexpectedResponse
from lab_grader_client.models import NonAuthorizedStudent


class EditForm(StatesGroup):
    fullname = State()
    group = State()
    github_username = State()
    email = State()
    course_name = State()
    end_edit = State()


@dispatcher.callback_query_handler(keyboard.start_edit_callback.filter(), state=States.logged_in)
async def start_login(callback_query: CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Введите новое ФИО студента",
        reply_markup=keyboard.edit_data_menu
    )
    await EditForm.fullname.set()


@dispatcher.message_handler(state=EditForm.group)
async def process_fullname(message: Message, state: FSMContext) -> None:
    if message.text == 'Пропустить':
        await EditForm.github_username.set()
        await message.answer("Введите новый никнейм в GitHub студента", reply_markup=keyboard.edit_data_menu)
        return
    async with state.proxy() as data:
        data['group'] = message.text
    await message.answer("Введите новый никнейм в GitHub студента", reply_markup=keyboard.edit_data_menu)
    await EditForm.github_username.set()


@dispatcher.message_handler(state=EditForm.fullname)
async def process_patronymic(message: Message, state: FSMContext) -> None:
    if message.text == 'Пропустить':
        await EditForm.group.set()
        await message.answer("Введите новую группу студента", reply_markup=keyboard.edit_data_menu)
        return
    async with state.proxy() as data:
        data['fullname'] = message.text
    await message.answer("Введите новую группу студента", reply_markup=keyboard.edit_data_menu)
    await EditForm.group.set()


@dispatcher.message_handler(state=EditForm.github_username)
async def process_github_username(message: Message, state: FSMContext) -> None:
    if message.text == 'Пропустить':
        await EditForm.email.set()
        await message.answer("Введите новую почту студента", reply_markup=keyboard.edit_data_menu)
        return
    async with state.proxy() as data:
        data['github_username'] = message.text
    await message.answer("Введите новую почту студента", reply_markup=keyboard.edit_data_menu)
    await EditForm.email.set()


@dispatcher.message_handler(state=EditForm.email)
async def process_email(message: Message, state: FSMContext) -> None:
    if message.text == 'Пропустить':
        await EditForm.course_name.set()
        await message.answer("Введите новый курс студента", reply_markup=keyboard.edit_data_menu)
        return
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Введите новый курс студента", reply_markup=keyboard.edit_data_menu)
    await EditForm.course_name.set()


@dispatcher.message_handler(state=EditForm.course_name)
async def process_course_name(message: Message, state: FSMContext) -> None:
    if message.text == 'Пропустить':
        await message.answer("Обновлённые данные", reply_markup=keyboard.show_data_menu)
        await EditForm.end_edit.set()
        return
    async with state.proxy() as data:
        data['course_name'] = message.text
    await message.answer("Обновлённые данные", reply_markup=keyboard.show_data_menu)
    await EditForm.end_edit.set()


@dispatcher.callback_query_handler(keyboard.show_data_callback.filter(), state=EditForm.end_edit)
async def start_login(callback_query: CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data['course_name'] = data['course_name'][0]
        student = NonAuthorizedStudent(**data)
        try:
            student_response = await lab_grader_client.authorization_api.login(student)
            await bot.send_message(
                callback_query.from_user.id,
                'Студент найден и добавлен',
                reply_markup=ReplyKeyboardRemove()
            )

            authorized_student = AuthorizedStudent(
                fullname=student_response.fullname,
                github_username=student_response.github_username,
                group=student_response.group,
                course_names=[data['course_name']],
                email=data['email'],
            )
            auth_message = await bot.send_message(callback_query.from_user.id, authorized_student.to_message())

            await EditForm.end_edit.set()

        except UnexpectedResponse as e:
            await bot.send_message(callback_query.from_user.id, 'Произошла ошибка!')
            exceptions = parse_unexpected_exception(e)
            await bot.send_message(callback_query.from_user.id, '\n'.join(exceptions))
