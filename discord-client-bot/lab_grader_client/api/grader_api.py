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
        self, course_name: str, authorized_student: m.AuthorizedStudent
    ) -> Awaitable[Dict[str, m.LaboratoryWork]]:
        query_params = {"course_name": str(course_name)}

        body = jsonable_encoder(authorized_student)

        return self.api_client.request(
            type_=Dict[str, m.LaboratoryWork],
            method="GET",
            url="/api/grader/laboratory_works",
            params=query_params,
            json=body,
        )


class AsyncGraderApi(_GraderApi):
    async def get_laboratory_works(
        self, course_name: str, authorized_student: m.AuthorizedStudent
    ) -> Dict[str, m.LaboratoryWork]:
        return await self._build_for_get_laboratory_works(
            course_name=course_name, authorized_student=authorized_student
        )


class SyncGraderApi(_GraderApi):
    def get_laboratory_works(
        self, course_name: str, authorized_student: m.AuthorizedStudent
    ) -> Dict[str, m.LaboratoryWork]:
        coroutine = self._build_for_get_laboratory_works(course_name=course_name, authorized_student=authorized_student)
        return get_event_loop().run_until_complete(coroutine)
