from asyncio import Protocol
from datetime import datetime
from typing import Optional

from apps.authorization.models import StudentFromSheet
from apps.grader.models import GoogleSheetInfo, LaboratoryWork
from config import Settings


class CourseSheetManagerProtocol(Protocol):
    async def find_student(
            self,
            fullname: str,
            group: str,
            google_sheet_info: GoogleSheetInfo,
    ) -> Optional[StudentFromSheet]:
        raise NotImplementedError

    async def get_deadline(
            self,
            group: str,
            laboratory_work: LaboratoryWork,
            spreadsheet_id: str,
            timezone: str,
    ) -> datetime:
        raise NotImplementedError

    async def update_github_username(
            self,
            student: StudentFromSheet,
            new_github_username: str,
            spreadsheet_id: str,
            settings: Settings,
    ) -> None:
        raise NotImplementedError

    async def update_lab_status(
            self,
            status: str,
            student: StudentFromSheet,
            laboratory_work: LaboratoryWork,
            spreadsheet_id: str,
            settings: Settings,
    ) -> None:
        raise NotImplementedError

    async def get_github_usernames(self, spreadsheet_id: str, settings: Settings) -> list[str]:
        raise NotImplementedError


class GithubManagerProtocol(Protocol):
    async def get_user(self, username: str) -> Optional[dict]:
        raise NotImplementedError

    async def get_repositories(self, organization: str, username: str = '') -> list[str]:
        raise NotImplementedError

    async def get_default_branch_name(self, organisation: str, repository_name: str) -> str:
        raise NotImplementedError

    async def get_builds(self, organisation: str, repository_name: str) -> list[dict]:
        raise NotImplementedError

    async def get_successful_build(
            self,
            organisation: str,
            repository_name: str,
            job_names: list[str],
            all_successful: bool = False,
    ) -> Optional[dict]:
        raise NotImplementedError

    async def get_successful_build_log(
            self,
            organisation: str,
            repository_name: str,
            job_names: list[str],
    ) -> Optional[str]:
        raise NotImplementedError
