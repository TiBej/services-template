import logging

from common.models.events.mail_triggered import MailTriggeredEvent
from common.utilities.logging_fw import LoggingFW

from consumers.mail_triggered_event_consumer import MailTriggeredEventConsumer

logFW = LoggingFW(service_name="consumer-service")
handler = logFW.setup_logging()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)


def main():
    logging.basicConfig(level=logging.INFO)  # Set up logging

    # Start Consuming MailTriggeredEvent
    consumer = MailTriggeredEventConsumer(MailTriggeredEvent)
    consumer.start_consuming()


if __name__ == "__main__":
    main()
