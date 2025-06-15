# Import the logging module.
import logging
from typing import Any

# Import the function to set the global logger provider from the OpenTelemetry logs module.
from opentelemetry._logs import set_logger_provider

# Import the OTLPLogExporter class from the OpenTelemetry gRPC log exporter module.
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# Import the LoggerProvider and LoggingHandler classes from the OpenTelemetry SDK logs module.
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler

# Import the BatchLogRecordProcessor class from the OpenTelemetry SDK logs export module.
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

# Import the Resource class from the OpenTelemetry SDK resources module.
from opentelemetry.sdk.resources import Resource

from .correlation_id import ctx_correlation_id


class InjectingFilter(logging.Filter):
    """
    A filter which injects context-specific information into logs
    """

    def filter(self, record: Any):
        if ctx_correlation_id.get() != "":
            record.correlation = f"[{ctx_correlation_id.get()}]"
        else:
            record.correlation = ""

        return True


class OtelLogger:
    """
    Sets up logging with specified service name, environment and filter for correlation ID
    """

    def __init__(
        self,
        service_name: str,
        service_environment: str,
        otel_host: str,
        otel_port: int,
    ):
        self.service_name = service_name
        self.otel_host = otel_host
        self.otel_port = otel_port

        self.logger_provider: LoggerProvider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": service_name,
                    "service.environment": service_environment,
                }
            )
        )

    def get_handler(self):
        # Set the created LoggerProvider as the global logger provider.
        set_logger_provider(self.logger_provider)

        # Create an instance of OTLPLogExporter with insecure connection.
        exporter = OTLPLogExporter(
            endpoint=f"{self.otel_host}:{self.otel_port}", insecure=True
        )

        # Add a BatchLogRecordProcessor to the logger provider with the exporter.
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        # Create a LoggingHandler with the specified logger provider and log level set to NOTSET.
        handler = LoggingHandler(
            level=logging.NOTSET, logger_provider=self.logger_provider
        )

        formatter = logging.Formatter(
            f"%(correlation)s [{self.service_name}] ::: %(message)s"
        )
        handler.setFormatter(formatter)

        handler.addFilter(InjectingFilter())

        return handler
