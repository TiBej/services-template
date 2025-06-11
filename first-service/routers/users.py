import logging

from fastapi import APIRouter

router = APIRouter()


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    logging.info("bug is incoming")
    logging.critical("critical message")
    logging.error("Triggering bug...")
    return {"username": username}
