import logging
import os

from common.models.events.mail_triggered import MailTriggeredEvent
from common.utilities.logging_fw import LoggingFW
from common.utilities.rabbitmq import RabbitMQ

from consumers.mail_triggered_event_consumer import MailTriggeredEventConsumer

loggingFW = LoggingFW(
    service_environment=os.getenv("SERVICE_ENVIRONMENT", "development"),
    service_name=os.getenv("SERVICE_NAME", "consumer-service"),
    otel_host=os.getenv("OTEL_HOST", "localhost"),
    otel_port=int(os.getenv("OTEL_PORT", 4317)),
)
handler = loggingFW.get_handler()

rabbitmq = RabbitMQ(
    service_name=os.getenv("SERVICE_NAME", "consumer-service"),
    user=os.getenv("RABBITMQ_USER", "admin"),
    password=os.getenv("RABBITMQ_PASSWORD", "admin"),
    host=os.getenv("RABBITMQ_HOST", "localhost"),
    port=int(os.getenv("RABBITMQ_PORT", 5672)),
)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)


def main():
    consumer = MailTriggeredEventConsumer(MailTriggeredEvent, rabbitmq)
    consumer.start_consuming()
    print("Started Service")


if __name__ == "__main__":
    main()
