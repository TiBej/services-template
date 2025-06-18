from consumers.mail_triggered_event_consumer import MailTriggeredEventConsumer

from common.config.base_config import BaseConfig
from common.events.mail_triggered import MailTriggeredEvent
from common.logging.logging_setup import setup_logging
from common.rabbitmq.rabbitmq import RabbitMQ

config = BaseConfig()
setup_logging(config)
rabbitmq = RabbitMQ(config)


def main():
    consumer = MailTriggeredEventConsumer(MailTriggeredEvent, rabbitmq)
    consumer.start_consuming()
    print("Started Service")


if __name__ == "__main__":
    main()
