from data.database import insert_query, query_count, update_query
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

def vote_on_r(topic_id: int, reply_id: int, user_id: int, vote: str):
    # validate user exists
    user_exists = query_count("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
    if user_exists == 0:
        raise ValueError("User does not exist.")

    # validate reply belongs to topic
    query = """
        select * from replies
        where id = ?
        and topic_id = ?
        """

    reply_exists = query_count(query, (reply_id, topic_id))

    if reply_exists == 0:
        raise ValueError("Wrong parameters. Reply does not exist or does not belong to the topic.")

    # record the vote in the DB
    vote_data = query_count(
        "select * from votes where users_id = ? and replies_id = ?", (user_id, reply_id))

    if vote_data > 0:
        update_query("update votes set vote = ? where users_id = ? and replies_id = ?", (int(vote), user_id, reply_id))
    else:
        insert_query("insert into votes (users_id, replies_id, vote) values (?, ?, ?)", (user_id, reply_id, int(vote)))

    return True







