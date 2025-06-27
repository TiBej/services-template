from dataclasses import dataclass

from common.events.base_event import BaseEvent


@dataclass(kw_only=True)
class UserRequestEvent(BaseEvent):
    """Request a user."""

    id: int
