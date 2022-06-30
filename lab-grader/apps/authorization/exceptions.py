from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from exceptions import CustomHTTPException


class ValidationException(HTTPException):
    def __init__(self, detail: list[dict]):
        super().__init__(HTTP_400_BAD_REQUEST, detail)


class StudentNotFound(CustomHTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = 'Студент с такими данным не найден ни в одном из курсов'
