from data.models import Users, UserResponse, UserResponseList

from data import database
from hashlib import sha256




def create(user_username, user_email, user_password, insert_data_func = None):

    if insert_data_func is None:
        insert_data_func = database.insert_query

    new_id = insert_data_func('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (user_username, user_email, user_password))
    return new_id

def find_user_by_username(username, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('SELECT id, username, email, bio, is_admin, is_active FROM users WHERE username = ?', (username,))
    if not data:
        return None
    
    id, username, email, bio, is_admin, is_active = data[0]

    return UserResponse(
        id=id,
        username = username,
        email=email,
        bio = bio,
        is_admin = bool(is_admin),
        is_active = bool(is_active)
    )

def get_users(search_username: str | None, search_is_admin: str | None, get_data_func = None):

    if search_username:
        username = search_username + "%"
    elif search_username == "":
        username = "%"

    if search_is_admin.lower() == "true":
        is_admin = 1
    else: is_admin = 0

    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('SELECT username, is_admin FROM users WHERE username LIKE ? and is_admin = ?', (username, is_admin))
    if not data:
        return None
    
    users = [UserResponseList(username=row[0], is_admin=bool(row[1])) for row in data]
    return users

def promote(username: str, update_func = None):

    if update_func is None:
        update_func = database.update_query

    result = update_func('UPDATE users SET is_admin = ? WHERE username = ?', (1, username))
    return result

def deactivate(username: str, update_func = None):

    if update_func is None:
        update_func = database.update_query

    result = update_func('UPDATE users SET is_active = ? WHERE username = ?', (0, username))
    return result

def activate(username: str, update_func = None):

    if update_func is None:
        update_func = database.update_query

    result = update_func('UPDATE users SET is_active = ? WHERE username = ?', (1, username))
    return result

def exists(username: str, get_data_func = None):

    if get_data_func is None:
        get_data_func = database.read_query

    result = get_data_func('SELECT username FROM users WHERE username = ?', (username,))
    return result

def update_bio(username: str, bio: str, update_func = None):

    if update_func is None:
        update_func = database.update_query

    result = update_func('UPDATE users SET bio = ? WHERE username = ?', (bio, username))
    return result

def try_login(username, hash_password, get_data_func = None):

    if get_data_func is None:
        get_data_func = database.read_query

    user_data = get_data_func('SELECT id, username, email, bio, is_admin, is_active from users WHERE username = ? and password = ?', (username, hash_password))[0]

    if user_data:
        return {
            "id" : user_data[0],
            "username" : user_data[1],
            "email" : user_data[2],
            "bio" : user_data[3],
            "is_admin" : user_data[4],
            "is_active" : user_data[5]
        }
    else: return False

    

