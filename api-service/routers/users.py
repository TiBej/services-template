import logging

from common.models.events.mail_triggered import MailTriggeredEvent
from fastapi import APIRouter

from rabbitmq import RabbitMQ

router = APIRouter()


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    logging.info("bug is incoming")
    logging.critical("critical message")
    logging.error("Triggering bug...")
    rabbitmq = RabbitMQ()
    triggeredEvent = MailTriggeredEvent(
        subject="test", body="test", recipient_email="test"
    )
    rabbitmq.publish(triggeredEvent)
    return {"username": username}
