from fastapi import APIRouter

message_router = APIRouter(prefix='/messages', tags=['Messages'])

@message_router.get('/')
# Returning all conversation of the authenticated user.
def get_conversations():
    pass

@message_router.get('/{id}')
# Returning specific conversation(list of messages) between the authenticated user and user with id as per path parameter.
def get_specific_conversation(id: int):
    pass

@message_router.post('/{id}')
# Creating new message between the authenticated user and user in path parameter.
def create_message(id: int):
    pass