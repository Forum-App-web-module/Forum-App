from fastapi import APIRouter, Body, Header, Request, Form
from common.template_config import CustomJinja2Templatges



topic_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")


@topic_router.get('/topic/{topic_id}')
def serve_topic(request: Request, topic_id: int):
    pass





















