import os
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class BaseConfig:
    """Base configuration class for common service settings."""

    # general
    service_name: str = field(
        default_factory=lambda: os.getenv("SERVICE_NAME", "default-service"),
    )
    service_environment: str = field(
        default_factory=lambda: os.getenv("SERVICE_ENVIRONMENT", "development"),
    )

    # rabbitmq
    rabbitmq_user: str = field(
        default_factory=lambda: os.getenv("RABBITMQ_USER", "admin"),
    )
    rabbitmq_password: str = field(
        default_factory=lambda: os.getenv("RABBITMQ_PASSWORD", "admin"),
    )
    rabbitmq_host: str = field(
        default_factory=lambda: os.getenv("RABBITMQ_HOST", "localhost"),
    )
    rabbitmq_port: int = field(
        default_factory=lambda: int(os.getenv("RABBITMQ_PORT", "5672")),
    )

    # logging
    otel_host: str = field(default_factory=lambda: os.getenv("OTEL_HOST", "localhost"))
    otel_port: int = field(default_factory=lambda: int(os.getenv("OTEL_PORT", "4317")))
