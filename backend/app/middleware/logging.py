from time import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start = time()

        response = await call_next(request)

        duration = time() - start

        request_id = request.state.request_id

        logger.info(
            f"[{request_id}] "
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{duration:.4f}s"
        )

        return response