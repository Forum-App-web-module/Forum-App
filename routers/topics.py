from fastapi import APIRouter, Response
from services import topic_service

topic_router = APIRouter(prefix='/topics', tags=["Topics"])

@topic_router.get('/')
def view_topics():
    topics = topic_service.get_all_topics()
    if not topics:
        return Response(content='{"messgae":"No topics found"}', status_code=404)
    
    return topics

@topic_router.get('/{topic_id}')
def view_topic_by_id(topic_id: int):
    topic = topic_service.get_topic_by_id(topic_id)
    if not topic: 
        return Response(content='{"messgae":"No topic found for the given ID"}', status_code=404)
    
    return topic
