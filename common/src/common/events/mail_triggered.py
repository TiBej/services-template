from dataclasses import dataclass

from .base_event import BaseEvent


@dataclass(kw_only=True)
class MailTriggeredEvent(BaseEvent):
    """Indicates that a Mail shall be sent."""

    recipient_email: str
    subject: str
    body: str
