from fastapi import APIRouter, Body, Header, Request, Form
from typing import Optional

from fastapi.templating import Jinja2Templates

from common.auth import get_user_if_token
from security.jwt_auth import verify_access_token
from services.category_service import get_all_public, get_all, get_allowed
from common.template_config import CustomJinja2Templatges

category_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")


@category_router.get('/categories')
def serve_categories(request: Request):
    # token authentication
    payload = get_user_if_token(request)

    if not payload:
        categories = get_all_public()
        return templates.TemplateResponse(request=request, name="/prefixed/categories.html",context={"categories": categories})

    if payload["key"]["is_admin"]:
        categories = get_all()
        return templates.TemplateResponse(request=request, name="/prefixed/categories.html", context={"categories": categories})
    else:
        categories = get_allowed(payload["key"]["id"])
        return templates.TemplateResponse(request=request, name="/prefixed/categories.html", context={"categories": categories})


