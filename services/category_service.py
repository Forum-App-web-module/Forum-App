from data.database import read_query
from data.models import Category, Topic
from fastapi import Response

def get_all():
    sql = '''SELECT id, name, is_private, locked from categories'''
    rows = read_query(sql)

    return [Category.from_query_result(row) for row in rows]  

def get_category_by_id(category_id: int):
    sql = '''SELECT id, name, is_private, locked FROM categories WHERE id = ?'''
    rows = read_query(sql, (category_id,))
    if not rows:
        return None # return message in router
    
    id, name, is_private, locked = rows[0]
    return Category.from_query_result((id, name, bool(is_private), bool(locked)))

def get_topics_by_category(category_id: int, search: str = "", sort_by: str = "title", skip: int = 0, limit: int = 5):
    if sort_by not in ["title", "author_id"]:
        sort_by = "title"

    sql = f'''
        SELECT id, title, category_id, author_id, best_reply_id, locked
        FROM topics
        WHERE category_id = ?
            AND title LIKE ?
        ORDER BY {sort_by}
        LIMIT ? OFFSET ?
    '''

    params = (category_id, f"%{search}%", limit, skip)
    rows = read_query(sql, params)   
    return [Topic.from_query_result(row) for row in rows]


def locked_category(category_id: int, locked: bool):
    pass


def create_caterogory():
    pass

def make_private(category_id):
    pass
def make_non_private(category_id):
    pass

def give_access(category_id, user_id):
    pass

def revoke_access(category_id, user_id): 
    pass

def give_write_access(category_id, user_id):
    pass

def revoke_write_access(categiry_id, user_id):
    pass

def view_privileged_users(category_id):
    pass

def lock_topic(topic_id):
    pass

def unlock_topic(topic_id):
    pass

def lock_category(category_id):
    pass

def unlock_category(category_id):
    pass

def is_member(category_id, user_id):
    pass

def can_write(category_id, user_id):
    pass


    

