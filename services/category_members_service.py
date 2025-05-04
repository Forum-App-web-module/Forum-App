from data.database import query_count, insert_query
from data import database


def is_member(category_id: int, user_id: int) -> bool:
    query = "SELECT * FROM category_members WHERE category_id = ? AND user_id = ?"

    data = query_count(query, (category_id, user_id))

    return True if data == 1 else False

def can_write(category_id, user_id):
    query = "SELECT * FROM category_members WHERE category_id = ? AND user_id = ? AND write_access = 1"

    data = query_count(query, (category_id, user_id))

    return True if data == 1 else False

def give_access(category_id, user_id):
    query = "INSERT INTO category_members (category_id, user_id, write_access) VALUES (?, ?, 1)"

    data = insert_query(query, (category_id, user_id))

    return True if data else False


def revoke_access(category_id, user_id, update_func = None):

    if update_func is None:
        update_func = database.update_query

    query = 'DELETE from category_members WHERE category_id = ? AND user_id=?'

    data = update_func(query, (category_id, user_id))

    return True if data else False
    

def update_write_access(category_id, user_id, access: bool, update_func = None):
    
    if update_func is None:
            update_func = database.update_query
    
    if access == True: 
        updated_access = 0
    else: updated_access = 1

    query = 'UPDATE category_members SET write_access = ? WHERE category_id = ? AND user_id=?'

    data = update_func(query, (updated_access, category_id, user_id))

    return True if data else False


def view_privileged_users(category_id, get_data_func = None):
     
    if get_data_func is None:
            get_data_func = database.read_query

    query = 'SELECT users.username FROM users JOIN category_members as cat ON users.id = cat.user_id WHERE cat.category_id = ?'
    
    data = get_data_func(query, (category_id,))

    return data
