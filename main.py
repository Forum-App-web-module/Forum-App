from fastapi import FastAPI
import uvicorn
from routers.api.messages import message_router as api_message_router
from routers.api.replies import replies_router as api_replies_router
from routers.api.users import user_router as api_user_router
from routers.api.categories import category_router as api_category_router
from routers.api.topics import topic_router as api_topic_router
from fastapi.staticfiles import StaticFiles

from routers.web.categories import category_router as web_category_router
from routers.web.messages import message_router as web_message_router
# from routers.web.replies import replies_router as web_replies_router
# from routers.web.topics import topic_router as web_topic_router
from routers.web.users import user_router as web_user_router
from routers.web.main import index_router as web_index_router

app = FastAPI()

app.include_router(api_message_router)
app.include_router(api_user_router)
app.include_router(api_replies_router)
app.include_router(api_category_router)
app.include_router(api_topic_router)

app.include_router(web_index_router)
app.include_router(web_message_router)
app.include_router(web_user_router)
# app.include_router(web_replies_router)
app.include_router(web_category_router)
# app.include_router(web_topic_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)