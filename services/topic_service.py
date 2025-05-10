from data.database import read_query, insert_query, update_query
from data.models import Topic, Replies

def create_topic(title: str, category_id: int, author_id: int, insert_func=None):
    if insert_func is None:
        insert_func = insert_query

    query = """INSERT INTO topics (title, category_id, author_id, locked) VALUES (?, ?, ?, 0)""" # value = 0 false
    params = (title, category_id, author_id)
    new_topic = insert_func(query, params)

    return new_topic

def get_all_topics(search: str = "", sort_by: str = "title", skip: int = 0, limit: int = 5, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    if sort_by not in ["title", "author_id"]:
        sort_by = "title"

    query = f'''
    SELECT id, title, category_id, author_id, best_reply_id, locked FROM topics
    WHERE title LIKE ?
    ORDER BY {sort_by}
    LIMIT ? OFFSET ?
    '''

    params = (f"%{search}%", limit, skip)
    rows = get_data_func(query, params)

    topics = []
    for row in rows:
        id, title, category_id, author_id, best_reply_id, locked = row
        topics.append(Topic.from_query_result((id, title, category_id, author_id, best_reply_id, bool(locked))))

    return topics

def get_topic_with_replies(topic_id: int, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''SELECT id, title, category_id, author_id, best_reply_id, locked FROM topics WHERE id = ?'''
    rows = get_data_func(query, (topic_id,))
    
    if not rows:
        return None 
    
    id, title, category_id, author_id, best_reply_id, locked = rows[0]
    topic = Topic.from_query_result((id, title, category_id, author_id, best_reply_id, bool(locked)))

    query_with_replies = '''
    SELECT id, creator_id, topic_id, text, created_on
    FROM replies
    WHERE topic_id = ?
    ORDER BY created_on ASC
    '''
    rows_replies = get_data_func(query_with_replies, (topic_id,))
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


# locks/unlocks a topic 
def update_topic(topic_id, locked: int, update_func=None):
    if update_func is None:
        update_func = update_query

    query = '''UPDATE topics SET locked = ? WHERE id = ?'''
    params = (locked, topic_id)
    updated_status = update_func(query, params)

    return updated_status

def is_locked(topic_id: int, get_data_func=None, topic_fetch_func = None):
    if topic_fetch_func is None:
        topic_fetch_func = get_topic_with_replies
    topic_data = topic_fetch_func(topic_id, get_data_func)

    if not topic_data:
        return True
    
    
    topic: Topic = topic_data["topic"]
    return topic.lock

def get_category_id(topic_id: int, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''SELECT category_id FROM topics WHERE id = ?'''

    topic_data = get_data_func(query, (topic_id,))

    if not topic_data:
        return None

    category_id = topic_data[0][0]
    return category_id
