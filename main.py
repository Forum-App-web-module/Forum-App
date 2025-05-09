from fastapi import FastAPI
import uvicorn
from routers.api.messages import message_router
from routers.api.replies import replies_router
from routers.api.users import user_router
from routers.api.categories import category_router
from routers.api.topics import topic_router

app = FastAPI()

app.include_router(message_router)
app.include_router(user_router)
app.include_router(replies_router)
app.include_router(category_router)
app.include_router(topic_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)