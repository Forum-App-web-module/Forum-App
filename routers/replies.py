from fastapi import APIRouter, HTTPException, Header, Body
from data.models import Replies
from services import reply_service
from jose import jwt, JWTError

SECRET_KEY = "A69"
ALGORITHM = "HS256"

replies_router = APIRouter(prefix='/replies', tags=['Replies'])

@replies_router.post("/{topic_id}", status_code=201)
def create_reply(topic_id: int, reply: str = Body(..., min_length=1, max_length=400), token: str = Header()): #token: str = Header()
    # Develop token verification
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = payload["key"]["id"]

    try:
        reply_service.create_reply(reply, topic_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Reply created successfully"}









