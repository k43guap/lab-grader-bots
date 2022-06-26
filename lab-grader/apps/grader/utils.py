import os

import aiofiles
import yaml

from apps.grader.models import Course
from config import Settings


async def get_courses(settings: Settings) -> list[Course]:
    courses = []
    files = os.listdir(settings.COURSES_CONFIG_DIRECTORY)
    for file in files:
        async with aiofiles.open(settings.COURSES_CONFIG_DIRECTORY + f'/{file}', encoding='utf-8') as f:
            data = yaml.safe_load(await f.read())
            courses.append(Course(**data['course']))

    return courses
