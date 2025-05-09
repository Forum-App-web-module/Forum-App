from fastapi import APIRouter, Body, Header
from typing import Optional
from fastapi.responses import JSONResponse
from data.models import Users, PrivilegedUsersResponse, RegisterData, LoginData
from services.user_service import (create, find_user_by_username, get_users, promote, deactivate, activate, update_bio,
                                   exists, try_login)
from services.category_members_service import give_access, update_write_access, revoke_access, view_privileged_users
from security.secrets import hash_password
from security.jwt_auth import verify_access_token, create_access_token
from security.authorization import admin_auth
from mariadb import IntegrityError
from common.responses import BadRequest, Created, Forbidden, Unauthorized, Successful, InternalServerError

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get('/')
# Searches user profile by filters: Username and role.
#  2 options: 1 search by username and role. 2 Search all admins.
def search_user(username: Optional[str]="", is_admin: Optional[str] = "False", token: str = Header()):
    # token authentication
    verify_access_token(token)
    
    if not username and is_admin.lower() == "false":
        return BadRequest(content = "Please select at least one search parameters.")

    users_list = get_users(username, is_admin)

    return users_list