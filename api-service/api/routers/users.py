import logging

from common.events.mail_triggered import MailTriggeredEvent
from common.rabbitmq.rabbitmq import RabbitMQ
from fastapi import APIRouter, Depends

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str, rabbitmq: RabbitMQ = Depends()):
    logger.info("bug is incoming")
    logger.critical("critical message")
    logger.error("Triggering bug...")
    triggeredEvent = MailTriggeredEvent(
        subject="test", body="test", recipient_email="test"
    )
    rabbitmq.publish(triggeredEvent)
    return {"username": username}
