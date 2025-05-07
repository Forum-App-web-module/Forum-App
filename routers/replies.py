from fastapi import APIRouter, HTTPException, Header, Body
from typing import Literal

from common.responses import BadRequest, Created
from services import reply_service, category_service, category_members_service, topic_service
from security.jwt_auth import verify_access_token
from security.authorization import admin_auth


replies_router = APIRouter(prefix='/replies', tags=['Replies'])

def user_has_access(payload, topic_id, category_id=None):
    user_id = payload["key"]["id"]
    if not category_id:
        category_id = topic_id  # failsafe for now but should we develop topic_service.is_private()
    if not category_service.is_private(category_id):
        return True
    if category_members_service.is_member(topic_id, user_id):
        return True
    if admin_auth(payload):
        return True
    return False


@replies_router.post("/{topic_id}", status_code=201)
def create_reply(topic_id: int, reply: str = Body(..., min_length=1, max_length=400), token: str = Header()):
    payload = verify_access_token(token)
    user_id = payload["key"]["id"]
    category_id = topic_service.get_category_id(topic_id)

    if category_service.is_locked(topic_id):
        return BadRequest(content="This topic is locked")

    if user_has_access(payload, topic_id, category_id):
        reply_service.create_reply(reply, topic_id, user_id)
        return Created(content="Reply created successfully")

    return BadRequest(content="Access  restricted. Contact an Admin.")


@replies_router.put("/{topic_id}/vote/{reply_id}", status_code=201)
def vote_on_reply(topic_id: int, reply_id: int, vote: Literal[-1, 1] = Body(...), token: str = Header()):
    payload = verify_access_token(token)
    user_id = payload["key"]["id"]

    try:
        reply_service.validate_topic_and_reply(topic_id, reply_id)
    except ValueError as e:
        return BadRequest(content=str(e))

    if user_has_access(payload, topic_id):
        reply_service.vote_to_db(reply_id, user_id, vote)
        return Created(content="Vote was updated. Long live democracy!")

    return BadRequest(content="This topic is locked")


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



# @replies_router.post("/{topic_id}", status_code=201)
# def create_reply(
#         topic_id: int,
#         reply: str = Body(..., min_length=1, max_length=400),
#         token: str = Header()
# ):
#     # token verification
#     payload = verify_access_token(token)
#
#     # DB creator_id extract from token
#     user_id = payload["key"]["id"]
#     category_id = topic_service.get_category_id(topic_id)
#
#     # check Category lock
#     if not category_service.is_locked(topic_id):
#         category_is_private = category_service.is_private(category_id)
#         # check category privacy and user membership
#         if category_is_private and category_members_service.is_member(topic_id, user_id):
#             reply_service.create_reply(reply, topic_id, user_id)
#             return Created(content="Reply created successfully")
#         # private category and user is Admin
#         elif category_is_private and admin_auth(payload):
#             reply_service.create_reply(reply, topic_id, user_id)
#             return Created(content="Reply created successfully")
#         # directly create reply when not a private category
#         elif not category_is_private:
#             reply_service.create_reply(reply, topic_id, user_id)
#             return Created(content="Reply created successfully")
#     else:
#         return BadRequest(content="This topic is locked")
#
#
#
# @replies_router.put("/{topic_id}/vote/{reply_id}", status_code=201)
# def vote_on_reply(
#         topic_id: int,
#         reply_id: int,
#         vote: Literal[-1,1] = Body(...),
#         token: str = Header()
# ):
#
#     # token verification
#     payload = verify_access_token(token)
#
#     # DB creator_id extract from token
#     user_id = payload["key"]["id"]
#
#     # validate reply belongs to topic
#     try:
#         reply_service.validate_topic_and_reply(topic_id, reply_id)
#     except ValueError as e:
#         return BadRequest(content=str(e))
#
#     category_is_private = category_service.is_private(topic_id)
#     # check privacy and user membership
#     if category_is_private and category_members_service.is_member(user_id, topic_id):
#         reply_service.vote_to_db(reply_id, user_id, vote)
#         return Created(content="Vote was updated. Long live democracy!")
#     # private category and user is Admin
#     elif category_is_private and admin_auth(payload):
#         reply_service.vote_to_db(reply_id, user_id, vote)
#         return Created(content="Vote was updated. Long live democracy!")
#     # update vote when not private
#     elif not category_is_private:
#         reply_service.vote_to_db(reply_id, user_id, vote)
#         return Created(content="Vote was updated. Long live democracy!")
#     # can't vote - not a member and category is private
#     else:
#         return BadRequest(content="This topic is locked")







