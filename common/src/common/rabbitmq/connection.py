# pyright: standard

import json
import logging
import math
import time
from collections.abc import Callable

import pika
from pika.exceptions import AMQPConnectionError
from retry import retry

from common.events.base_event import BaseEvent

logger = logging.getLogger(__name__)


class Connection:
    """Connection & Communication with RabbitMQ."""

    def __init__(
        self, connection_parameter: pika.ConnectionParameters, service_name: str
    ) -> None:
        """Initialize & start connection."""
        self.connection_parameter = connection_parameter
        self.service_name = service_name
        self.conn = None

    def _get_connection(self) -> pika.BlockingConnection:
        if self.conn is None or self.conn.is_closed:
            self.conn = pika.BlockingConnection(self.connection_parameter)
        return self.conn

    @retry(AMQPConnectionError, backoff=2, max_delay=512, logger=logger)
    def publish(self, event: BaseEvent) -> None:
        """Publish a event as message."""
        exchange_name = f"{event.__module__}.{type(event).__name__}".lower()
        channel = self._get_connection().channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        message = json.dumps(event.__dict__)

        channel.basic_publish(
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

    @retry(AMQPConnectionError, backoff=2, max_delay=512, logger=logger)
    def consume[B: BaseEvent](
        self,
        message_type: type[B],
        func: Callable[[B], None],
    ) -> None:
        """Consume Event."""
        exchange_name = f"{message_type.__module__}.{message_type.__name__}".lower()
        channel = self._get_connection().channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        # processing queue
        processing_queue_name = f"{self.service_name}-{exchange_name}"
        channel.queue_declare(queue=processing_queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=processing_queue_name)

        # error queue
        error_queue_name = f"{self.service_name}-{exchange_name}-error"
        channel.queue_declare(queue=error_queue_name, durable=True)

        def callback(ch, method, properties, body: str) -> None:  # noqa: ANN001, ARG001
            # convert message to type
            event_data = json.loads(body)
            event_instance = message_type(**event_data)
            # process
            try:
                func(event_instance)
            except Exception as e:
                logger.exception("Failed processing message")
                if not channel:
                    raise

                exception_info = {
                    "type": type(e).__name__,
                    "args": e.args,
                    "context": str(e.__context__),
                    "cause": str(e.__cause__),
                }

                exception_info_json = json.dumps(exception_info)

                channel.basic_publish(
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

        channel.basic_consume(
            queue=processing_queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )

        channel.start_consuming()
