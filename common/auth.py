from fastapi import HTTPException
from data.models import Users
# from services.user_service import is_authenticated, from_token
from fastapi import Request
from security.jwt_auth import verify_access_token


# def get_user_or_raise_401(token: str) -> Users:
#     if not is_authenticated(token):
#         raise HTTPException(status_code=401)

#     return from_token(token)

def get_user_if_token(request: Request):
    token = request.cookies.get('token')
    if token:
        token = eval(token).get('JWT')
        return verify_access_token(token)
