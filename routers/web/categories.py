from fastapi import APIRouter, Body, Header, Request, Form, Query
from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from services.category_service import (get_all_public, get_all, get_allowed, get_topics_by_category,
            is_private, get_category_by_name, lock_category, create_category, count_topics_by_category)
from services.topic_service import get_all_topics, get_topic_with_replies
from services.category_members_service import is_member
from fastapi.responses import RedirectResponse
from security.authorization import admin_auth

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
def serve_category_topics(
    request: Request,
    category_id: int,
    search: str = Query(default="", alias="search"),
    sort_by: str = Query(default="title_asc", alias="sort"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=5, ge=1, le=100)
):
    skip = (page - 1) * per_page
    # token authentication
    payload = get_user_if_token(request)

    if not payload:
        if not is_private(category_id):
            topics = get_topics_by_category(category_id, search, sort_by, skip, per_page)
            total = count_topics_by_category(category_id, search)
            total_pages = (total + per_page - 1) // per_page
            return templates.TemplateResponse(
                request=request,
                name="prefixed/topics.html",
                context={
                    "topics": topics,
                    "category_id": category_id,
                    "search": search,
                    "sort_by": sort_by,
                    "page": page,
                    "per_page": per_page,
                    "total_pages": total_pages
                }
            )

    if payload or is_member(category_id, payload["key"]["id"]):
        topics = get_topics_by_category(category_id, search, sort_by, skip, per_page)
        total = count_topics_by_category(category_id, search)
        total_pages = (total + per_page - 1) // per_page
        return templates.TemplateResponse(
            request=request,
            name="prefixed/topics.html",
            context={
                "topics": topics,
                "category_id": category_id,
                "search": search,
                "sort_by": sort_by,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages
            }
        )


# View replies for a topic
# Duplicate of serve_topic in web\topics
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

# Lock Category

@category_router.post('/categories/lock')
def lock_the_category(request: Request, category_name: str = Form(...), action: int = Form(...)):
    payload = get_user_if_token(request)
    if not category_name:
        return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, context={"msg": f"Please input category name!", 'section': 'category'})
    # Admin authorization returns an error or None
    if payload and payload["key"]["is_admin"] == True:
        id = get_category_by_name(category_name)
        if not id:
            return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, context={"msg": f"Category doesn't exist!", 'section': 'category'})
        lock_category(id, action)
        return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, context={"msg": f"Category {category_name} is {'locked!' if action else 'unlocked!'}", 'section': 'category'})

# Create category
@category_router.post('/categories', status_code=201)
def create_categories(request: Request, category: str = Form(...)):
    payload = get_user_if_token(request)

    # Admin authorization returns an error or None
    if admin_auth(payload):
        # call service
        create_category(category)
        return templates.TemplateResponse(name = "admin_privacy/admin.html",
                                          request=request,
                                          context={"msg": f"Category {category} is created", 'section': 'create_category'})