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

@user_router.post('/register', status_code=201)
# Creates user profile
def register(data: RegisterData):
    try: new_id = create(data.username, data.email, hash_password(data.password))
    except IntegrityError as integ:
        return BadRequest(content = "Invalid input - {integ}")
    if new_id:
        return Created(content = f"Account with username {data.username} created successfully")
    else: return InternalServerError (content = "Server error - contact addministrator")


@user_router.post('/login')
def login(login: LoginData):

    user = try_login(login.username, hash_password(login.password))

    if user: 
        return create_access_token(user)
    else: return BadRequest(content = "Invalid login data")


@user_router.get('/{username}')
# Returns User profile information
def get_profile(username: str, token: str = Header()):

    # token authentication
    verify_access_token(token)
    
    user_information = find_user_by_username(username)
    if not user_information:
        return BadRequest(content = f'There is no account with username: {username}')
    else: 
        return user_information


@user_router.put('/bio')
# Update user bio BY the user.
def update_profile_bio(bio: str = Body(..., min_length=1, max_length=150), token: str = Header()):

    # token authentication
    payload = verify_access_token(token)
    
    result = update_bio(payload["username"], bio)

    # following is mariadb validation error. No need to proceed if Body validation error above.
    # except DataError as dat:
    #     return JSONResponse (status_code=400, content= {"message": f"Invalid input - {dat} , max lenght is 150 characters."})
    
    if result:
        return Successful(content= f"Bio is updated")
    

@user_router.put('/deactivate/{username}')
# Deactivation(block) of account BY ADMIN
def deactivate_user(username: str, token: str = Header()):

    # token authentication
    payload = verify_access_token(token)

    #  ADMIN authorization
    admin_auth(payload)

    if not exists(username):
        return BadRequest(content = f'There is no account with username: {username}')

    result = deactivate(username)
    if result:
        return Successful(content = f"{username} is now blocked.")

    else: return Successful(content = f'{username} already has been blocked.')

@user_router.put('/activate/{username}')
# Activation(Unblock) account BY ADMIN
def activate_user(username: str, token: str = Header()):

    # token authentication
    payload = verify_access_token(token)

    #  ADMIN authorization
    admin_auth(payload)

#  requires ADMIN authorization
    if not exists(username):
        return BadRequest(content = f'There is no account with username: {username}')

    result = activate(username)
    if result:
        return Successful(content = f"{username} is activated.")

    else: return Successful(content = f'{username} is already activated.')


@user_router.put('/promote/{username}')
# Promote user into admin.
def promote_user(username: str, token: str = Header()):
    
     # token authentication
    payload = verify_access_token(token)

    #  ADMIN authorization
    admin_auth(payload)

    if not exists(username):
        return BadRequest(content = f'There is no account with username: {username}')
    
    result = promote(username)
    if result:Successful(content = f"{username} is now Admin.")

    else: return Successful(content = f'{username} is already Admin.')


# Give User Category read access
@user_router.put('/read_access/{id}/category/{category_id}')
def give_user_category_access(id: int, category_id: int, token: str = Header()):
    # Admin authorization returns an error or None
    if admin_auth(token):
        # call service
        give_access(id, category_id)
        return Created(content=f'User {id} has access to category {category_id}')


# Give User a Category Write Access
@user_router.put('/write_access/{id}/category/{category_id}')
def give_user_category_write_access(id: int, category_id: int, token: str = Header()):
    # Admin authorization returns an error or None
    if admin_auth(token):
        # call service
        update_write_access(id, category_id, True)
        return Created(content=f'User {id} has write access to category {category_id}')


# Revoke User Access
@user_router.delete('/access/{id}/category/{category_id}')
def delete_user_category_access(id: int, category_id: int, token: str = Header()):
    # Admin authorization returns an error or None
    if admin_auth(token):
        # call service
        revoke_access(id, category_id)
        return Created(content=f'User {id} has no access to category {category_id}')


# View Privileged Users
@user_router.get('/access/{category_id}')
def get_privileged_users(category_id: int, token: str = Header()):
    # Admin authorization returns an error or None
    if admin_auth(token):
        # call service
        service_response = view_privileged_users(category_id)[0]
        return [PrivilegedUsersResponse.from_query_result(row) for row in service_response]


