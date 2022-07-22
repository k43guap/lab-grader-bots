# flake8: noqa E501
from asyncio import get_event_loop
from typing import TYPE_CHECKING, Awaitable

from fastapi.encoders import jsonable_encoder

from lab_grader_client import models as m

if TYPE_CHECKING:
    from lab_grader_client.api_client import ApiClient


class _AuthorizationApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_login(
        self, client_bot_id: str, non_authorized_student: m.NonAuthorizedStudent
    ) -> Awaitable[m.StudentFromSheet]:
        query_params = {"client_bot_id": str(client_bot_id)}

        body = jsonable_encoder(non_authorized_student)

        return self.api_client.request(
            type_=m.StudentFromSheet, method="POST", url="/api/authorization/login", params=query_params, json=body
        )


class AsyncAuthorizationApi(_AuthorizationApi):
    async def login(self, client_bot_id: str, non_authorized_student: m.NonAuthorizedStudent) -> m.StudentFromSheet:
        return await self._build_for_login(client_bot_id=client_bot_id, non_authorized_student=non_authorized_student)


class SyncAuthorizationApi(_AuthorizationApi):
    def login(self, client_bot_id: str, non_authorized_student: m.NonAuthorizedStudent) -> m.StudentFromSheet:
        coroutine = self._build_for_login(client_bot_id=client_bot_id, non_authorized_student=non_authorized_student)
        return get_event_loop().run_until_complete(coroutine)
