import os

from common.rabbitmq.rabbitmq import RabbitMQ


def setup_rabbitmq():
    """
    Setup RabbitMQ
    """
    rabbitmq = RabbitMQ(
        service_name=os.getenv("SERVICE_NAME", "default-service"),
        user=os.getenv("RABBITMQ_USER", "admin"),
        password=os.getenv("RABBITMQ_PASSWORD", "admin"),
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", 5672)),
    )
    return rabbitmq
