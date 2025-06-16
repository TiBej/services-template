import logging
import os

from common.logging.otel_logger import OtelLogger


def setup_logging():
    """
    Setup root logger & attaches open telemetry handler
    """
    otel_logger = OtelLogger(
        service_environment=os.getenv("SERVICE_ENVIRONMENT", "development"),
        service_name=os.getenv("SERVICE_NAME", "default-service"),
        otel_host=os.getenv("OTEL_HOST", "localhost"),
        otel_port=int(os.getenv("OTEL_PORT", 4317)),
    )
    handler = otel_logger.get_handler()

    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)
