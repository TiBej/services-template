# pyright: standard

import json
import logging
from collections.abc import Callable
from dataclasses import asdict

import pika
import pika.spec
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from retry import retry

from common.events.base_event import BaseEvent

logger = logging.getLogger(__name__)


# RT = response type, CT = consumer type
class RPCHandler[RT: BaseEvent, CT: BaseEvent]:
    """Connection & Communication with RabbitMQ."""

    def __init__(
        self,
        connection_parameter: pika.ConnectionParameters,
        response_type: type[RT],
        consume_type: type[CT],
    ) -> None:
        """Initialize & start connection."""
        self.connection_parameter = connection_parameter
        self.response_type = response_type

        consume_part = f"{consume_type.__module__}.{consume_type.__name__}"
        response_part = f"{response_type.__module__}.{response_type.__name__}"
        self.queue_name = f"{consume_part}-{response_part}".lower()

    @retry(AMQPConnectionError, backoff=1, max_delay=4, logger=logger)
    def _server_reply(
        self,
        response_json: str,
        reply_to: str,
        delivery_tag: int,
    ) -> None:
        """Send the reply for the request."""
        with pika.BlockingConnection(self.connection_parameter) as conn:
            channel = conn.channel()
            channel.basic_publish("", routing_key=reply_to, body=response_json)
            channel.basic_ack(delivery_tag=delivery_tag)

    @retry(AMQPConnectionError, backoff=1, max_delay=4, logger=logger)
    def send(self, request: CT) -> None:
        """Send a request to rabbitmq & get a direct reply."""
        with pika.BlockingConnection(self.connection_parameter) as conn:
            channel = conn.channel()
            request_json = json.dumps(asdict(request))

            def just_do_something_callback(
                ch: BlockingChannel,
                method: pika.spec.Basic.Deliver,  # noqa: ARG001
                properties: pika.spec.BasicProperties,  # noqa: ARG001
                body: str,
            ) -> None:
                event_data = json.loads(body)
                event_instance = self.response_type(**event_data)
                logger.info(event_instance.correlation_id)
                ch.close()

            channel.basic_consume(
                "amq.rabbitmq.reply-to", just_do_something_callback, auto_ack=True
            )
            channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=request_json,
                properties=pika.BasicProperties(reply_to="amq.rabbitmq.reply-to"),
            )

            channel.start_consuming()

    def consume(self, consume_type: type[CT], func: Callable[[CT], RT]) -> None:
        """Consume requests."""
        with pika.BlockingConnection() as conn:
            channel = conn.channel()

            def callback(
                ch: BlockingChannel,  # noqa: ARG001
                method: pika.spec.Basic.Deliver,
                properties: pika.spec.BasicProperties,
                body: str,
            ) -> None:
                if properties.reply_to is None:
                    logger.error("Received on reply to event without reply_to property")
                    return

                event_data = json.loads(body)
                event_instance = consume_type(**event_data)
                try:
                    response = func(event_instance)
                    request_json = json.dumps(asdict(response))
                    self._server_reply(
                        response_json=request_json,
                        reply_to=properties.reply_to,
                        delivery_tag=method.delivery_tag,
                    )

                except Exception:
                    logger.exception("Couldn't reply to request.")
                    if not channel:
                        self._server_reply(
                            response_json=body,
                            reply_to=properties.reply_to,
                            delivery_tag=method.delivery_tag,
                        )

            channel.queue_declare(
                queue=self.queue_name, exclusive=True, auto_delete=True
            )
            channel.basic_consume(self.queue_name, callback)
