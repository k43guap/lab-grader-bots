from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


register_button = InlineKeyboardButton('Зарегистрироваться', callback_data='start_registration')
profile_button = KeyboardButton('Профиль 🚀')
check_labs_button = KeyboardButton('Проверить лабу в курсе 🔍')
back_button = KeyboardButton('Назад')


auth_menu = InlineKeyboardMarkup().add(register_button)
home_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(check_labs_button).add(profile_button)
labs_menu = ReplyKeyboardMarkup(resize_keyboard=True)
profile_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)
