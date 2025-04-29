from data.database import read_query
from data.models import Category, Topic
from fastapi import Response

def get_all():
    sql = '''SELECT id, name, is_private, lock from categories'''
    rows = read_query(sql)

    return [Category.from_query_result(row) for row in rows]  

def get_category_by_id(category_id: int):
    sql = '''SELECT id, name, is_private, lock FROM categories WHERE id = ?'''
    rows = read_query(sql, (category_id,))
    if not rows:
        return None # return message in router
    
    id, name, is_private, lock = rows[0]
    return Category.from_query_result((id, name, bool(is_private), bool(lock)))

def get_topics_by_category(category_id: int, search: str = "", sort_by: str = "title", skip: int = 0, limit: int = 5):
    if sort_by not in ["title", "author_id"]:
        sort_by = "title"

    sql = f'''
        SELECT id, title, category_id, author_id, best_reply_id, lock
        FROM topics
        WHERE category_id = ?
            AND title LIKE ?
        ORDER BY {sort_by}
        LIMIT ? OFFSET ?
    '''

    params = (category_id, f"%{search}%", limit, skip)
    rows = read_query(sql, params)   
    return [Topic.from_query_result(row) for row in rows]

