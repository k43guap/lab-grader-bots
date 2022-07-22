from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from api_clients import lab_grader_client
from core import bot
from core.keyboards import keyboard
from core.models import AuthorizedStudent


def generate_labs_markup(labs: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for lab in labs:
        markup.row(KeyboardButton(lab))
    return markup.add(keyboard.back_button)


def generate_inline_labs_markup(labs_list: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup().add(*[InlineKeyboardButton(lab, callback_data=lab) for lab in labs_list])
    return markup


def generate_courses_markup(courses: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for course in courses:
        markup.row(KeyboardButton(course))
    return markup.add(keyboard.back_button)


async def get_pinned_message(chat_id: int) -> Message:
    chat = await bot.get_chat(chat_id)
    return chat.pinned_message


async def get_labs(chat_id: int, course: str, authorized_student: AuthorizedStudent) -> list:
    labs = await lab_grader_client.grader_api.get_laboratory_works(
        str(chat_id),
        course,
        authorized_student,
    )
    lab_names = []
    for lab in labs.values():
        lab_names.append(lab.short_name)
    return lab_names
