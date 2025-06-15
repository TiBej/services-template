# pyright: standard

import json
import logging
import time
from typing import Callable, Type, TypeVar

import pika

from common.models.events.base_event import BaseEvent

logger = logging.getLogger(__name__)


class RabbitMQ:
    T = TypeVar("T", bound=BaseEvent)

    def __init__(
        self, service_name: str, user: str, password: str, host: str, port: int
    ):
        self.service_name = service_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            connection_attempts=3,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, message_type: Type[T], func: Callable[[T], None]):
        if not self.channel:
            raise Exception("Connection is not established.")

        exchange_name = f"{message_type.__module__}.{message_type.__name__}".lower()

        self.channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        # processing queue
        processing_queue_name = f"{self.service_name}-{exchange_name}"
        self.channel.queue_declare(queue=processing_queue_name, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=processing_queue_name)

        # error queue
        error_queue_name = f"{self.service_name}-{exchange_name}-error"
        self.channel.queue_declare(queue=error_queue_name, durable=True)

        def callback(ch, method, properties, body: str):
            # convert message to type
            event_data = json.loads(body)
            event_instance = message_type(**event_data)
            # process
            try:
                func(event_instance)
            except Exception as e:
                logger.exception(f"failed processing message: {e}")
                if not self.channel:
                    raise Exception("Connection is not established.")

                exception_info = {
                    "type": e.__class__.__name__,
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
                        timestamp=int(time.time()),
                        correlation_id=event_instance.correlation_id,
                        headers={
                            "exception": exception_info_json,
                        },
                    ),
                )

        self.channel.basic_consume(
            queue=processing_queue_name, on_message_callback=callback, auto_ack=True
        )

        self.channel.start_consuming()

    def publish(self, event: BaseEvent):
        if not self.channel:
            raise Exception("Connection is not established.")

        exchange_name = f"{event.__module__}.{event.__class__.__name__}".lower()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        message = json.dumps(event.__dict__)

        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key="",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                timestamp=int(time.time()),
                correlation_id=event.correlation_id,
            ),
        )
        logger.info(f"published message: {message}")
