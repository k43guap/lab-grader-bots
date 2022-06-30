from api_clients.protocols import CourseSheetManagerProtocol, GithubManagerProtocol
from apps.authorization.exceptions import ValidationException
from apps.authorization.models import NonAuthorizedStudent, Student
from apps.grader.models import Course
from config import Settings


class StudentValidator:
    def __init__(
            self,
            non_authorized_student: NonAuthorizedStudent,
            student_from_sheet: Student,
            github_manager: GithubManagerProtocol,
            course_sheet_manager: CourseSheetManagerProtocol,
            course: Course,
            settings: Settings,
    ):
        self.non_authorized_student = non_authorized_student
        self.student_from_sheet = student_from_sheet
        self.__errors: list[dict] = []
        self.github_manager = github_manager
        self.course_sheet_manager = course_sheet_manager
        self.course = course
        self.settings = settings

    async def validate(self) -> None:
        await self._validate_github_username_existence()
        await self._validate_empty_student_github()
        await self._validate_github_username_uniqueness()
        self._validate_course_name()
        if self.__errors:
            raise ValidationException(self.__errors)

    async def _validate_github_username_existence(self) -> None:
        if not await self.github_manager.get_user(self.non_authorized_student.github_username):
            self.__errors.append({'message': 'Такого GitHub аккаунта не существует'})

    async def _validate_empty_student_github(self) -> None:
        if not self.student_from_sheet.github_username:
            return
        if self.student_from_sheet.github_username != self.non_authorized_student.github_username:
            self.__errors.append(
                {'message': f'Уже есть закрепленный GitHub аккаунт - {self.student_from_sheet.github_username}'},
            )

    async def _validate_github_username_uniqueness(self) -> None:
        github_usernames = await self.course_sheet_manager.get_github_usernames(
            spreadsheet_id=self.course.google_sheet_info.spreadsheet_id,
            settings=self.settings,
        )
        if self.non_authorized_student.github_username in github_usernames:
            self.__errors.append(
                {'message': 'Указан GitHub аккаунт другого студента'},
            )

    def _validate_course_name(self) -> None:
        if self.non_authorized_student.course_name.lower() not in self.course.all_course_names:
            self.__errors.append(
                {'message': f'Курс "{self.non_authorized_student.course_name}" не найден'},
            )
