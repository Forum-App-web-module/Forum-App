from fastapi import APIRouter, Body, Header, Request, Form
from fastapi.responses import RedirectResponse

from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from services.category_service import is_private
from services.topic_service import get_topic_with_replies, get_category_id
from services.reply_service import create_reply
from services.category_members_service import is_member

replies_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")


@replies_router.post('/replies/{topic_id}/new')
def upload_reply(
        request: Request,
        topic_id: int,
        content: str = Form(...),
    ):

    # token authentication
    payload = get_user_if_token(request)
    if payload:
        user_id = payload["key"]["id"]
        create_reply(content, topic_id, user_id)

    return RedirectResponse(url=f'/topic/{topic_id}', status_code=302)



