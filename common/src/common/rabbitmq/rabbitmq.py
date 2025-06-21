# pyright: standard

import logging
from collections.abc import Iterator
from contextlib import contextmanager

import pika
from pika.adapters.blocking_connection import BlockingConnection

from common.config.base_config import BaseConfig
from common.rabbitmq.connection import Connection

logger = logging.getLogger(__name__)


class RabbitMQ:
    """Connection & Communication with RabbitMQ."""

    def __init__(self, config: BaseConfig) -> None:
        """Initialize & start connection."""
        self.service_name = config.service_name

        credentials = pika.PlainCredentials(
            config.rabbitmq_user, config.rabbitmq_password
        )
        self.parameters = pika.ConnectionParameters(
            host=config.rabbitmq_host,
            port=config.rabbitmq_port,
            connection_attempts=3,
            credentials=credentials,
        )

    @contextmanager
    def connection(self) -> Iterator[Connection]:
        """Get a currently unused connection."""
        blocking_connection = BlockingConnection(self.parameters)
        connection = Connection(self)
        try:
            yield connection
        finally:
            if connection and not blocking_connection.is_closed:
                blocking_connection.close()
