import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from common.events.mail_triggered import MailTriggeredEvent
from common.rabbitmq.rabbitmq import RabbitMQ

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/users/{username}", tags=["users"])
async def read_user(
    username: str,
    rabbitmq: Annotated[RabbitMQ, Depends()],
) -> dict[str, str]:
    """Get user by name."""
    logger.info("random log, to showcase the logging system")
    triggered_event = MailTriggeredEvent(
        subject="test",
        body="test",
        recipient_email="test",
    )
    with rabbitmq.connection() as connection:
        connection.publish(triggered_event)
        return {"username": username}
