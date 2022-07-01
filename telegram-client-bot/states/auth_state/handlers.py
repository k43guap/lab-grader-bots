from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from api_clients import lab_grader_client
from core import bot, dispatcher, States
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


@dispatcher.message_handler(state=States.auth)
async def start_login(message: Message) -> None:
    await message.answer("Введите ваши данные")
    await message.answer("Введите вашу фамилию:")
    await LoginForm.lastname.set()


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
            await message.answer('Вы успешно зашли!')

            authorized_student = AuthorizedStudent(
                fullname=student_response.fullname,
                github_username=student_response.github_username,
                group=student_response.group,
                courses=[data['course_name']],
            )
            auth_message = await message.answer(authorized_student.to_message())
            message_id = auth_message['message_id']
            await bot.pin_chat_message(message.chat.id, message_id)

            await States.main_menu.set()
        except UnexpectedResponse as e:
            await message.answer('Произошла ошибка!')
            await message.answer('\n'.join(parse_unexpected_exception(e)))
            await States.auth.set()
            await start_login(message)
