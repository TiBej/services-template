from dataclasses import dataclass

from .base_event import BaseEvent


@dataclass
class MailTriggeredEvent(BaseEvent):
    recipient_email: str
    subject: str
    body: str
