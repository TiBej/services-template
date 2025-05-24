import logging
from loggingfw import CustomLogFW

logFW = CustomLogFW(service_name='plant_service', instance_id='1')
handler = logFW.setup_logging()
logging.getLogger().addHandler(handler)

def main():
    print("Hello from main!")
    logging.info('this is an error log.')


if __name__ == "__main__":
    main()