from common.events.mail_triggered import MailTriggeredEvent
from common.logging.logging_setup import setup_logging
from common.rabbitmq.rabbitmq_setup import setup_rabbitmq

from consumers.mail_triggered_event_consumer import MailTriggeredEventConsumer

setup_logging()
rabbitmq = setup_rabbitmq()


def main():
    consumer = MailTriggeredEventConsumer(MailTriggeredEvent, rabbitmq)
    consumer.start_consuming()
    print("Started Service")


if __name__ == "__main__":
    main()
