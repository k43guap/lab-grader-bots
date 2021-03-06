from typing import Optional

from pydantic import BaseModel, Field


class GithubOrganization(BaseModel):
    organization: str
    teachers: list[str] = Field(default_factory=list)


class GoogleSheetInfo(BaseModel):
    spreadsheet_id: str = Field(alias='spreadsheet')
    info_sheet: str = Field(alias='info-sheet')
    task_id_column: Optional[int] = Field(alias='task-id-column', default=None)
    student_name_column: int = Field(alias='student-name-column')
    lab_column_offset: int = Field(alias='lab-column-offset')

    class Config:
        allow_population_by_field_name = True


class LaboratoryWork(BaseModel):
    github_prefix: str = Field(alias='github-prefix')
    short_name: str = Field(alias='short-name')
    taskid_max: int = Field(alias='taskid-max')
    penalty_max: int = Field(alias='penalty-max', default=0)
    taskid_shift: int = Field(alias='taskid-shift', default=0)
    ignore_task_id: bool = Field(alias='ignore-task-id', default=False)
    jobs: list[str] | dict = Field(alias='ci', default_factory=list)

    class Config:
        allow_population_by_field_name = True


class Course(BaseModel):
    name: str
    alt_names: list[str] = Field(alias='alt-names', default_factory=list)
    semester: str
    github_organization: GithubOrganization = Field(alias='github')
    google_sheet_info: GoogleSheetInfo = Field(default_factory=dict, alias='google')
    laboratory_works: dict[str, LaboratoryWork] = Field(default_factory=dict, alias='labs')
    timezone: str = Field(default='UTC')

    @property
    def all_course_names(self) -> list[str]:
        course_names = [self.name.lower()] + [name.lower() for name in self.alt_names]
        return course_names

    class Config:
        allow_population_by_field_name = True


class RateLabData(BaseModel):
    course_name: str
    laboratory_work: str


class RateResponse(BaseModel):
    status: str
