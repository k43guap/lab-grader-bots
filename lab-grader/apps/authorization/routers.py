from fastapi import APIRouter, Depends

from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.exceptions import StudentNotFound
from apps.authorization.models import NonAuthorizedStudent, Student
from apps.authorization.validation import StudentValidator
from apps.grader.utils import get_courses
from config import get_settings, Settings

router = APIRouter()


@router.post(
    "/login",
    response_model=Student,
    status_code=200,
    response_description="Student successfully logged in",
    operation_id="login",
)
async def login(
        non_authorized_student: NonAuthorizedStudent,
        github_manager: GithubManagerProtocol = Depends(),
        course_sheet_manager: CourseSheetManagerProtocol = Depends(),
        settings: Settings = Depends(get_settings),
) -> Student:
    for course in await get_courses(settings):
        student_from_sheet = await course_sheet_manager.find_student(
            non_authorized_student.fullname,
            non_authorized_student.group,
            course.google_sheet_info,
        )
        if student_from_sheet:
            break
    else:
        raise StudentNotFound

    student_validator = StudentValidator(
        non_authorized_student=non_authorized_student,
        student_from_sheet=student_from_sheet,
        github_manager=github_manager,
        course_sheet_manager=course_sheet_manager,
        course=course,
        settings=settings,
    )
    await student_validator.validate()

    await course_sheet_manager.update_github_username(
        student_from_sheet,
        non_authorized_student.github_username,
        course.google_sheet_info.spreadsheet_id,
        settings,
    )

    return student_from_sheet
