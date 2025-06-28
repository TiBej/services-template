import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from common.events.mail_triggered import MailTriggeredEvent
from common.events.user_reponse_event import UserResponseEvent
from common.events.user_request_event import UserRequestEvent
from common.rabbitmq.rabbitmq import RabbitMQ

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/user/{user_id}", tags=["users"])
async def get_user(
    user_id: str,
    rabbitmq: Annotated[RabbitMQ, Depends()],
) -> dict[str, str]:
    """Get user by id."""
    logger.info("random log, to showcase the logging system")
    triggered_event = UserRequestEvent(id=int(user_id))
    with rabbitmq.rpc_handler(UserResponseEvent, UserRequestEvent) as rpc_handler:
        rpc_handler.send(triggered_event)
        return {"id": user_id}


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
    with rabbitmq.handler() as handler:
        handler.publish(triggered_event)
        return {"username": username}
