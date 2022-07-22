from dateutil.parser import isoparse
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.exceptions import StudentNotFound
from apps.authorization.models import AuthorizedStudent
from apps.grader.exceptions import (
    CourseNotFound,
    GithubLogNotFound,
    LaboratoryWorkNotFound,
    NoAccessToCourse,
    SuccessfulBuildNotFound,
)
from apps.grader.models import LaboratoryWork, RateLabData
from apps.grader.services.github_log_parser import GithubLogParser
from apps.grader.services.lab_grader import get_status
from apps.grader.utils import find_course_by_name
from config import get_settings, Settings
from limiter import limiter

router = APIRouter()


@router.get(
    "/laboratory_works",
    response_model=dict[str, LaboratoryWork],
    status_code=200,
    response_description="List of labs for which repositories have been created",
    operation_id="get_laboratory_works",
)
async def get_laboratory_works(
    request: Request,
    client_bot_id: str,
    course_name: str,
    student: AuthorizedStudent,
    settings: Settings = Depends(get_settings),
    github_manager: GithubManagerProtocol = Depends(),
) -> dict[str, LaboratoryWork]:
    course = await find_course_by_name(course_name, settings)
    if not course:
        raise CourseNotFound
    if course_name not in student.course_names:
        raise NoAccessToCourse

    repositories = await github_manager.get_repositories(
        organization=course.github_organization.organization,
        username=student.github_username,
    )

    laboratory_works = {}
    for repo in repositories:
        for lab_name, lab in course.laboratory_works.items():
            if lab.github_prefix in repo:
                laboratory_works[lab_name] = lab
                break

    return laboratory_works


@router.post(
    "/rate",
    response_model=None,
    status_code=HTTP_204_NO_CONTENT,
    operation_id="rate",
)
@limiter.limit("1/5minute")
async def rate(
    request: Request,
    client_bot_id: str,
    lab_data: RateLabData,
    student: AuthorizedStudent,
    settings: Settings = Depends(get_settings),
    github_manager: GithubManagerProtocol = Depends(),
    course_sheet_manager: CourseSheetManagerProtocol = Depends(),
) -> Response:
    course = await find_course_by_name(lab_data.course_name, settings)
    if not course:
        raise CourseNotFound
    if lab_data.course_name not in student.course_names:
        raise NoAccessToCourse

    try:
        laboratory_work = next(
            lab for lab in course.laboratory_works.values() if lab.short_name == lab_data.laboratory_work
        )
    except StopIteration:
        raise LaboratoryWorkNotFound

    student_from_sheet = await course_sheet_manager.find_student(
        student.fullname,
        student.group,
        course.google_sheet_info,
    )
    if not student_from_sheet:
        raise StudentNotFound

    deadline = await course_sheet_manager.get_deadline(
        student.group,
        laboratory_work,
        spreadsheet_id=course.google_sheet_info.spreadsheet_id,
        timezone=course.timezone,
    )

    repository_name = f"{laboratory_work.github_prefix}-{student.github_username}"
    successful_build = await github_manager.get_successful_build(
        course.github_organization.organization,
        repository_name,
        settings.DEFAULT_CI_JOBS,
        all_successful=True,
    )
    if not successful_build:
        raise SuccessfulBuildNotFound
    completion_date = isoparse(successful_build['completed_at'])

    build_log = await github_manager.get_successful_build_log(
        course.github_organization.organization,
        repository_name,
        settings.DEFAULT_CI_JOBS,
    )
    if not build_log:
        raise GithubLogNotFound

    lab_status = get_status(
        student=student_from_sheet,
        laboratory_work=laboratory_work,
        completion_date=completion_date,
        lab_deadline=deadline,
        log_parser=GithubLogParser(build_log, settings),
        settings=settings,
    )

    await course_sheet_manager.update_lab_status(
        status=lab_status,
        laboratory_work=laboratory_work,
        spreadsheet_id=course.google_sheet_info.spreadsheet_id,
        student=student_from_sheet,
        settings=settings,
    )

    return Response(status_code=HTTP_204_NO_CONTENT)
