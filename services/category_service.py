from data.database import read_query, insert_query, update_query
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

def get_category_by_topic(topic_id: int):
    sql = '''
        SELECT c.id, c.name, c.is_private, c.locked FROM topics t
            JOIN categories c
            ON t.category_id = c.id
        WHERE t.id = ?
        '''
    category = read_query(sql, (topic_id,))[0]
    return category if category else None


def create_category(name: str):
    sql = '''INSERT INTO categories (name, is_private, locked) VALUES (?, 0, 0)'''
    new_category = insert_query(sql, (name,))
    return new_category

def lock_category(category_id: int, lock: bool): #locks/unlocks category only
    sql = '''UPDATE categories SET locked = ? WHERE id = ?'''
    category_status = update_query(sql, (int(lock), category_id))
    return category_status

def is_locked(category_id: int):
    category = get_category_by_id(category_id)
    if not category:
        return True
    return category.lock
    

def is_private(category_id: int):  # should be is_private, the below is updating
    category = get_category_by_id(category_id)
    if not category:
        return None
    return category.is_private

def update_privacy(category_id, locked: bool):
    sql = '''UPDATE categories SET locked = ? WHERE id = ?'''
    params = (locked, category_id)
    return read_query(sql, params)




    

