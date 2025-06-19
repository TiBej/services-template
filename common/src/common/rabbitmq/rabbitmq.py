# pyright: standard

import json
import logging
import math
import time
from collections.abc import Callable
from typing import TypeVar

import pika

from common.config.base_config import BaseConfig
from common.events.base_event import BaseEvent
from common.rabbitmq.rabbitmq_exceptions import RabbitMQConnectionLostError

logger = logging.getLogger(__name__)


class RabbitMQ:
    """Connection & Communication with RabbitMQ."""

    T = TypeVar("T", bound=BaseEvent)

    def __init__(self, config: BaseConfig) -> None:
        """Initialize & start connection."""
        self.service_name = config.service_name
        self.user = config.rabbitmq_user
        self.password = config.rabbitmq_password
        self.host = config.rabbitmq_host
        self.port = config.rabbitmq_port
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self) -> None:
        """Connect to RabbitMQ."""
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            connection_attempts=3,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self) -> None:
        """Close Connection to RabbitMQ."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume[B: BaseEvent](
        self, message_type: type[B], func: Callable[[B], None]
    ) -> None:
        """Consume Event."""
        if not self.channel:
            raise RabbitMQConnectionLostError

        exchange_name = f"{message_type.__module__}.{message_type.__name__}".lower()

        self.channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        # processing queue
        processing_queue_name = f"{self.service_name}-{exchange_name}"
        self.channel.queue_declare(queue=processing_queue_name, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=processing_queue_name)

        # error queue
        error_queue_name = f"{self.service_name}-{exchange_name}-error"
        self.channel.queue_declare(queue=error_queue_name, durable=True)

        def callback(ch, method, properties, body: str) -> None:  # noqa: ANN001, ARG001
            # convert message to type
            event_data = json.loads(body)
            event_instance = message_type(**event_data)
            # process
            try:
                func(event_instance)
            except Exception as e:
                logger.exception("Failed processing message")
                if not self.channel:
                    raise

                exception_info = {
                    "type": type(e).__name__,
                    "args": e.args,
                    "context": str(e.__context__),
                    "cause": str(e.__cause__),
                }

                exception_info_json = json.dumps(exception_info)

                self.channel.basic_publish(
                    exchange="",
                    routing_key=error_queue_name,
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        timestamp=math.floor(time.time()),
                        correlation_id=event_instance.correlation_id,
                        headers={
                            "exception": exception_info_json,
                        },
                    ),
                )

        self.channel.basic_consume(
            queue=processing_queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )

        self.channel.start_consuming()

    def publish(self, event: BaseEvent) -> None:
        """Publish a event as message."""
        if not self.channel:
            raise RabbitMQConnectionLostError

        exchange_name = f"{event.__module__}.{type(event).__name__}".lower()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        message = json.dumps(event.__dict__)

        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key="",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                timestamp=math.floor(time.time()),
                correlation_id=event.correlation_id,
            ),
        )
        logger.info(
            "Published message: %s",
            exchange_name,
            extra={
                "exchange_name": exchange_name,
                "event_body": message,
            },
        )
