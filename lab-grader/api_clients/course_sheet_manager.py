import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from aiogoogle.excs import HTTPError
from dateutil.parser import parse
from dateutil.tz import gettz

from api_clients.google.google_sheets_client import GoogleSheetClient
from apps.authorization.models import StudentFromSheet
from apps.grader.models import GoogleSheetInfo, LaboratoryWork
from config import Settings


@dataclass
class ResultColumnQuery:
    column_ind: int
    values: list[str]


@dataclass
class ResultCellQuery:
    google_sheet_cell_id: str
    value: str


class CourseSheetManager:
    def __init__(self, google_sheets_client: GoogleSheetClient):
        self._google_sheets_client = google_sheets_client

    def __find_columns_in_response(
            self,
            unique_string: str,
            response_sheets: dict,
    ) -> Optional[dict[str, ResultColumnQuery]]:
        response_sheets = response_sheets['sheets']
        column_indexes = []
        sheet_indexes = []
        titles = []
        for sheet_ind, sheet in enumerate(response_sheets):
            title = sheet['properties']['title']
            for row in sheet['data'][0]['rowData']:
                row_values = []
                if not row:
                    continue
                for row_data in row['values']:
                    if 'formattedValue' in row_data:
                        row_values.append(row_data['formattedValue'])
                    else:
                        row_values.append('')  # empty cell
                if unique_string in row_values:
                    column_indexes.append(row_values.index(unique_string))
                    sheet_indexes.append(sheet_ind)
                    titles.append(title)
        columns: dict[str, ResultColumnQuery] = {}
        for column_ind, sheet_ind, title in zip(column_indexes, sheet_indexes, titles):
            columns[title] = ResultColumnQuery(column_ind, [])
            for row in response_sheets[sheet_ind]['data'][0]['rowData']:
                cell_value = row['values'][column_ind]
                if 'formattedValue' in cell_value:
                    columns[title].values.append(cell_value['formattedValue'])
        if not columns:
            return None
        return columns

    def __find_column_in_response_by_sheet(
            self,
            unique_string: str,
            response_sheet: dict,
    ) -> Optional[ResultColumnQuery]:
        sheet_columns = response_sheet['valueRanges'][0]['values']
        for column in sheet_columns:
            column = list(map(str, column))
            if unique_string in column:
                return ResultColumnQuery(sheet_columns.index(column), column)
        return None

    async def _find_column_in_sheet(
            self,
            unique_string: str,
            sheet_title: str,
            spreadsheet_id: str,
    ) -> Optional[ResultColumnQuery]:
        try:
            group_sheets = await self._google_sheets_client.get_sheets_values_by_column(
                spreadsheet_id,
                sheet_titles=[sheet_title],
            )
        except HTTPError:
            return None

        return self.__find_column_in_response_by_sheet(unique_string, group_sheets)

    async def _find_columns(self, unique_string: str, spreadsheet_id: str) -> Optional[dict[str, ResultColumnQuery]]:
        response_sheets = await self._google_sheets_client.get_spreadsheet(
            spreadsheet_id=spreadsheet_id,
            include_values=True,
        )
        return self.__find_columns_in_response(unique_string, response_sheets)

    async def _get_intersection_cell(
            self,
            first_column_name: str,
            second_column_name: str,
            row_value_in_second_column: str,
            sheet_title: str,
            spreadsheet_id: str,
    ) -> ResultCellQuery:
        group_sheet = await self._google_sheets_client.get_sheets_values_by_column(
            spreadsheet_id,
            sheet_titles=[sheet_title],
        )
        first_column = self.__find_column_in_response_by_sheet(first_column_name, group_sheet)
        second_column = self.__find_column_in_response_by_sheet(second_column_name, group_sheet)
        if not first_column or not second_column:
            raise ValueError(f'Columns {first_column_name} and {second_column_name} not found')
        first_column_values = first_column.values
        second_column_values = second_column.values
        if len(first_column_values) > len(second_column_values):
            second_column_values += max(0, len(first_column_values) - len(second_column_values)) * ['']
        if len(first_column_values) < len(second_column_values):
            first_column_values += max(0, len(second_column_values) - len(first_column_values)) * ['']
        col_ind = first_column.column_ind
        row_ind = second_column.values.index(row_value_in_second_column)

        google_sheet_cell_id = f"{sheet_title}!{self._number_to_string(col_ind)}{row_ind + 1}"
        return ResultCellQuery(google_sheet_cell_id, first_column.values[row_ind])

    def _number_to_string(self, number: int) -> str:
        string = ""
        number += 1
        while number > 0:
            number, remainder = divmod(number - 1, 26)
            string = chr(65 + remainder) + string
        return string

    async def find_student(
            self,
            fullname: str,
            group: str,
            google_sheet_info: GoogleSheetInfo,
    ) -> Optional[StudentFromSheet]:
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
            if google_sheet_info.task_id_column is not None:
                task_id_column = sheet_values[google_sheet_info.task_id_column]
            else:
                task_id_column = []
            github_column = next(column for column in sheet_values if column[0] == 'GitHub')
            github_column += max(0, len(students_column) - len(github_column)) * ['']
            if fullname in students_column:
                student_index = students_column.index(fullname)
                if task_id_column:
                    task_id = task_id_column[student_index]
                else:
                    task_id = -1
                if group_text := re.search(r"'(.+?)'", group_sheet['range']):
                    group = group_text.group(1)
                github_username = github_column[student_index]
                if not github_username:
                    github_username = None
                return StudentFromSheet(
                    variant_number=task_id,
                    fullname=fullname,
                    group=group,
                    github_username=github_username,
                )

        return None

    async def get_deadline(
            self,
            group: str,
            laboratory_work: LaboratoryWork,
            spreadsheet_id: str,
            timezone: str,
    ) -> datetime:
        group_sheets = await self._google_sheets_client.get_sheets_values_by_column(
            spreadsheet_id,
            sheet_titles=[group],
        )

        moscow_tz = {"MSK": gettz("Russia/Moscow")}

        sheet_columns = group_sheets['valueRanges'][0]['values']
        for column in sheet_columns:
            if laboratory_work.short_name in column:
                deadline = column[0]
                if len(deadline.split('.')) == 2:
                    deadline += f".{datetime.now().year}"
                deadline += f" 23:59:59 {timezone}"
                return parse(deadline, dayfirst=True, tzinfos=moscow_tz)

        raise ValueError(laboratory_work.short_name)  # this code is unreachable

    async def update_github_username(
            self,
            student: StudentFromSheet,
            new_github_username: str,
            spreadsheet_id: str,
            settings: Settings,
    ) -> None:
        cell = await self._get_intersection_cell(
            first_column_name=settings.GITHUB_COLUMN,
            second_column_name=settings.STUDENT_FULLNAME_COLUMN,
            row_value_in_second_column=student.fullname,
            sheet_title=student.group,
            spreadsheet_id=spreadsheet_id,
        )
        await self._google_sheets_client.update_cell(spreadsheet_id, cell.google_sheet_cell_id, new_github_username)

    async def update_lab_status(
            self,
            status: str,
            student: StudentFromSheet,
            laboratory_work: LaboratoryWork,
            spreadsheet_id: str,
            settings: Settings,
    ) -> None:
        cell = await self._get_intersection_cell(
            first_column_name=laboratory_work.short_name,
            second_column_name=settings.STUDENT_FULLNAME_COLUMN,
            row_value_in_second_column=student.fullname,
            sheet_title=student.group,
            spreadsheet_id=spreadsheet_id,
        )
        await self._google_sheets_client.update_cell(spreadsheet_id, cell.google_sheet_cell_id, status)

    async def get_github_usernames(self, spreadsheet_id: str, settings: Settings) -> list[str]:
        github_columns = await self._find_columns(settings.GITHUB_COLUMN, spreadsheet_id)
        if not github_columns:
            raise ValueError(f'Column {settings.GITHUB_COLUMN} not found')
        github_usernames = []

        for column in github_columns.values():
            for github_username in column.values:
                if github_username == settings.GITHUB_COLUMN:
                    continue
                github_usernames.append(github_username)
        return github_usernames
