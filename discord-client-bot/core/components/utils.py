from discord.ui import Button, View
from discord import ButtonStyle, Interaction


async def course_button_callback(inter: Interaction):
    await inter.response.edit_message(
        content='Здесь я отправляю курс на бэк',
        view=None
    )


def generate_courses_view(courses: list) -> View:
    view = View()
    for course in courses:
        button = Button(style=ButtonStyle.primary, label=f'{course}')
        button.callback = course_button_callback
        view.add_item(button)
    return view
