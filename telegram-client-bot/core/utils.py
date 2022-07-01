from typing import Any


def parse_unexpected_exception(exception: Any) -> list[str]:
    fallback_message = ['Обратитесь к администратору системы']
    if not hasattr(exception, 'structured'):
        return fallback_message
    exception_structure: dict = exception.structured()

    if 'detail' not in exception_structure:
        return fallback_message

    detail = exception_structure['detail']

    if isinstance(detail, str):
        return [detail]

    if isinstance(detail, list):
        messages = []
        for exception in detail:
            messages.append(exception['message'])
        return messages

    return fallback_message
