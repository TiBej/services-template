# pyright: standard

import logging
from collections.abc import Iterator
from contextlib import contextmanager

import pika

from common.config.base_config import BaseConfig
from common.events.base_event import BaseEvent
from common.rabbitmq.handler import Handler
from common.rabbitmq.rpc_handler import RPCHandler

logger = logging.getLogger(__name__)


class RabbitMQ:
    """Connection & Communication with RabbitMQ."""

    def __init__(self, config: BaseConfig) -> None:
        """Initialize & start connection."""
        self.service_name = config.service_name

        credentials = pika.PlainCredentials(
            config.rabbitmq_user, config.rabbitmq_password
        )
        self.parameter = pika.ConnectionParameters(
            host=config.rabbitmq_host,
            port=config.rabbitmq_port,
            connection_attempts=3,
            credentials=credentials,
        )

    @contextmanager
    def handler(self) -> Iterator[Handler]:
        """Get a rabbitmq handler that does basic publish & consume."""
        handler = Handler(
            connection_parameter=self.parameter, service_name=self.service_name
        )
        try:
            yield handler
        finally:
            if handler.connection and not handler.connection.is_closed:
                handler.connection.close()

    # RT = response type, CT = consumer type
    @contextmanager
    def rpc_handler[RT: BaseEvent, CT: BaseEvent](
        self, response_type: type[RT], consume_type: type[CT]
    ) -> Iterator[RPCHandler[RT, CT]]:
        """Get a rabbitmq handler that manages request / reply."""
        rpc_handler = RPCHandler[RT, CT](
            connection_parameter=self.parameter,
            response_type=response_type,
            consume_type=consume_type,
        )
        yield rpc_handler
