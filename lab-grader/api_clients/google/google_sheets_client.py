import json

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from aiogoogle.resource import Resource

from api_clients.google.exceptions import GoogleSheetSessionIsNotInitialized
from config import Settings


class GoogleSheetSession:
    def __init__(self, settings: Settings):
        self._spreadsheets = None
        self._aiogoogle = None
        self._creds = None
        with open(settings.GOOGLE_KEY_FILE_PATH, "r") as key_file:
            self._creds = json.load(key_file)

    async def init_session(self) -> None:
        service_account = ServiceAccountCreds(scopes=['https://www.googleapis.com/auth/spreadsheets'], **self._creds)
        async with Aiogoogle(service_account_creds=service_account) as aiogoogle:
            google_sheets_service = await aiogoogle.discover("sheets", "v4")
        self._spreadsheets = google_sheets_service.spreadsheets
        self._aiogoogle = aiogoogle

    @property
    def spreadsheets(self) -> Resource:
        if not self._spreadsheets:
            raise GoogleSheetSessionIsNotInitialized
        return self._spreadsheets  # type: ignore

    @property
    def aiogoogle(self) -> Aiogoogle:
        if not self._spreadsheets:
            raise GoogleSheetSessionIsNotInitialized
        return self._aiogoogle  # type: ignore


class GoogleSheetClient:
    def __init__(self, google_sheet_session: GoogleSheetSession):
        self._spreadsheets = google_sheet_session.spreadsheets
        self._aiogoogle = google_sheet_session.aiogoogle

    async def get_spreadsheet(self, spreadsheet_id: str, include_values: bool = False) -> dict:
        response = await self._aiogoogle.as_service_account(self._spreadsheets.get(
            spreadsheetId=spreadsheet_id,
            includeGridData=include_values,
        ))
        return dict(response)

    async def get_sheets_values_by_column(self, spreadsheet_id: str, sheet_titles: list[str]) -> dict:
        response = await self._aiogoogle.as_service_account(self._spreadsheets.values.batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=sheet_titles,
            majorDimension='COLUMNS',
        ))
        return dict(response)

    async def get_sheets_values_by_row(self, spreadsheet_id: str, sheet_titles: list[str]) -> dict:
        response = await self._aiogoogle.as_service_account(self._spreadsheets.values.batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=sheet_titles,
            majorDimension='ROWS',
        ))
        return dict(response)
