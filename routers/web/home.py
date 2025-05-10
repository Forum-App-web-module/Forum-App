from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx


index_router = APIRouter(prefix='')
templates = Jinja2Templates(directory="templates")

GNEWS_API_KEY = "ee81d4c6bf5f7583160aec788147a75f"
GNEWS_ENDPOINT = "https://gnews.io/api/v4/top-headlines?lang=en&token=" + GNEWS_API_KEY

@index_router.get('/home')
def serve_index(request: Request):
    with httpx.Client() as client:
        response = client.get(GNEWS_ENDPOINT)
        news_data = response.json().get("articles", [])
    return templates.TemplateResponse("index.html", {"request": request, "news": news_data})
