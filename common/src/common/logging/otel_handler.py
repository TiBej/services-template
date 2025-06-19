import logging
from typing import Any, override

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource


class OtelHandler(logging.Handler):
    """Handler that that wrapps opentelemetry.sdk._logs.LoggingHandler."""

    def __init__(
        self,
        service_name: str,
        service_environment: str,
        otel_host: str,
        otel_port: int,
    ) -> None:
        """Set up handler."""
        super().__init__()
        self.service_name = service_name
        self.otel_host = otel_host
        self.otel_port = otel_port

        self.logger_provider: LoggerProvider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": service_name,
                    "deployment.environment": service_environment,
                },
            ),
        )
        set_logger_provider(self.logger_provider)

        exporter = OTLPLogExporter(
            endpoint=f"{self.otel_host}:{self.otel_port}",
            insecure=True,  # otel_host is expected to be in the same private network
        )

        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        self.logger_handler = LoggingHandler(
            self.level,
            logger_provider=self.logger_provider,
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Send log to OTEL."""
        self.logger_handler.emit(record)

    @override
    def addFilter(self, filter: Any) -> None:
        """Override of default method to add filter to otel handler."""
        super().addFilter(filter)
        if filter not in self.logger_handler.filters:
            self.logger_handler.filters.append(filter)

    @override
    def setFormatter(self, fmt: logging.Formatter | None) -> None:
        """Override of default method to add formatter to otel handler."""
        super().setFormatter(fmt)
        self.logger_handler.formatter = fmt
