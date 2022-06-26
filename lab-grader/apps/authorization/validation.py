from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.exceptions import ValidationException
from apps.authorization.models import NonAuthorizedStudent, Student
from config import Settings


class StudentValidator:
    def __init__(
            self,
            student: NonAuthorizedStudent,
            student_from_sheet: Student,
            github_manager: GithubManagerProtocol,
            course_sheet_manager: CourseSheetManagerProtocol,
            settings: Settings,
    ):
        self.student = student
        self.student_from_sheet = student_from_sheet
        self.__errors: list[dict] = []
        self.github_manager = github_manager
        self.course_sheet_manager = course_sheet_manager
        self.settings = settings

    async def validate(self) -> None:
        await self._validate_github()
        await self._validate_student()
        if self.__errors:
            raise ValidationException(self.__errors)

    async def _validate_github(self) -> None:
        if not await self.github_manager.get_user(self.student.github_username):
            self.__errors.append({'message': 'Такого GitHub аккаунта не существует'})

    async def _validate_student(self) -> None:
        if not self.student_from_sheet.github_username:
            return
        if self.student_from_sheet.github_username != self.student.github_username:
            self.__errors.append(
                {'message': f'Уже есть закрепленный GitHub аккаунт - {self.student_from_sheet.github_username}'},
            )
