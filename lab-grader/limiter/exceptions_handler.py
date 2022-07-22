from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Build a simple JSON response that includes the details of the rate limit
    that was hit. If no limit is hit, the countdown is added to headers.
    """
    response = JSONResponse(
        {
            "detail": f"Достигнут лимит запросов: {exc.detail.replace('per', 'в').replace('minute', 'минут')}",
        },
        status_code=429,
    )
    response = request.app.state.limiter._inject_headers(
        response,
        request.state.view_rate_limit,
    )
    return response
