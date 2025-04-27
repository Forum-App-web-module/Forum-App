from data.database import query_count
from hashlib import sha256


def hash_password(password: str, salt):
    solted = password + salt
    return sha256(solted.encode("utf-8")).hexdigest()

def validate_password(username: str, password: str):
    hashed = hash_password(password, username[2:4]) # salt should be stored in the DB upon user registration and retrieved during login attempt

    result = query_count('SELECT username FROM users WHERE username = ? AND password = ?', (username, hashed))[0]

    return result == 1




