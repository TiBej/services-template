import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from logging import Filter, LogRecord

ctx_correlation_id = ContextVar("correlation_id", default="")


@contextmanager
def set_correlation_id(correlation_id: str | None = None):
    """
    Within this context logging includes correlation id
    """
    correlation_id = correlation_id or str(uuid.uuid4())
    token = ctx_correlation_id.set(correlation_id)
    try:
        yield correlation_id
    finally:
        ctx_correlation_id.reset(token)


class CorrelationIdFilter(Filter):
    """
    A filter which injects context-specific information into logs
    Can be used with %(correlation_id)s
    """

    def filter(self, record: LogRecord):
        record.correlation_id = ctx_correlation_id.get()
        return True
