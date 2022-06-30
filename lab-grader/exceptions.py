from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)
