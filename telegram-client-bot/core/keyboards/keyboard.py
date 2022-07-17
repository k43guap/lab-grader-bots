from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData

register_button = InlineKeyboardButton('Зарегистрироваться', callback_data='start_registration')
retry_register_button = InlineKeyboardButton('Попробовать снова', callback_data='start_registration')
report_button = InlineKeyboardButton('Сообщить преподавателю', callback_data='send_report')
profile_button = KeyboardButton('Профиль 🚀')
check_labs_button = KeyboardButton('Проверить лабу в курсе 🔍')
back_button = KeyboardButton('Назад ⬅')
add_course_button = KeyboardButton('Добавить курс ➕')
send_report = KeyboardButton('Отправить запрос на изменение GitHub аккаунта ❗')

auth_menu = InlineKeyboardMarkup().add(register_button)
failed_auth_menu = InlineKeyboardMarkup().add(retry_register_button).add(report_button)
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(check_labs_button).add(profile_button)
labs_menu = ReplyKeyboardMarkup(resize_keyboard=True)
profile_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(add_course_button).add(send_report).add(back_button)

start_registration_callback = CallbackData('start_registration')
send_report_callback = CallbackData('send_report')
