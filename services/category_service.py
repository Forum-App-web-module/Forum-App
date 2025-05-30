from data.database import read_query, insert_query, update_query
from data.models import Category, Topic

def get_all(get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''SELECT id, name, is_private, locked FROM categories'''
    rows = get_data_func(query)

    return [Category.from_query_result(row) for row in rows]

def get_all_public(get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''
        SELECT id, name, is_private, locked 
        FROM categories 
        WHERE is_private = 0
        '''
    rows = get_data_func(query)

    return [Category.from_query_result(row) for row in rows]

def get_allowed(id: int, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''
    SELECT c.id, c.name, c.is_private, c.locked
    FROM category_members cm
    JOIN categories c
    ON cm.category_id = c.id
    WHERE user_id = 3
    UNION
    SELECT * FROM categories
    WHERE is_private = 0
    '''

    rows = get_data_func(query)

    return [Category.from_query_result(row) for row in rows]

def get_category_by_id(category_id: int, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''SELECT id, name, is_private, locked FROM categories WHERE id = ?'''
    rows = get_data_func(query, (category_id,))
    if not rows:
        return None # return message in router
    
    id, name, is_private, locked = rows[0]
    return Category.from_query_result((id, name, bool(is_private), bool(locked)))

def get_category_by_name(category_id: str, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''SELECT id, name, is_private, locked FROM categories WHERE name = ?'''
    rows = get_data_func(query, (category_id,))
    if not rows:
        return None # return message in router
    
    id, name, is_private, locked = rows[0]
    return Category.from_query_result((id, name, bool(is_private), bool(locked)))


def get_topics_by_category(category_id: int, search: str = "", sort_by: str = "title", skip: int = 0, limit: int = 5, get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query
    
    if sort_by not in ["title_asc", "title_desc"]:
        sort_by = "title_asc"

    order_by = "ORDER BY title ASC" if sort_by == "title_asc" else "ORDER BY title DESC"

    query = f'''
        SELECT id, title, category_id, author_id, best_reply_id, locked
        FROM topics
        WHERE category_id = ?
          AND title LIKE ?
        {order_by}
        LIMIT ? OFFSET ?
    '''

    params = (category_id, f"%{search}%", limit, skip)
    rows = get_data_func(query, params)   
    return [Topic.from_query_result(row) for row in rows]


def create_category(name: str, insert_func=None):
    if insert_func is None:
        insert_func = insert_query

    query = '''INSERT INTO categories (name, is_private, locked) VALUES (?, 0, 0)'''
    new_category = insert_func(query, (name,))
    return new_category

def lock_category(category_id: int, lock: int, update_func=None): #locks/unlocks category only
    if update_func is None:
        update_func = update_query

    query = '''UPDATE categories SET locked = ? WHERE id = ?'''
    category_status = update_func(query, (lock, category_id))
    return category_status

def update_privacy(category_id: int, is_private: int, update_func=None):
    if update_func is None:
        update_func = update_query

    query = '''UPDATE categories SET is_private = ? WHERE id = ?'''
    new_status = update_func(query, (is_private, category_id))
    return new_status

def is_locked(category_id: int, get_data_func=None):
    category = get_category_by_id(category_id, get_data_func)
    if not category:
        return True
    return category.lock
    

def is_private(category_id: int, get_data_func=None): 
    category = get_category_by_id(category_id, get_data_func)
    if not category:
        return True
    return category.is_private

def count_topics_by_category(category_id: int, search: str = "", get_data_func=None):
    if get_data_func is None:
        get_data_func = read_query

    query = '''
        SELECT COUNT(*) FROM topics
        WHERE category_id = ?
          AND title LIKE ?
    '''
    params = (category_id, f"%{search}%")
    result = get_data_func(query, params)
    return result[0][0] if result else 0