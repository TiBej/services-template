import asyncio
import logging

from consumers.mail_triggered_event_consumer import MailTriggeredEventConsumer

from common.config.base_config import BaseConfig
from common.events.mail_triggered import MailTriggeredEvent
from common.logging.logging_setup import setup_logging
from common.rabbitmq.rabbitmq import RabbitMQ

config = BaseConfig()
setup_logging(config)
rabbitmq = RabbitMQ(config)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Start Consumer Service."""
    async with asyncio.TaskGroup() as tg:
        consumer = MailTriggeredEventConsumer(MailTriggeredEvent, rabbitmq)
        tg.create_task(consumer.start_consuming())

        logger.info("Service successfully started")


if __name__ == "__main__":
    asyncio.run(main())
