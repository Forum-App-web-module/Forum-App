from fastapi import APIRouter, Response, Header, Body
from services import topic_service, reply_service
from security.jwt_auth import verify_access_token

topic_router = APIRouter(prefix='/topics', tags=["Topics"])

# create a new topic
@topic_router.post('/')
def create_topic(
    title: str = Body(..., min_length=1, max_length=200), 
    category_id: int = Body(...), 
    token: str = Header()
    ):
    payload = verify_access_token(token)
    
    author_id = payload['id']
    new_id = topic_service.create_topic(title, category_id, author_id)

    if new_id:
        return Response(content=f'{"message":"Topic {title} created"}', status_code=201)
    return Response(content="Failed to create topic", status_code=500)  #fix status code

#view all topics, no authentication needed
@topic_router.get('/')
def view_topics():
    topics = topic_service.get_all_topics()
    if not topics:
        return Response(content='{"messgae":"No topics found"}', status_code=404)
    
    return topics

#view topic by id, show replies
@topic_router.get('/{topic_id}')
def view_topic_by_id(topic_id: int):
    topic_replies = topic_service.get_topic_with_replies(topic_id)
    if not topic_replies: 
        return Response(content='{"messgae":"No topic found for the given ID"}', status_code=404)
    
    return topic_replies

#create a reply for a topic, auth required
@topic_router.post('/{topic_id}/replies', status_code=201)
def create_reply(
    topic_id: int,
    text: str = Body(...,min_length=1, max_length=400),
        token: str = Header()
):
    payload = verify_access_token(token)
    
    user_id = payload['id']
    reply_service.create_reply(text, topic_id, user_id)

    return Response(content='{"messgae":"Reply created"}', status_code=201)
