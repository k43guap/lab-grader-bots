from asyncio import Protocol
from datetime import datetime
from typing import Optional

from apps.authorization.models import Student
from apps.grader.models import GithubOrganization, GoogleSheetInfo, LaboratoryWork


class CourseSheetManagerProtocol(Protocol):
    async def find_student(self, fullname: str, group: str, google_sheet_info: GoogleSheetInfo) -> Optional[Student]:
        raise NotImplementedError

    async def get_deadline(self, group: str, laboratory_work: LaboratoryWork, spreadsheet_id: str) -> datetime:
        raise NotImplementedError


class GithubManagerProtocol(Protocol):
    async def get_user(self, username: str) -> Optional[dict]:
        raise NotImplementedError

    async def get_repositories(self, github_organization: GithubOrganization, prefix: str = '') -> list[str]:
        raise NotImplementedError

    async def get_default_branch_name(self, repository_name: str) -> str:
        raise NotImplementedError

    async def get_builds(self, repository_name: str) -> list[dict]:
        raise NotImplementedError

    async def get_successful_build(
            self,
            repository_name: str,
            job_names: list[str],
            all_successful: bool = False,
    ) -> Optional[dict]:
        raise NotImplementedError

    async def get_successful_build_log(self, repository_name: str, job_names: list[str]) -> Optional[str]:
        raise NotImplementedError
