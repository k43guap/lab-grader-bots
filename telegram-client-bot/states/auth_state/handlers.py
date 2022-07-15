from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from api_clients import lab_grader_client
from core import bot, dispatcher, States
from core.keyboards import keyboard
from core.models import AuthorizedStudent
from core.utils import parse_unexpected_exception
from lab_grader_client.exceptions import UnexpectedResponse
from lab_grader_client.models import NonAuthorizedStudent


class LoginForm(StatesGroup):
    lastname = State()
    firstname = State()
    patronymic = State()
    group = State()
    github_username = State()
    email = State()
    course_name = State()


start_registration = CallbackData('start_registration')
send_report_callback = CallbackData('send_report')


@dispatcher.callback_query_handler(start_registration.filter(), state=States.auth)
async def start_login(callback_query: CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите вашу фамилию:", reply_markup=ReplyKeyboardRemove())
    await LoginForm.lastname.set()


@dispatcher.callback_query_handler(send_report_callback.filter(), state=States.auth)
async def send_report(callback_query: CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Мы сообщили преподавателю о вашей проблеме")
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard.auth_menu,
    )


@dispatcher.message_handler(state=LoginForm.lastname)
async def process_lastname(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['lastname'] = message.text
    await message.answer("Введите ваше имя:")
    await LoginForm.firstname.set()


@dispatcher.message_handler(state=LoginForm.firstname)
async def process_firstname(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['firstname'] = message.text
    await message.answer("Введите ваше отчество:")
    await LoginForm.patronymic.set()


@dispatcher.message_handler(state=LoginForm.patronymic)
async def process_patronymic(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['patronymic'] = message.text
    await message.answer("Введите вашу группу:")
    await LoginForm.group.set()


@dispatcher.message_handler(state=LoginForm.group)
async def process_group(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['group'] = message.text
    await message.answer("Введите ваш никнейм в Github:")
    await LoginForm.github_username.set()


@dispatcher.message_handler(state=LoginForm.github_username)
async def process_github_username(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['github_username'] = message.text
    await message.answer("Введите ваш email:")
    await LoginForm.email.set()


@dispatcher.message_handler(state=LoginForm.email)
async def process_email(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Введите название курса:")
    await LoginForm.course_name.set()


@dispatcher.message_handler(state=LoginForm.course_name)
async def process_course_name(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['course_name'] = message.text
        data['fullname'] = f"{data['lastname']} {data['firstname']} {data['patronymic']}"
        student = NonAuthorizedStudent(**data)
        try:
            student_response = await lab_grader_client.authorization_api.login(student)
            await message.answer('Вы успешно зашли!', reply_markup=keyboard.main_menu)

            authorized_student = AuthorizedStudent(
                fullname=student_response.fullname,
                github_username=student_response.github_username,
                group=student_response.group,
                courses=[data['course_name']],
            )
            auth_message = await message.answer(authorized_student.to_message())
            message_id = auth_message['message_id']
            await bot.unpin_all_chat_messages(message.chat.id)
            await bot.pin_chat_message(message.chat.id, message_id)

            await States.main_menu.set()

        except UnexpectedResponse as e:
            await message.answer('Произошла ошибка!')
            exceptions = parse_unexpected_exception(e)
            await message.answer('\n'.join(exceptions))
            await message.answer(
                'Попробуйте ещё раз или сообщите преподавателю об ошибке',
                reply_markup=keyboard.failed_auth_menu,
            )
            await States.auth.set()
