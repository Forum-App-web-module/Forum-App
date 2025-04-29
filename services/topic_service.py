from data.database import read_query, insert_query
from data.models import Topic, Replies

def create_topic(title: str, category_id: int, author_id: int):
    sql = """INSERT INTO topics (title, category_id, author_id, lock) VALUES (?, ?, ?, 0)""" # value = 0 false
    params = (title, category_id, author_id)

    return insert_query(sql, params)

def get_all_topics(search: str = "", sort_by: str = "title", skip: int = 0, limit: int = 5):
    if sort_by not in ["title", "author_id"]:
        sort_by = "title"

    sql = f'''
    SELECT id, title, category_id, author_id, best_reply_id, lock FROM topics
    WHERE title LIKE ?
    ORDER BY {sort_by}
    LIMIT ? OFFSET ?
    '''

    params = (f"%{search}%", limit, skip)
    rows = read_query(sql, params)
    topics = []
    for row in rows:
        id, title, category_id, author_id, best_reply_id, lock = row
        topics.append(Topic.from_query_result((id, title, category_id, author_id, best_reply_id, bool(lock))))

    return topics

def get_topic_with_replies(topic_id: int):
    sql = '''SELECT id, title, category_id, author_id, best_reply_id, lock FROM topics WHERE id = ?'''
    rows = read_query(sql, (topic_id,))
    
    if not rows:
        return None # return message in router
    
    id, title, category_id, author_id, best_reply_id, lock = rows[0]
    topic = Topic.from_query_result((id, title, category_id, author_id, best_reply_id, bool(lock)))

    sql_with_replies = '''
    SELECT id, creator_id, topic_id, text, created_on
    FROM replies
    WHERE topic_id = ?
    ORDER BY created_on ASC
    '''
    rows_replies = read_query(sql_with_replies, (topic_id,))
    replies = [Replies(
        id = row[0],
        creator_id = row[1],
        topic_id = row[2],
        text = row[3],
        created_at = row[4]
    ) for row in rows_replies]

    return {
        "topic": topic,
        "replies": replies
            }