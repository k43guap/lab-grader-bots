from json.decoder import JSONDecodeError
from typing import Any


def format_error(error: str) -> str:
    return f"⚠ {error} ⚠"


def parse_unexpected_exception(exception: Any) -> list[str]:
    fallback_message = ['Обратитесь к администратору системы']
    if not hasattr(exception, 'structured'):
        return fallback_message

    try:
        exception_structure: dict = exception.structured()
    except JSONDecodeError:
        return fallback_message

    if 'detail' not in exception_structure:
        return fallback_message

    detail = exception_structure['detail']

    if isinstance(detail, str):
        return [format_error(detail)]

    if isinstance(detail, list):
        messages = []
        for exception in detail:
            messages.append(format_error(exception['message']))
        return messages

    return fallback_message
