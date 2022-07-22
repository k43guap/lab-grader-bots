from discord.ext import commands

from api_clients import lab_grader_client
from core import bot
from core.components import buttons
from core.models import AuthorizedStudent
from core.utils import parse_unexpected_exception
from lab_grader_client.exceptions import UnexpectedResponse
from lab_grader_client.models import NonAuthorizedStudent


async def unpin_all_messages(channel):
    pins = await channel.pins()
    for message in pins:
        await message.unpin()


class Auth(commands.Cog, name="Auth"):

    def __init__(self, client: commands.Bot):
        self.client = client

    # @commands.Cog.listener()
    @classmethod
    async def register(cls, ctx):
        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        data = {}

        data['lastname'] = (await bot.wait_for('message', check=check)).content
        await ctx.channel.send('Введите выше имя: ')
        data['firstname'] = (await bot.wait_for('message', check=check)).content
        await ctx.channel.send('Введите выше отвечство: ')
        data['patronymic'] = (await bot.wait_for('message', check=check)).content
        await ctx.channel.send('Введите вашу группу: ')
        data['group'] = (await bot.wait_for('message', check=check)).content
        await ctx.channel.send('Введите ваш никнейм в Github:')
        data['github_username'] = (await bot.wait_for('message', check=check)).content
        await ctx.channel.send('Введите ваш email: ')
        data['email'] = (await bot.wait_for('message', check=check)).content
        await ctx.channel.send('Введите ваш курс: ')
        data['course_name'] = (await bot.wait_for('message', check=check)).content
        data['fullname'] = f"{data['lastname']} {data['firstname']} {data['patronymic']}"
        student = NonAuthorizedStudent(**data)

        try:
            student_response = await lab_grader_client.authorization_api.login(student)
            await ctx.send('Вы успешно зашли!')

            authorized_student = AuthorizedStudent(
                fullname=student_response.fullname,
                github_username=student_response.github_username,
                group=student_response.group,
                course_names=[data['course_name']],
                email=data['email'],
            )

            auth_message = await ctx.send(authorized_student.to_message())
            await unpin_all_messages(ctx.channel)
            await auth_message.pin(reason='Student info')

        except UnexpectedResponse as e:
            await ctx.send('Произошла ошибка!')
            exceptions = parse_unexpected_exception(e)
            await ctx.send('\n'.join(exceptions))
            await ctx.send('Попробуйте начать заново - \'.start\'',)

    @commands.command()
    async def start(self, ctx: commands.Context):
        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        if await ctx.channel.pins():
            await ctx.send('Вы уже зарегистрированы')
            return
        await ctx.send('Это бот для студентов ГУАП\n '
                       'Для начала нужно зарегистрироваться',
                       components=buttons.auth_buttons)
        interaction = await self.client.wait_for('button_click', check=check)
        if interaction.channel == ctx.channel:
            if interaction.component.label == 'Зарегистрироваться':
                await interaction.send(content='Введите вашу фамилию: ', ephemeral=False)
                await Auth.register(ctx)
            else:
                await interaction.respond('Мы отправили сообщение об ошибке', ephemeral=False)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Auth cog is loaded')


def setup(client: commands.Bot):
    bot.add_cog(Auth(client))
