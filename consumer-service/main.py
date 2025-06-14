import logging

from common.utilities.logging_fw import LoggingFW

logFW = LoggingFW(service_name="consumer-service")
handler = logFW.setup_logging()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)


def main():
    logging.info("hi")


if __name__ == "__main__":
    main()
