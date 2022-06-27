import re
from datetime import datetime
from typing import Optional

from aiogoogle.excs import HTTPError

from api_clients.google.google_sheets_client import GoogleSheetClient
from apps.authorization.models import Student
from apps.grader.models import GoogleSheetInfo, LaboratoryWork


class CourseSheetManager:
    def __init__(self, google_sheets_client: GoogleSheetClient):
        self._google_sheets_client = google_sheets_client

    async def find_student(self, fullname: str, group: str, google_sheet_info: GoogleSheetInfo) -> Optional[Student]:
        try:
            group_sheets = await self._google_sheets_client.get_sheets_values_by_column(
                google_sheet_info.spreadsheet_id,
                sheet_titles=[group],
            )
        except HTTPError:
            return None

        group_sheets = group_sheets['valueRanges']

        for group_sheet in group_sheets:
            sheet_values = group_sheet['values']
            students_column = sheet_values[google_sheet_info.student_name_column]
            task_id_column = sheet_values[google_sheet_info.task_id_column]
            github_column = next(column for column in sheet_values if column[0] == 'GitHub')
            if fullname in students_column:
                student_index = students_column.index(fullname)
                task_id = task_id_column[student_index]
                if group_text := re.search(r"'(.+?)'", group_sheet['range']):
                    group = group_text.group(1)
                github_username = github_column[student_index]
                if not github_username:
                    github_username = None
                return Student(variant_number=task_id, fullname=fullname, group=group, github_username=github_username)

        return None

    async def get_deadline(self, group: str, laboratory_work: LaboratoryWork, spreadsheet_id: str) -> datetime:
        group_sheets = await self._google_sheets_client.get_sheets_values_by_column(
            spreadsheet_id,
            sheet_titles=[group],
        )

        sheet_columns = group_sheets['valueRanges'][0]['values']
        for column in sheet_columns:
            if laboratory_work.short_name in column:
                return datetime.strptime(column[0], '%d.%m.%Y')
        raise ValueError(laboratory_work.short_name)  # this code is unreachable
