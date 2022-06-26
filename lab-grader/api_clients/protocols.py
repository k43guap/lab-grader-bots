from asyncio import Protocol
from typing import Optional

from apps.authorization.models import Student
from apps.grader.models import GoogleSheetInfo


class CourseSheetManagerProtocol(Protocol):
    async def find_student(self, fullname: str, group: str, google_sheet_info: GoogleSheetInfo) -> Optional[Student]:
        raise NotImplementedError
