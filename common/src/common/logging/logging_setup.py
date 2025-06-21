import logging
import logging.config

from common.config.base_config import BaseConfig


def setup_logging(config: BaseConfig) -> None:
    """Configure basic logging."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "otel": {
                "format": f"[%(correlation_id)s] [{config.service_name}] :: %(message)s"
            },
            "simple": {"format": "%(levelname)s: %(message)s"},
        },
        "filters": {
            "correlation_id_filter": {
                "()": "common.logging.correlation_id.CorrelationIdFilter",
            },
        },
        "handlers": {
            "otel": {
                "()": "common.logging.otel_handler.OtelHandler",
                "filters": ["correlation_id_filter"],
                "formatter": "otel",
                "service_name": config.service_name,
                "service_environment": config.service_environment,
                "otel_host": config.otel_host,
                "otel_port": config.otel_port,
            },
            "stdrr": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {"root": {"handlers": ["otel", "stdrr"], "level": "INFO"}},
    }

    logging.config.dictConfig(logging_config)
