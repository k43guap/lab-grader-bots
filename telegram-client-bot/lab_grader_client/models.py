from typing import Any  # noqa
from typing import List, Optional

from pydantic import BaseModel, Field


class HTTPValidationError(BaseModel):
    detail: "Optional[List[ValidationError]]" = Field(None, alias="detail")


class NonAuthorizedStudent(BaseModel):
    fullname: "str" = Field(..., alias="fullname")
    group: "str" = Field(..., alias="group")
    github_username: "str" = Field(..., alias="github_username")
    email: "str" = Field(..., alias="email")
    course_name: "str" = Field(..., alias="course_name")


class Student(BaseModel):
    variant_number: "int" = Field(..., alias="variant_number")
    fullname: "str" = Field(..., alias="fullname")
    group: "str" = Field(..., alias="group")
    github_username: "Optional[str]" = Field(None, alias="github_username")


class ValidationError(BaseModel):
    loc: "List[Any]" = Field(..., alias="loc")
    msg: "str" = Field(..., alias="msg")
    type: "str" = Field(..., alias="type")
