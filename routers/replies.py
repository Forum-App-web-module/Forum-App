from fastapi import APIRouter, HTTPException
from data.models import Replies
from services import reply_service

replies_router = APIRouter(prefix='/replies', tags=['Replies'])

@replies_router.post("/", status_code=201)
def create_reply(reply: Replies):
    # Develop token verification

    try:
        reply_service.create_reply(reply)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Reply created successfully"}









