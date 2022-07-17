from fastapi import APIRouter, Depends

from api_clients.protocols import GithubManagerProtocol
from apps.authorization.models import AuthorizedStudent
from apps.grader.exceptions import CourseNotFound, NoAccessToCourse
from apps.grader.models import LaboratoryWork
from apps.grader.utils import get_courses
from config import get_settings, Settings

router = APIRouter()


@router.get(
    "/laboratory_works",
    response_model=dict[str, LaboratoryWork],
    status_code=200,
    response_description="List of labs for which repositories have been created",
    operation_id="get_laboratory_works",
)
async def get_laboratory_works(
    course_name: str,
    student: AuthorizedStudent,
    settings: Settings = Depends(get_settings),
    github_manager: GithubManagerProtocol = Depends(),
) -> dict[str, LaboratoryWork]:
    course = None
    for course in await get_courses(settings):
        if course_name in course.all_course_names:
            course = course
    if not course:
        raise CourseNotFound

    if course_name not in student.course_names:
        raise NoAccessToCourse

    repositories = await github_manager.get_repositories(
        github_organization=course.github_organization,
        username=student.github_username,
    )

    laboratory_works = {}
    for repo in repositories:
        for lab_name, lab in course.laboratory_works.items():
            if lab.github_prefix in repo:
                laboratory_works[lab_name] = lab
                break

    return laboratory_works
