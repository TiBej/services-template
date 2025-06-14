import logging
import uuid
from typing import Awaitable, Callable

from common.utilities.correlation_id import set_correlation_id
from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI()


@app.middleware("http")
async def logging_mw(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    """
    Sets the correlation ID for logging and logs request & response
    """
    correlation_id = request.headers.get("X-Correlation-ID")

    # if a correlation id is given it has to be in valid format
    if correlation_id:
        try:
            uuid.UUID(correlation_id)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Correlation ID header has to be in UUID format"
            )

    with set_correlation_id(correlation_id) as correlation_id:
        logging.info(f"{request.method} {request.url}")
        logging.info(f"{request.headers}")
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        logging.info(f"Response status: {response.status_code}")
    return response
