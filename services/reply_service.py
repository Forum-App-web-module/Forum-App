from data.database import insert_query
from data.models import Replies

def create_reply(reply: str, topic_id: int, user_id: int):

    if reply and topic_id:
        query = """
            insert into replies
            (creator_id,
            topic_id,
            text,
            created_on)
            values (?, ?, ?, NOW())
            """

        insert_query(query, (user_id, topic_id, reply))
    else:
        raise ValueError("Reply text and topic id are required")

    return True
