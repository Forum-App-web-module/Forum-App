from fastapi import APIRouter, Header, Body
from typing import Literal

from security.authorization import admin_auth
from services import topic_service, reply_service
from security.jwt_auth import verify_access_token
from common.responses import NotFound, Created
from routers.api.replies import create_reply as replies_create_reply

topic_router = APIRouter(prefix='/api/topics', tags=["Topics"])

# create a new topic
@topic_router.post('/')
def create_topic(
    title: str = Body(..., min_length=1, max_length=200), 
    category_id: int = Body(...), 
    token: str = Header()
    ):
    payload = verify_access_token(token)
    
    author_id = payload["key"]['id']
    new_id = topic_service.create_topic(title, category_id, author_id)

    if new_id:
        return Created(content=f'Topic {title} created')

#view all topics, no authentication needed
@topic_router.get('/')
def view_topics():
    topics = topic_service.get_all_topics()
    if not topics:
        return NotFound(content="No topics found")
    
    return topics

#view topic by id, show replies
@topic_router.get('/{topic_id}')
def view_topic_by_id(topic_id: int):
    topic_replies = topic_service.get_topic_with_replies(topic_id)
    if not topic_replies: 
        return NotFound(content="No topic found for the given ID")
    
    return topic_replies

#create a reply for a topic, auth required
@topic_router.post('/{topic_id}/replies', status_code=201)
def create_reply(
    topic_id: int,
    text: str = Body(...,min_length=1, max_length=400),
    token: str = Header()
):
    return replies_create_reply(topic_id, text, token)

# lock topic
@topic_router.put('/{topic_id}/lock', status_code=201)
def lock_topic(
    topic_id: int,
    lock: Literal[0,1] = Body(...),
    token: str = Header()
):
    payload = verify_access_token(token)

    # Admin authorization returns an error or None
    if admin_auth(payload):
        # call service
        topic_service.update_topic(topic_id, lock)
        if lock:
            return Created(content= f'Topic {topic_id} was locked')
        else:
            return Created(content= f'Topic {topic_id} was unlocked')




