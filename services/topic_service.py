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

    topic_query = '''
        SELECT t.id, t.title, t.category_id, t.author_id, u.username, t.best_reply_id, t.locked
        FROM topics t
        JOIN users u ON t.author_id = u.id
        WHERE t.id = ?
    '''
    topic_rows = get_data_func(topic_query, (topic_id,))
    if not topic_rows:
        return None

    id, title, category_id, author_id, author_username, best_reply_id, locked = topic_rows[0]
    topic = Topic.from_query_result((id, title, category_id, author_id, best_reply_id, bool(locked)))
    topic_dict = topic.model_dump() #topic.dict
    topic_dict["author_username"] = author_username

    #category name, needed for the html
    category_query = "SELECT name FROM categories WHERE id = ?"
    category_rows = get_data_func(category_query, (category_id,))
    topic_dict["category_name"] = category_rows[0][0] if category_rows else "Неизвестна категория"

    #replies+username name, needed for the html
    replies_query = '''
        SELECT r.id, r.creator_id, u.username, r.topic_id, r.text, r.created_on
        FROM replies r
        JOIN users u ON r.creator_id = u.id
        WHERE r.topic_id = ?
        ORDER BY r.created_on ASC
    '''
    rows_replies = get_data_func(replies_query, (topic_id,))
    replies = []
    for row in rows_replies:
        id, creator_id, username, topic_id_fk, text, created_at = row
        reply = Replies(
            id=id,
            creator_id=creator_id,
            topic_id=topic_id_fk,
            text=text,
            created_at=created_at
        )
        reply_dict = reply.model_dump()
        reply_dict["username"] = username
        replies.append(reply_dict)

    return {
        "topic": topic_dict,
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
