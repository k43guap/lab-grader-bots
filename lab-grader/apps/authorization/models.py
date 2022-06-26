from typing import Optional

from pydantic import BaseModel


class Student(BaseModel):
    variant_number: int
    fullname: str
    group: str
    github_username: Optional[str]
