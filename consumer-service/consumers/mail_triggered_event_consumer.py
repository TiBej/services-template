import asyncio
import logging

from common.models.events.mail_triggered import MailTriggeredEvent
from common.utilities.base_consumer import BaseConsumer


class MailTriggeredEventConsumer(BaseConsumer[MailTriggeredEvent]):
    async def consume(self, event: MailTriggeredEvent) -> None:
        await asyncio.sleep(1)
        logging.info(event)
        logging.info("hi")
