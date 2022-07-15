from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from core import bot
from core.keyboards import keyboard


def generate_labs_markup(labs_list: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup().add(*[InlineKeyboardButton(lab, callback_data=labs_list[lab]) for lab in labs_list])
    return markup


def generate_courses_markup(courses_list: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for course in courses_list:
        markup.row(KeyboardButton(course))
    return markup.add(keyboard.back_button)


async def get_pinned_message(chat_id: int) -> Message:
    chat = await bot.get_chat(chat_id)
    return chat.pinned_message
