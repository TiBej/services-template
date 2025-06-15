import logging

from common.models.events.mail_triggered import MailTriggeredEvent
from common.utilities.rabbitmq import RabbitMQ
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str, rabbitmq: RabbitMQ = Depends()):
    logging.info("bug is incoming")
    logging.critical("critical message")
    logging.error("Triggering bug...")
    triggeredEvent = MailTriggeredEvent(
        subject="test", body="test", recipient_email="test"
    )
    rabbitmq.publish(triggeredEvent)
    return {"username": username}
