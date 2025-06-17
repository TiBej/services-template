import logging
from typing import Any, override

from opentelemetry._logs import set_logger_provider

# Import the OTLPLogExporter class from the OpenTelemetry gRPC log exporter module.
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# Import the LoggerProvider and LoggingHandler classes from the OpenTelemetry SDK logs module.
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler

# Import the BatchLogRecordProcessor class from the OpenTelemetry SDK logs export module.
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

# Import the Resource class from the OpenTelemetry SDK resources module.
from opentelemetry.sdk.resources import Resource


class OtelHandler(logging.Handler):
    """
    Logs to OpenTelemetry with wrapping opentelemetry.sdk._logs.LoggingHandler
    """

    def __init__(
        self,
        service_name: str,
        service_environment: str,
        otel_host: str,
        otel_port: int,
    ):
        logging.Handler.__init__(self)
        self.service_name = service_name
        self.otel_host = otel_host
        self.otel_port = otel_port

        self.logger_provider: LoggerProvider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": service_name,
                    "deployment.environment": service_environment,
                }
            )
        )
        set_logger_provider(self.logger_provider)

        # Create an instance of OTLPLogExporter with insecure connection.
        exporter = OTLPLogExporter(
            endpoint=f"{self.otel_host}:{self.otel_port}", insecure=True
        )

        # Add a BatchLogRecordProcessor to the logger provider with the exporter.
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        # Create a LoggingHandler with the specified logger provider and log level set to NOTSET.
        self.logger_handler = LoggingHandler(
            self.level, logger_provider=self.logger_provider
        )

    def emit(self, record: logging.LogRecord):
        self.logger_handler.emit(record)

    @override
    def addFilter(self, filter: Any):
        """
        override of default method to add filter to otel handler
        """
        super().addFilter(filter)
        if filter not in self.logger_handler.filters:
            self.logger_handler.filters.append(filter)

    @override
    def setFormatter(self, fmt: logging.Formatter | None):
        """
        override of default method to add formatter to otel handler
        """
        super().setFormatter(fmt)
        self.logger_handler.formatter = fmt
