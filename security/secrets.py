from data.database import query_count
from hashlib import sha256
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path="key_example.env")

SALT = getenv("SALT")

def hash_password(password: str):
    solted = password + SALT
    return sha256(solted.encode("utf-8")).hexdigest()

# check if deleted
def validate_password(username: str, password: str):
    hashed = hash_password(password) 
    result = query_count('SELECT username FROM users WHERE username = ? AND password = ?',
                         (username, hashed))

    return result == 1




