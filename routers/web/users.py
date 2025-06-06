from fastapi import APIRouter, Body, Header, Request, Form
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
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templatges
from pydantic import ValidationError
from common.auth import get_user_if_token

user_router = APIRouter(prefix='/users', tags=['Users'])
templates = CustomJinja2Templatges(directory="templates")


# @user_router.get('/')
# # Searches user profile by filters: Username and role.
# #  2 options: 1 search by username and role. 2 Search all admins.
# def search_user(request: Request, username: Optional[str] = Form(...), is_admin: Optional[str] = Form(...)):
#     # token authentication
#     verify_access_token(request.cookies.get('token'))
    
#     if not username and is_admin.lower() == "false":
#         return templates.TemplateResponse(request=request, name="users_search_results.html", context={"msg": "Please select at least one search parameters."})
        
#     users_list = get_users(username, is_admin)

#     return templates.TemplateResponse(request=request, name="users_search_results.html", context={'users': users_list})

@user_router.get('/register')
def serve_register(request:Request):
    return templates.TemplateResponse(request=request, name="auth/register.html")


@user_router.post('/register', status_code=201)
# Creates user profile
def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try: data = RegisterData(username=username, email=email, password=password)
    except ValidationError as val:
        return templates.TemplateResponse(request=request, name="auth/register.html", context={"msg":f"Invalid input"})

    try: new_id = create(username, email, hash_password(password))
    except IntegrityError as integ:
        return templates.TemplateResponse(request=request, name="auth/register.html", context={"msg":f"Invalid input - {integ}"})
    
    if new_id:
        user = try_login(username, hash_password(password))
        token = create_access_token(user)
        response = RedirectResponse(url="/home", status_code=302)
        response.set_cookie('token', token)
        return response
 


@user_router.get('/login')
def serve_login(request:Request):
    return templates.TemplateResponse(request=request, name="auth/login.html")

@user_router.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    user = try_login(username, hash_password(password))

    if user: 
        token = create_access_token(user)
        response = RedirectResponse(url="/home", status_code=302)
        response.set_cookie('token', token)
        return response
    else: 
        return templates.TemplateResponse(request=request, name="auth/login.html", context={"msg": "Wrong Credentials"})


@user_router.get('/profile')
# Returns User profile information
def get_profile(request: Request):

    # token authentication
    payload = get_user_if_token(request)
    username = payload["key"]['username']
    user_information = find_user_by_username(username)
    if not user_information:
        return templates.TemplateResponse(request=request, name="index.html", context={"msg":f'There is no account with username: {username}'})
    else: 
        return templates.TemplateResponse(request=request, name = "prefixed/profile.html", context={"user": user_information})

@user_router.post('/deactivate')
# Deactivation(block) of account BY ADMIN
def deactivate_user(request: Request, username: str = Form(...)):

    # token authentication
    payload = get_user_if_token(request)

    #  ADMIN authorization
    admin_auth(payload)

    if not exists(username):
        return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, 
                                          context={"msg": f'There is no account with username: {username}', 'section': 'user'}) 
    result = deactivate(username)
    if result:
        return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, 
                                          context={"msg": f'{username} is now blocked.', 'section': 'user'}) 

    else: return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, 
                                          context={"msg": f'{username} already has been blocked.', 'section': 'user'}) 


                                        
@user_router.post('/activate')
# activation of account BY ADMIN
def activate_user(request: Request, username: str = Form(...)):

    # token authentication
    payload = get_user_if_token(request)

    #  ADMIN authorization
    admin_auth(payload)

    if not exists(username):
        return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, 
                                          context={"msg": f'There is no account with username: {username}', 'section': 'user'}) 
    result = activate(username)
    if result:
        return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, 
                                          context={"msg": f'{username} is now unblocked.', 'section': 'user'}) 

    else: return templates.TemplateResponse(name = "admin_privacy/admin.html", request=request, 
                                          context={"msg": f'{username} already has been unblocked.', 'section': 'user'}) 


@user_router.post('/bio')
# Update user bio BY the user.
def update_profile_bio(request: Request, bio: str = Form(...) ):

    # token authentication
    payload = get_user_if_token(request)
    
    result = update_bio(payload["key"]["username"], bio)

    if result:
        response = RedirectResponse(url="/users/profile", status_code=302)
        return response

