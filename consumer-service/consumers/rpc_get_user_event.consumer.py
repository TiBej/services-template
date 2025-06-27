import logging

from common.events.user_reponse_event import UserResponseEvent
from common.events.user_request_event import UserRequestEvent
from common.rabbitmq.rpc_base_consumer import RPCBaseConsumer

logger = logging.getLogger(__name__)


class MailTriggeredEventConsumer(RPCBaseConsumer[UserResponseEvent]):
    """Consumer for MailEventTriggered."""

    def _consume(self, event: UserRequestEvent) -> UserResponseEvent:
        logger.info("Received Request %s", event.id)
        return UserResponseEvent(name="Max")
