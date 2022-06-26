from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class ValidationException(HTTPException):
    def __init__(self, detail: list[dict]):
        super().__init__(HTTP_400_BAD_REQUEST, detail)


class StudentNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Студент с такими данным не найден ни в одном из курсов',
        )
