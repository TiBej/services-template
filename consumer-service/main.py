import asyncio
import logging

from consumers.mail_triggered_event_consumer import MailTriggeredEventConsumer
from consumers.rpc_get_user_event_consumer import RPCGetUserEventConsumer

from common.config.base_config import BaseConfig
from common.events.mail_triggered import MailTriggeredEvent
from common.events.user_reponse_event import UserResponseEvent
from common.events.user_request_event import UserRequestEvent
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

        consumer2 = RPCGetUserEventConsumer(
            UserRequestEvent, UserResponseEvent, rabbitmq
        )
        tg.create_task(consumer2.start_consuming())

        logger.info("Service successfully started")


if __name__ == "__main__":
    asyncio.run(main())
