from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.exceptions import StudentNotFound
from apps.authorization.models import NonAuthorizedStudent, StudentFromSheet
from apps.authorization.validation import StudentValidator
from apps.grader.utils import get_courses
from config import get_settings, Settings
from limiter import limiter

router = APIRouter()


@router.post(
    "/login",
    response_model=StudentFromSheet,
    status_code=HTTP_200_OK,
    response_description="Student successfully logged in",
    operation_id="login",
)
@limiter.limit("1/5minute")
async def login(
    request: Request,
    client_bot_id: str,
    non_authorized_student: NonAuthorizedStudent,
    github_manager: GithubManagerProtocol = Depends(),
    course_sheet_manager: CourseSheetManagerProtocol = Depends(),
    settings: Settings = Depends(get_settings),
) -> StudentFromSheet:
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
    student_from_sheet.github_username = non_authorized_student.github_username

    return student_from_sheet
