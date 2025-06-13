import uuid
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class BaseEvent:
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
