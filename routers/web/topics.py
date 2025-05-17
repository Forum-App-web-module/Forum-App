from fastapi import APIRouter, Body, Header, Request, Form
from fastapi.responses import RedirectResponse

from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from services.category_service import is_private
from services.topic_service import get_topic_with_replies, get_category_id
from services.category_members_service import is_member

topic_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")

def helper_serve_topic_replies(request: Request ,id: int, write_flag = True):
    topic_replies = get_topic_with_replies(id)
    return templates.TemplateResponse(
        request=request,
        name="prefixed/replies.html",
        context={
            "topic": topic_replies["topic"],
            "replies": topic_replies["replies"],
            "write_access": write_flag
        }
    )

# view topic by id, show replies
@topic_router.get('/topic/{topic_id}')
def serve_topic(request: Request, topic_id: int):
    payload = get_user_if_token(request)
    category_id = get_category_id(topic_id)
    category_is_private = is_private(category_id)

    if payload:
        user_id = payload["key"]["id"]
        is_admin = payload["key"]["is_admin"]
        is_cat_member = is_member(category_id, user_id)

        if is_admin or is_cat_member or not category_is_private:
            return helper_serve_topic_replies(request, topic_id)

    elif not category_is_private:
        return helper_serve_topic_replies(request, topic_id, write_flag = False)

    return RedirectResponse(url="/categories", status_code=302)

























