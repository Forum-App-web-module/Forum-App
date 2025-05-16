from fastapi import APIRouter, Body, Header, Request, Form
from typing import Optional

from fastapi.templating import Jinja2Templates

from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from security.jwt_auth import verify_access_token
from services.category_service import get_all_public, get_all, get_allowed, get_topics_by_category
from services.topic_service import get_all_topics

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
def serve_category_topics(request: Request, category_id: int, token: str = Header()):
    # token authentication
    payload = get_user_if_token(request)

    if not payload:
        topics = get_topics_by_category(category_id)
        return templates.TemplateResponse(request=request, name="prefixed/topics.html",context={"topics": topics}



@category_router.get('/{category_id}/topics')
def view_category_topics(category_id: int, token: str = Header()):
    payload = verify_access_token(token)

    user_id = payload["key"]["id"]

    category = category_service.get_category_by_id(category_id)
    if not category:
        return NotFound(content="No category found with this ID")
    if category.is_private:

        if not category_members_service.is_member(category_id, user_id):
            return Unauthorized(content="This category is private, you are not a member.")

    topics = category_service.get_topics_by_category(category_id)
    if not topics:
        return NoContent(content="No topics found for this category")

    return topics

