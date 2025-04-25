from pydantic import BaseModel, constr, 
from datetime import datetime


class Messages(BaseModel):
    id: int | None
    text: str
    sent_on: datetime | None = datetime.now.strftime('%Y-%m-%d %H:%M:%S')

class Users(BaseModel):
    id: int | None
    username: constr(min_length=6, max_length=30)
    email: str
    password: constr(min_length=6, max_length=30)
    bio: str | None
    is_admin: bool | None = False
    is_active: bool | None = True

class Categories(BaseModel):
    pass

class Replies(BaseModel):
    pass

class Topics(BaseModel):
    pass

