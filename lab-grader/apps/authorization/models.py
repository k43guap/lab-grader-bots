from typing import Optional

from pydantic import BaseModel


class StudentBase(BaseModel):
    fullname: str
    group: str


class StudentFromSheet(StudentBase):
    variant_number: int
    github_username: Optional[str]


class NonAuthorizedStudent(StudentBase):
    email: str
    course_name: str
    github_username: str


class AuthorizedStudent(StudentBase):
    email: str
    course_names: list[str]
    github_username: str
