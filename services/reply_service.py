from data.database import insert_query
from data.models import Replies

def create_reply(reply: Replies):
    #creator_id, topic_id, reply_text, *rest = reply.creator_id, reply.topic_id, reply.text

    if reply.text and reply.topic_id:
        query = """
            insert into replies
            (creator_id,
            topic_id,
            text,
            created_on)
            values (?, ?, ?, NOW())
            """

        insert_query(query, (reply.creator_id, reply.topic_id, reply.text))
    else:
        raise ValueError("Reply text and topic id are required")

    return True
