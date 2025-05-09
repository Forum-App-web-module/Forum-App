from fastapi import FastAPI
import uvicorn
from routers.api.messages import message_router
from routers.api.replies import replies_router
from routers.api.users import user_router
from routers.api.categories import category_router
from routers.api.topics import topic_router
from fastapi.staticfiles import StaticFiles

# from routers.web.categories import category_router
# from routers.web.messages import message_router
# from routers.web.replies import replies_router
# from routers.web.topics import topic_router
from routers.web.users import user_router

app = FastAPI()

app.include_router(message_router)
app.include_router(user_router)
app.include_router(replies_router)
app.include_router(category_router)
app.include_router(topic_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)