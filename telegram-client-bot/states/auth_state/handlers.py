from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from api_clients import lab_grader_client
from core import dispatcher, States
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
    await message.reply("Введите ваше имя:")
    await LoginForm.firstname.set()


@dispatcher.message_handler(state=LoginForm.firstname)
async def process_firstname(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['firstname'] = message.text
    await message.reply("Введите ваше отчество:")
    await LoginForm.patronymic.set()


@dispatcher.message_handler(state=LoginForm.patronymic)
async def process_patronymic(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['patronymic'] = message.text
    await message.reply("Введите вашу группу:")
    await LoginForm.group.set()


@dispatcher.message_handler(state=LoginForm.group)
async def process_group(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['group'] = message.text
    await message.reply("Введите ваш никнейм в Github:")
    await LoginForm.github_username.set()


@dispatcher.message_handler(state=LoginForm.github_username)
async def process_github_username(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['github_username'] = message.text
    await message.reply("Введите ваш email:")
    await LoginForm.email.set()


@dispatcher.message_handler(state=LoginForm.email)
async def process_email(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['email'] = message.text
    await message.reply("Введите название курса:")
    await LoginForm.course_name.set()


@dispatcher.message_handler(state=LoginForm.course_name)
async def process_course_name(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['course_name'] = message.text
        data['fullname'] = f"{data['lastname']} {data['firstname']} {data['patronymic']}"
        result = await lab_grader_client.authorization_api.login(NonAuthorizedStudent(**data))
        await message.reply(result)
        await States.main_menu.set()
