from starlette.requests import Request


def get_limiter_id(request: Request) -> str:
    client_bot_id = request.query_params.get('client_bot_id')
    return client_bot_id
