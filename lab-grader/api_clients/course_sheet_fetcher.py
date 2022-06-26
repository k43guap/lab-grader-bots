import re
from typing import Optional

from api_clients.google.google_sheets_client import GoogleSheetClient
from apps.authorization.models import Student
from apps.grader.models import GoogleSheetInfo


class CourseSheetManager:
    def __init__(self, google_sheets_client: GoogleSheetClient):
        self._google_sheets_client = google_sheets_client

    async def find_student(self, fullname: str, group: str, google_sheet_info: GoogleSheetInfo) -> Optional[Student]:
        group_sheets = await self._google_sheets_client.get_sheets_values_by_column(
            google_sheet_info.spreadsheet_id,
            sheet_titles=[group],
        )
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
