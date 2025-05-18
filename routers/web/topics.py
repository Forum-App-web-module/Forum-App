from fastapi import APIRouter, Body, Header, Request, Form
from fastapi.responses import RedirectResponse

from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from services.category_service import is_private
from services.topic_service import get_topic_with_replies, get_category_id, create_topic
from services.reply_service import create_reply
from services.category_members_service import is_member

topic_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")

def helper_serve_topic_replies(request: Request ,id: int, category_id, write_flag = True):
    topic_replies = get_topic_with_replies(id)

    if topic_replies is None:
        return RedirectResponse(url="/categories", status_code=302)
    
    return templates.TemplateResponse(
        request=request,
        name="prefixed/replies.html",
        context={
            "category_id": category_id,
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
            return helper_serve_topic_replies(request, topic_id, category_id)

    elif not category_is_private:
        return helper_serve_topic_replies(request, topic_id, category_id, write_flag = False)

    return RedirectResponse(url="/categories", status_code=302)

# create topic and first reply
@topic_router.post('/topics/new')
def create_new_topic(
    request: Request,
    title: str = Form(...),
    reply: str = Form(alias="content"),
    category_id: str = Form(...)
):
    # get user id
    payload = get_user_if_token(request)
    if payload:
        user_id = payload["key"]["id"]

        # insert_title
        new_topic_id = create_topic(title, int(category_id), user_id)

        # insert_reply
        create_reply(reply, new_topic_id, user_id)

    return RedirectResponse(url=f"/categories/{int(category_id)}/topics", status_code=302)

























