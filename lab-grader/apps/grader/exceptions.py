from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from exceptions import CustomHTTPException


class CourseNotFound(CustomHTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = 'Курс не найден'


class NoAccessToCourse(CustomHTTPException):
    status_code = HTTP_403_FORBIDDEN
    detail = 'Нет доступа к курсу'
