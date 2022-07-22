from typing import Any  # noqa
from typing import List, Optional

from pydantic import BaseModel, Field


class AuthorizedStudent(BaseModel):
    fullname: "str" = Field(..., alias="fullname")
    group: "str" = Field(..., alias="group")
    email: "str" = Field(..., alias="email")
    course_names: "List[str]" = Field(..., alias="course_names")
    github_username: "str" = Field(..., alias="github_username")


class HTTPValidationError(BaseModel):
    detail: "Optional[List[ValidationError]]" = Field(None, alias="detail")


class LaboratoryWork(BaseModel):
    github_prefix: "str" = Field(..., alias="github-prefix")
    short_name: "str" = Field(..., alias="short-name")
    taskid_max: "int" = Field(..., alias="taskid-max")
    penalty_max: "int" = Field(..., alias="penalty-max")
    taskid_shift: "Optional[int]" = Field(None, alias="taskid-shift")
    ignore_task_id: "Optional[bool]" = Field(None, alias="ignore-task-id")
    ci: "Optional[Any]" = Field(None, alias="ci")


class NonAuthorizedStudent(BaseModel):
    fullname: "str" = Field(..., alias="fullname")
    group: "str" = Field(..., alias="group")
    email: "str" = Field(..., alias="email")
    course_name: "str" = Field(..., alias="course_name")
    github_username: "str" = Field(..., alias="github_username")


class StudentFromSheet(BaseModel):
    fullname: "str" = Field(..., alias="fullname")
    group: "str" = Field(..., alias="group")
    variant_number: "int" = Field(..., alias="variant_number")
    github_username: "Optional[str]" = Field(None, alias="github_username")


class ValidationError(BaseModel):
    loc: "List[Any]" = Field(..., alias="loc")
    msg: "str" = Field(..., alias="msg")
    type: "str" = Field(..., alias="type")
