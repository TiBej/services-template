"""Custom middleware for logging with a correlation ID."""

import logging
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, HTTPException, Request, Response

from common.logging.correlation_id import set_correlation_id

app = FastAPI()
logger = logging.getLogger(__name__)


@app.middleware("http")
async def logging_mw(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Set the correlation ID for logging and log request & response.

    Uses the correlation ID from the X-Correlation-ID header if present.
    """
    existing_correlation_id = request.headers.get("X-Correlation-ID")

    if existing_correlation_id:
        try:
            uuid.UUID(existing_correlation_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Correlation ID header has to be in UUID format",
            ) from None
    with set_correlation_id(existing_correlation_id) as correlation_id:
        logger.info(
            "New Incoming Request",
            extra={
                "request_method": request.method,
                "request_header": request.headers,
                "request_path": request.url.path,
                "request_query": request.url.query,
            },
        )
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        logger.info("Response status: %d", response.status_code)
    return response
