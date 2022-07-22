from slowapi.extension import Limiter

from limiter.limiter_func import get_limiter_id

limiter = Limiter(key_func=get_limiter_id)
