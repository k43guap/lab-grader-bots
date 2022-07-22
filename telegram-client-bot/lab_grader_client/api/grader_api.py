# flake8: noqa E501
from asyncio import get_event_loop
from typing import TYPE_CHECKING, Awaitable, Dict

from fastapi.encoders import jsonable_encoder

from lab_grader_client import models as m

if TYPE_CHECKING:
    from lab_grader_client.api_client import ApiClient


class _GraderApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_get_laboratory_works(
        self, client_bot_id: str, course_name: str, authorized_student: m.AuthorizedStudent
    ) -> Awaitable[Dict[str, m.LaboratoryWork]]:
        query_params = {"client_bot_id": str(client_bot_id), "course_name": str(course_name)}

        body = jsonable_encoder(authorized_student)

        return self.api_client.request(
            type_=Dict[str, m.LaboratoryWork],
            method="GET",
            url="/api/grader/laboratory_works",
            params=query_params,
            json=body,
        )

    def _build_for_rate(self, client_bot_id: str, body_rate: m.BodyRate) -> Awaitable[m.RateResponse]:
        query_params = {"client_bot_id": str(client_bot_id)}

        body = jsonable_encoder(body_rate)

        return self.api_client.request(
            type_=m.RateResponse, method="POST", url="/api/grader/rate", params=query_params, json=body
        )


class AsyncGraderApi(_GraderApi):
    async def get_laboratory_works(
        self, client_bot_id: str, course_name: str, authorized_student: m.AuthorizedStudent
    ) -> Dict[str, m.LaboratoryWork]:
        return await self._build_for_get_laboratory_works(
            client_bot_id=client_bot_id, course_name=course_name, authorized_student=authorized_student
        )

    async def rate(self, client_bot_id: str, body_rate: m.BodyRate) -> m.RateResponse:
        return await self._build_for_rate(client_bot_id=client_bot_id, body_rate=body_rate)


class SyncGraderApi(_GraderApi):
    def get_laboratory_works(
        self, client_bot_id: str, course_name: str, authorized_student: m.AuthorizedStudent
    ) -> Dict[str, m.LaboratoryWork]:
        coroutine = self._build_for_get_laboratory_works(
            client_bot_id=client_bot_id, course_name=course_name, authorized_student=authorized_student
        )
        return get_event_loop().run_until_complete(coroutine)

    def rate(self, client_bot_id: str, body_rate: m.BodyRate) -> m.RateResponse:
        coroutine = self._build_for_rate(client_bot_id=client_bot_id, body_rate=body_rate)
        return get_event_loop().run_until_complete(coroutine)
