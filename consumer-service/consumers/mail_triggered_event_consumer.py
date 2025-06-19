import logging

from common.events.mail_triggered import MailTriggeredEvent
from common.rabbitmq.base_consumer import BaseConsumer

logger = logging.getLogger(__name__)


class MailTriggeredEventConsumer(BaseConsumer[MailTriggeredEvent]):
    """Consumer for MailEventTriggered."""

    async def _consume(self, event: MailTriggeredEvent) -> None:
        logger.info("Sucessfully consumed %s", event)
