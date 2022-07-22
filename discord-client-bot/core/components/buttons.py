from discord.ui import Button
from discord import ButtonStyle


auth_buttons = [[Button(label='Зарегистрироваться', style=ButtonStyle.green, emoji='✔'),
                Button(label='Сообщить об ошибке', style=ButtonStyle.grey, emoji='⚠')]]
profile_buttons = [[Button(label='Добавить курс', style=ButtonStyle.green, emoji='➕'),
                    Button(label='Проверить лабу в курсе', style=ButtonStyle.green, emoji='🔍')]]