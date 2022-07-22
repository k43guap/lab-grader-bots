from lab_grader_client.models import AuthorizedStudent as AuthorizedStudentModel


class AuthorizedStudent(AuthorizedStudentModel):

    @classmethod
    def from_message(cls, message: str) -> 'AuthorizedStudent':
        lines = message.split('\n')[1:]
        return AuthorizedStudent(
            fullname=lines[0].split(': ')[1],
            group=lines[1].split(': ')[1],
            github_username=lines[2].split(': ')[1],
            course_names=lines[3].split(': ')[1].split(', '),
            email=lines[4].split(': ')[1],
        )

    def to_message(self) -> str:
        return f"Данные студента:\n" \
               f"Ф.И.О.: {self.fullname}\n" \
               f"Группа: {self.group}\n" \
               f"GitHub: {self.github_username}\n" \
               f"Курсы: {', '.join(self.course_names)}\n" \
               f"Почта: {self.email}"
