from pydantic import BaseModel

class Messages(BaseModel):
    pass

class Users(BaseModel):
    pass

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

class Replies(BaseModel):
    pass

class Topic(BaseModel):
    id: int
    title: str
    category_id: int
    author_id: int
    best_reply_id: int
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


