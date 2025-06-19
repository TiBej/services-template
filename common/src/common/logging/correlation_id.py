import logging
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

ctx_correlation_id = ContextVar("correlation_id", default="")


@contextmanager
def set_correlation_id(existing_id: str | None = None) -> Iterator[str]:
    """Within this context logging includes correlation id."""
    correlation_id = existing_id or str(uuid.uuid4())
    token = ctx_correlation_id.set(correlation_id)
    try:
        yield correlation_id
    finally:
        ctx_correlation_id.reset(token)


class CorrelationIdFilter(logging.Filter):
    """Filter that injects correlation id for logging."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add `correlation_id` to logging record."""
        record.correlation_id = ctx_correlation_id.get()
        return True
