import asyncio
import logging
from abc import abstractmethod
from types import CoroutineType
from typing import Any

from common.events.base_event import BaseEvent
from common.logging.correlation_id import set_correlation_id

from .rabbitmq import RabbitMQ

logger = logging.getLogger(__name__)


class BaseConsumer[B: BaseEvent]:
    """Base class for all consumers, handling correlation id's and event consumption."""

    def __init__(self, event_type: type[B], rabbitmq: RabbitMQ) -> None:
        """Initialize class."""
        self.event_type = event_type
        self.rabbitmq = rabbitmq

    def _handle_event(self, event: B) -> None:
        """Handle incoming events and set the correlation id."""
        with set_correlation_id(event.correlation_id):
            logger.info(
                "Consuming %s",
                self.event_type,
                extra={
                    "event_type": self.event_type,
                    "event_object": event,
                },
            )
        self._consume(event)

    @abstractmethod
    def _consume(self, event: B) -> None:
        raise NotImplementedError

    def start_consuming(self) -> CoroutineType[Any, Any, None]:
        """Start consuming messages from RabbitMQ."""

        def consume_async() -> None:
            with self.rabbitmq.connection() as connection:
                connection.consume(
                    message_type=self.event_type,
                    func=self._handle_event,
                )

        return asyncio.to_thread(consume_async)
