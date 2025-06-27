import asyncio
import logging
from abc import abstractmethod

from common.events.base_event import BaseEvent
from common.logging.correlation_id import set_correlation_id

from .rabbitmq import RabbitMQ

logger = logging.getLogger(__name__)


# RT = response type, CT = consumer type
class RPCBaseConsumer[RT: BaseEvent, CT: BaseEvent]:
    """Base class for all RPC consumers."""

    def __init__(
        self, consume_type: type[CT], response_type: type[RT], rabbitmq: RabbitMQ
    ) -> None:
        """Initialize class."""
        self.response_type = response_type
        self.consume_type = consume_type
        self.rabbitmq = rabbitmq

    def _handle_event(self, event: CT) -> RT:
        """Handle incoming events and set the correlation id."""
        with set_correlation_id(event.correlation_id):
            logger.info(
                "Consuming %s",
                self.response_type,
                extra={
                    "event_type": self.response_type,
                    "event_object": event,
                },
            )
            return self._consume(event)

    @abstractmethod
    def _consume(self, event: CT) -> RT:
        raise NotImplementedError

    async def start_consuming(self) -> None:
        """Start consuming messages from RabbitMQ."""

        def exec_consume() -> None:
            with self.rabbitmq.rpc_handler(
                self.response_type, self.consume_type
            ) as rpc_handler:
                rpc_handler.consume(
                    consume_type=self.consume_type,
                    func=self._handle_event,
                )

        await asyncio.to_thread(exec_consume)
