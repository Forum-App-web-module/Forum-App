from data.models import Users, UserResponse, UserResponseList
from data.database import insert_query, read_query, update_query




def create(user_username, user_email, user_password):
    new_id = insert_query('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (user_username, user_email, user_password))
    return new_id

def find_user_by_username(username):
    data = read_query('SELECT username, email, bio, is_admin, is_active FROM users WHERE username = ?', (username,))
    if not data:
        return None
    
    username, email, bio, is_admin, is_active = data[0]

    return UserResponse(
        username = username,
        email=email,
        bio = bio,
        is_admin = bool(is_admin),
        is_active = bool(is_active)
    )

def get_users(search_username: str | None, search_is_admin: str | None ):

    if search_username:
        username = search_username + "%"
    elif search_username == "":
        username = "%"

    if search_is_admin.lower() == "true":
        is_admin = 1
    else: is_admin = 0

    query = 'SELECT username, is_admin FROM users WHERE username LIKE ? and is_admin = ?'

    data = read_query(query, (username, is_admin))
    if not data:
        return None
    
    users = [UserResponseList(username=row[0], is_admin=bool(row[1])) for row in data]
    return users

def promote(username: str):
    result = update_query('UPDATE users SET is_admin = ? WHERE username = ?', (1, username))
    return result

def deactivate(username: str):
    result = update_query('UPDATE users SET is_active = ? WHERE username = ?', (0, username))
    return result

def activate(username: str):
    result = update_query('UPDATE users SET is_active = ? WHERE username = ?', (1, username))
    return result

def exists(username: str):
    result = read_query('SELECT username FROM users WHERE username = ?', (username,))
    return result

def update_bio(username: str, bio: str):
    result = update_query('UPDATE users SET bio = ? WHERE username = ?', (bio, username))
    return result