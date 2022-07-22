import os
from typing import Optional

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


async def find_course_by_name(course_name: str, settings: Settings) -> Optional[Course]:
    course = None
    for course in await get_courses(settings):
        if course_name in course.all_course_names:
            course = course
    return course
