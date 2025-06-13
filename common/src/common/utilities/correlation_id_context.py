import uuid
from contextlib import contextmanager

from .logging_fw import ctx_correlation_id


@contextmanager
def set_correlation_id():
    correlation_id = str(uuid.uuid4())
    ctx_correlation_id.set(correlation_id)
    yield correlation_id
