from pydantic import BaseModel, constr
from datetime import datetime


class Messages(BaseModel):
    id: int | None
    text: str
    sent_on: datetime | None = datetime.now
    sender_id: int
    receiver_id: int

    @classmethod 
    def from_query_result(cls, id, text, sent_on, sender_id, receiver_id):
        return cls(id = id,
                   text = text,
                   sent_on = sent_on,
                   sender_id = sender_id,
                   receiver_id = receiver_id)

class MessageOut(BaseModel):
    id: int | None
    text: str
    sent_on: datetime | None
    sender_username: str
    receiver_username: str

    @classmethod 
    def from_query_result(cls, id, text, sent_on, sender_username, receiver_username):
        return cls(id = id,
                   text = text,
                   sent_on = sent_on,
                   sender_username = sender_username,
                   receiver_username = receiver_username)

class Users(BaseModel):
    id: int | None
    username: constr(min_length=6, max_length=30)
    email: str
    password: constr(min_length=6, max_length=30)
    bio: str | None
    is_admin: bool | None = False
    is_active: bool | None = True

    @classmethod
    def from_query_result(cls, id, username, email, password, bio, is_admin, is_active):
        return cls(username = username,
                   email = email,
                   bio = bio,
                   is_admin = is_admin)

class LoginData(BaseModel):
    username: constr(min_length=6, max_length=30)
    password: constr(min_length=6, max_length=30)

class RegisterData(BaseModel):
    username: constr(min_length=6, max_length=30)
    email: constr(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: constr(min_length=6, max_length=30)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: str | None
    is_admin: bool
    is_active: bool



class UserResponseList(BaseModel):
    username: str
    is_admin: bool


class Category(BaseModel):
    id: int 
    name: str
    is_private: bool
    lock: bool

    @classmethod
    def from_query_result(cls, row):
        return cls(
            id = row[0],
            name = row[1],
            is_private = bool(row[2]),
            lock = bool(row[3])
        )

# Possibly useless
class Replies(BaseModel):
    id: int | None
    creator_id: int
    topic_id: int
    text: str
    created_at: datetime | None = None

class Topic(BaseModel):
    id: int
    title: str
    category_id: int
    author_id: int
    best_reply_id: int | None = None
    lock: bool

    @classmethod
    def from_query_result(cls, row):
        return cls(
            id = row[0],
            title = row[1],
            category_id = row[2],
            author_id = row[3],
            best_reply_id = row[4],
            lock = bool(row[5])
        )


