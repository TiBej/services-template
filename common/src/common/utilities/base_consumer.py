import asyncio
import logging
from abc import abstractmethod
from typing import Type

from common.models.events.base_event import BaseEvent
from common.utilities.correlation_id import set_correlation_id
from common.utilities.rabbitmq import RabbitMQ


class BaseConsumer[B: BaseEvent]:
    """
    Base class for all consumers, handling correlation IDs and event consumption.
    """

    def __init__(self, event_type: Type[B], rabbitmq: RabbitMQ):
        self.event_type = event_type
        self.rabbitmq = rabbitmq

    async def handle_event(self, event: B) -> None:
        """Handle incoming events and set the correlation ID."""
        with set_correlation_id(event.correlation_id):
            logging.info(f"Consuming {event}")
            await self.consume(event)

    @abstractmethod
    async def consume(self, event: B) -> None:
        """Subclasses must implement this method to handle specific events."""
        pass

    def start_consuming(self) -> None:
        """Start consuming messages from RabbitMQ."""

        # Wrap the async method in a sync function
        def sync_handle_event(event: B) -> None:
            asyncio.run(self.handle_event(event))

        self.rabbitmq.consume(self.event_type, sync_handle_event)
