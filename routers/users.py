from fastapi import APIRouter
from data.models import Users

user_router = APIRouter(prefix='/users', tags=['Users'])

@user_router.get('/')
# Searches user profile by filters: Username and role.
def search_user(username: str, is_admin = bool):
    pass

@user_router.post('/register')
# Creates user profile
def register(data: Users):
    pass

@user_router.get('/{username}')
# Returns User profile information
def check_profile(username: str):
    pass

@user_router.put('/{id}')
# Update user profile BY authorized user.
def update_profile(id: int):
    pass

@user_router.put('/deactivate/{username}')
# Deactivation(block) of account BY ADMIN
def deactivate(username: str):
    pass

@user_router.put('/promote/{username}')
# Promote user into admin.
def promote(username: str):
    pass


