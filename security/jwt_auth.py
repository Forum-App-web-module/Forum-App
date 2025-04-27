from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "A69"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    # to_encode.update({"exp": expire})
    # return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"JWT": token}

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None





