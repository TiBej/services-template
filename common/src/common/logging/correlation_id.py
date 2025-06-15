import uuid
from contextlib import contextmanager
from contextvars import ContextVar

ctx_correlation_id = ContextVar("correlation_id", default="")


@contextmanager
def set_correlation_id(correlation_id: str | None = None):
    """
    Within this context logging includes correlation id
    """
    correlation_id = correlation_id or str(uuid.uuid4())
    ctx_correlation_id.set(correlation_id)
    yield correlation_id
