from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx
from common.template_config import CustomJinja2Templatges
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path="key_example.env")
GNEWS_API_KEY = getenv("GNEWS_API_KEY")

index_router = APIRouter(prefix='')
templates = CustomJinja2Templatges(directory="templates")

GNEWS_ENDPOINT = "https://gnews.io/api/v4/top-headlines?lang=en&token=" + GNEWS_API_KEY

@index_router.get('/home')
def serve_index(request: Request):
    with httpx.Client() as client:
        response = client.get(GNEWS_ENDPOINT)
        news_data = response.json().get("articles", [])
    return templates.TemplateResponse("index.html", {"request": request, "news": news_data})

@index_router.get('/policy')
def serve_policy(request: Request):
    return templates.TemplateResponse(name = "admin_privacy/privacy_policy.html", request=request)

@index_router.get('/logout')
def serve_logout(request: Request):
    response = RedirectResponse(url="/home", status_code=302)
    response.delete_cookie('token')
    return response

@index_router.get('/admin')
def serve_policy(request: Request):
    return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request)











