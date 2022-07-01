from pydantic import BaseModel, Field


class AuthorizedStudent(BaseModel):
    fullname: str
    group: str
    github_username: str
    courses: list[str] = Field(default_factory=list)

    @classmethod
    def from_message(cls, message: str) -> 'AuthorizedStudent':
        lines = message.split('\n')[1:]
        return AuthorizedStudent(
            fullname=lines[0].split(': ')[1],
            group=lines[1].split(': ')[1],
            github_username=lines[2].split(': ')[1],
            courses=lines[3].split(': ')[1].split(', '),
        )

    def to_message(self) -> str:
        return f"Данные студента:\n" \
               f"Ф.И.О.: {self.fullname}\n" \
               f"Группа: {self.group}\n" \
               f"GitHub: {self.github_username}\n" \
               f"Курсы: {', '.join(self.courses)}"
