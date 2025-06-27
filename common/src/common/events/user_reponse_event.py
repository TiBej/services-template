from dataclasses import dataclass

from .base_event import BaseEvent


@dataclass(kw_only=True)
class UserResponseEvent(BaseEvent):
    """Response Response."""

    name: str
