from fastapi import APIRouter, Body, Header, Request, Form
from typing import Optional

from fastapi.templating import Jinja2Templates

from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from security.jwt_auth import verify_access_token
from services.category_service import get_all_public, get_all, get_allowed, get_topics_by_category, is_private
from services.topic_service import get_all_topics, get_topic_with_replies
from services.category_members_service import is_member
from fastapi.responses import RedirectResponse

category_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")


@category_router.get('/categories')
def serve_categories(request: Request):
    # token authentication
    payload = get_user_if_token(request)

    if not payload:
        categories = get_all_public()
        return templates.TemplateResponse(request=request, name="prefixed/categories.html",context={"categories": categories})

    if payload["key"]["is_admin"]:
        categories = get_all()
        return templates.TemplateResponse(request=request, name="prefixed/categories.html", context={"categories": categories})
    else:
        categories = get_allowed(payload["key"]["id"])
        return templates.TemplateResponse(request=request, name="prefixed/categories.html", context={"categories": categories})

# View topics for a category
@category_router.get('/categories/{category_id}/topics')
def serve_category_topics(request: Request, category_id: int):
    # token authentication
    payload = get_user_if_token(request)

    if not payload:
        if not is_private(category_id):
            topics = get_topics_by_category(category_id)
            return templates.TemplateResponse(request=request, name="prefixed/topics.html",context={"topics": topics})

    if payload["key"]["is_admin"] or is_member(category_id, payload["key"]["id"]):
        topics = get_topics_by_category(category_id)
        return templates.TemplateResponse(request=request, name="prefixed/topics.html",context={"topics": topics})
    else:
        response = RedirectResponse(url="/categories", status_code=302)
        return response


# View replies for a topic
@category_router.get('/categories/{category_id}/topics/{topic_id}/replies')
def serve_topic_replies(request: Request, category_id: int, topic_id: int):
    payload = get_user_if_token(request)

    if not payload:
        if not is_private(category_id):
            replies = get_topic_with_replies(topic_id)
            if replies is None:
                return None # templates.TemplateResponse something
            
            return templates.TemplateResponse(
                request=request,
                name="prefixed/replies.html",
                context={
                    "request": request,
                    "topic": replies["topic"],
                    "replies": replies["replies"],
                    "msg": None
                }
            )
        else:
            return RedirectResponse(url="/categories", status_code=302)
        
    if payload["key"]["is_admin"] or is_member(category_id, payload["key"]["id"]):
        replies = get_topic_with_replies(topic_id)
        if replies is None:
            return None # templates.TemplateResponse something
        
        return templates.TemplateResponse(
            request=request,
            name="prefixed/replies.html",
            context={
                "request": request,
                "topic": replies["topic"],
                "replies": replies["replies"],
                "msg": None
            }
        )
    else:
        return RedirectResponse(url="/categories", status_code=302)



# #view topic by id, show replies
# @topic_router.get('/{topic_id}')
# def view_topic_by_id(topic_id: int):
#     topic_replies = topic_service.get_topic_with_replies(topic_id)
#     if not topic_replies: 
#         return NotFound(content="No topic found for the given ID")
    
#     return topic_replies

# @category_router.get('/{category_id}/topics')
# def view_category_topics(category_id: int, token: str = Header()):
#     payload = verify_access_token(token)

#     user_id = payload["key"]["id"]

#     category = category_service.get_category_by_id(category_id)
#     if not category:
#         return NotFound(content="No category found with this ID")
#     if category.is_private:

#         if not category_members_service.is_member(category_id, user_id):
#             return Unauthorized(content="This category is private, you are not a member.")

#     topics = category_service.get_topics_by_category(category_id)
#     if not topics:
#         return NoContent(content="No topics found for this category")

#     return topics

# Lock Category
@category_router.put('/{category_id}/lock')
def lock_the_category(request: Request, category_id: int, category: str = Form(...), action: int = Form(...)):
    payload = get_user_if_token(request)
    # Admin authorization returns an error or None
    if payload and payload["key"]["is_admin"] == True:
        lock_category(category_id, action)
        return Created(content=f'Category {category_id} locked')
