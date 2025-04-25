from data.database import read_query
from data.models import Topic

def get_all_topics():
    sql = '''SELECT id, title, category_id, author_id, best_reply_id, lock FROM topics'''
    rows = read_query(sql)
    return [Topic.from_query_result(row) for row in rows]

def get_topic_by_id(topic_id: int):
    sql = '''SELECT id, title, category_id, author_id, best_reply_id, lock FROM topics WHERE id = ?'''
    rows = read_query(sql, (topic_id,))
    return Topic.from_query_result(rows[0] if rows else None)