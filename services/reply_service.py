from data.database import insert_query, query_count, update_query
from data.models import Replies
# from category_service import is_private
# from topic_service import is_locked
# from category_members_service import is_member

def create_reply(reply: str, topic_id: int, user_id: int):

    # if not is_locked(topic_id):
    #     category_is_private = is_private(topic_id)
    #     if category_is_private and is_member(user_id, topic_id):
    #         insert_reply_to_db(reply, topic_id, user_id)
    #         return True
    #     elif not category_is_private:
    #         insert_reply_to_db(reply, topic_id, user_id)
    #         return True
    #
    # return False

    query = """
                    insert into replies
                    (creator_id,
                    topic_id,
                    text,
                    created_on)
                    values (?, ?, ?, NOW())
                    """
    insert_query(query, (user_id, topic_id, reply))


# def insert_reply_to_db(reply, topic_id, user_id):
#     query = """
#                 insert into replies
#                 (creator_id,
#                 topic_id,
#                 text,
#                 created_on)
#                 values (?, ?, ?, NOW())
#                 """
#     insert_query(query, (user_id, topic_id, reply))


def validate_topic_and_reply(topic_id: int, reply_id: int):
    # validate reply belongs to topic
    query = """
        select * from replies
        where id = ?
        and topic_id = ?
        """

    reply_exists = query_count(query, (reply_id, topic_id))

    if reply_exists == 0:
        raise ValueError("Wrong parameters. Reply does not exist or does not belong to the topic.")
        # return False




def vote_to_db(reply_id, user_id, vote):
    # record the vote in the DB
    vote_data = query_count(
        "select * from votes where user_id = ? and reply_id = ?", (user_id, reply_id))
    if vote_data > 0:
        update_query("update votes set vote = ? where user_id = ? and reply_id = ?",
                     (int(vote), user_id, reply_id))
    else:
        insert_query("insert into votes (user_id, reply_id, vote) values (?, ?, ?)",
                     (user_id, reply_id, int(vote)))


def mark_best_reply(topic_id: int, reply_id: int, user_id: int):
    is_author = validate_is_author(topic_id, user_id)

    if not is_author:
        return False
    else:
        update_query("update topics set best_reply_id = ? where id = ?", (reply_id, topic_id))
        return True


def validate_is_author(topic_id, user_id):
    # validate user is author of topic
    query = """
        select * from topics
        where id = ?
        and author_id = ?
    """
    is_author = query_count(query, (topic_id, user_id))
    return is_author





