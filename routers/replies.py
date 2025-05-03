from fastapi import APIRouter, HTTPException, Header, Body

from common.responses import BadRequest, Created
from services import reply_service
from security.jwt_auth import verify_access_token


replies_router = APIRouter(prefix='/replies', tags=['Replies'])

@replies_router.post("/{topic_id}", status_code=201)
def create_reply(
        topic_id: int,
        reply: str = Body(..., min_length=1, max_length=400),
        token: str = Header()
):
    # token verification
    payload = verify_access_token(token)

    # DB creator_id extract from token
    user_id = payload["id"]

    # insert reply in the DB
    if not reply_service.create_reply(reply, topic_id, user_id):
        return BadRequest(content="Invalid input parameters")
    else:
        return Created(content="Reply created successfully")


@replies_router.put("/{topic_id}/vote/{reply_id}", status_code=201)
def vote_on_reply(
        topic_id: int,
        reply_id: int,
        vote: str = Body(regex='^(-1|1)$'),
        token: str = Header()
):

    # token verification
    payload = verify_access_token(token)

    # DB creator_id extract from token
    user_id = payload["id"]

    if not reply_service.vote_on_r(topic_id, reply_id, user_id, vote):
        return BadRequest(content="Invalid input parameters")
    else:
        return Created(content="Vote was updated. Long live democracy!")


@replies_router.put("/{topic_id}/top/{reply_id}", status_code=201)
def mark_best_reply(
        topic_id: int,
        reply_id: int,
        token: str = Header()
):
    # token verification
    payload = verify_access_token(token)

    # DB creator_id extract from token
    user_id = payload["key"]["id"]

    if not reply_service.mark_best_reply(topic_id, reply_id, user_id):
        return BadRequest(content="Invalid input parameters")
    else:
        return Created(content="Best reply marked successfully")




