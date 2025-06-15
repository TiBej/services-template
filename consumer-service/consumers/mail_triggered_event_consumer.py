import asyncio
import logging

from common.events.mail_triggered import MailTriggeredEvent
from common.rabbitmq.base_consumer import BaseConsumer

logger = logging.getLogger(__name__)


class MailTriggeredEventConsumer(BaseConsumer[MailTriggeredEvent]):
    async def consume(self, event: MailTriggeredEvent) -> None:
        await asyncio.sleep(1)
        logger.info(event)
        logger.info("hi")
