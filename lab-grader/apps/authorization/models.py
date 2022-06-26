from typing import Optional

from pydantic import BaseModel


class Student(BaseModel):
    variant_number: int
    fullname: str
    group: str
    github_username: Optional[str]


class NonAuthorizedStudent(BaseModel):
    fullname: str
    group: str
    github_username: str
    email: str
    course_name: str
