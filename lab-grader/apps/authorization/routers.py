from fastapi import APIRouter, Depends

from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.exceptions import StudentNotFound
from apps.authorization.models import NonAuthorizedStudent, Student
from apps.authorization.validation import StudentValidator
from apps.grader.utils import get_courses
from config import get_settings, Settings

router = APIRouter()


@router.post("/login")
async def login(
        student: NonAuthorizedStudent,
        github_manager: GithubManagerProtocol = Depends(),
        course_sheet_manager: CourseSheetManagerProtocol = Depends(),
        settings: Settings = Depends(get_settings),
) -> Student:
    for course in await get_courses(settings):
        student_from_sheet = await course_sheet_manager.find_student(
                student.fullname,
                student.group,
                course.google_sheet_info,
        )
        if student_from_sheet:
            break
    else:
        raise StudentNotFound

    student_validator = StudentValidator(student, student_from_sheet, github_manager, course_sheet_manager, settings)

    await student_validator.validate()

    return student_from_sheet
