from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData


edit_data_button = InlineKeyboardButton('Редактировать данные', callback_data='edit_data')
show_data_button = InlineKeyboardButton('Добавить студента', callback_data='show_data')
skip_button = KeyboardButton('Пропустить')

inline_edit_menu = InlineKeyboardMarkup().add(edit_data_button)
show_data_menu = InlineKeyboardMarkup().add(show_data_button)
edit_data_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(skip_button)


start_edit_callback = CallbackData('edit_data')
show_data_callback = CallbackData('show_data')
