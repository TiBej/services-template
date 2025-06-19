class RabbitMQConnectionLostError(Exception):
    """Exception raised when the RabbitMQ connection is lost."""

    def __init__(self, message: str = "RabbitMQ connection lost.") -> None:
        """Init Exception."""
        super().__init__(message)
        self.message = message
