from fastapi import APIRouter, HTTPException, Header, Body
from services import reply_service
from jose import JWTError
from security.jwt_auth import verify_access_token


replies_router = APIRouter(prefix='/replies', tags=['Replies'])

@replies_router.post("/{topic_id}", status_code=201)
def create_reply(topic_id: int, reply: str = Body(..., min_length=1, max_length=400), token: str = Header()):
    # token verification
    try:
        payload = verify_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # DB creator_id extract from token
    user_id = payload["id"]

    # insert reply in the DB
    try:
        reply_service.create_reply(reply, topic_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Reply created successfully"}

@replies_router.post("/{topic_id}/vote/{reply_id}", status_code=201)
def vote_on_reply(topic_id: int, reply_id: int, vote: str = Body(regex='^(-1|1)$'), token: str = Header()):
    # token verification
    try:
        payload = verify_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # DB creator_id extract from token
    user_id = payload["key"]["id"]

    try:
        result = reply_service.vote_on_r(topic_id, reply_id, user_id, vote)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if result:
        return {"message": "Vote was updated. Long live democracy!"}










