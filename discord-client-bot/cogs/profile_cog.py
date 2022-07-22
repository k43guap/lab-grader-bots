from discord import Interaction, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View

from core import bot
from core.models import AuthorizedStudent
from core.components.utils import generate_courses_view


async def unpin_all_messages(channel):
    pins = await channel.pins()
    for message in pins:
        await message.unpin()


async def send_course(ctx: commands.Context, course: str):
    await ctx.send(f'Вы выбрали курс: {course}')


class Profile(commands.Cog, name="Profile"):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def profile(self, ctx: commands.Context):
        async def add_course_button_callback(inter: Interaction):
            await inter.response.edit_message(content='Введите название курса, который хотите добавить: ', view=None)

            def check(msg):
                return msg.author == ctx.author

            new_course = (await bot.wait_for('message', check=check)).content
            channel = ctx.channel
            pinned_message = (await channel.pins())[0]
            student_info = AuthorizedStudent.from_message(pinned_message.content)
            student_info.course_names.append(new_course)

            auth_message = await ctx.send(student_info.to_message())
            await unpin_all_messages(channel)
            await auth_message.pin(reason='Student info')

            await inter.followup.send('Курс добавлен')

        channel = ctx.channel
        pinned_message = (await channel.pins())[0]
        courses = AuthorizedStudent.from_message(pinned_message.content).course_names

        if not await ctx.channel.pins():
            await ctx.send('Вам нужно зарегистрироваться - \'.start\'')
            return

        async def check_lab_button_callback(inter: Interaction):
            await inter.response.edit_message(
                content='Выберите курс, в ктором хотите проверить лабу',
                view=generate_courses_view(courses)
            )

        add_course_button = Button(label='Добавить курс', style=ButtonStyle.danger, emoji='➕')

        check_lab_button = Button(label='Проверить лабу в курсе', style=ButtonStyle.green, emoji='🔍')

        add_course_button.callback = add_course_button_callback
        check_lab_button.callback = check_lab_button_callback

        view = View()
        view.add_item(add_course_button)
        view.add_item(check_lab_button)

        await ctx.send('Здесь вы можете проверить лабу или добавить курс', view=view)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Profile cog is loaded')


def setup(client: commands.Bot):
    bot.add_cog(Profile(client))
