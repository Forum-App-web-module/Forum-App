from fastapi import APIRouter, Header, Body
from fastapi.responses import JSONResponse
from security.jwt_auth import verify_access_token
from services.user_service import find_user_by_username
from services.message_service import create, list_messages, list_conversations

message_router = APIRouter(prefix='/messages', tags=['Messages'])

@message_router.get('/')
# Returning all conversations of the authenticated user.
def get_conversations(token: str = Header()):
    
    # token authentication
    payload = verify_access_token(token)
    if not payload:
        return JSONResponse(status_code=401, content={"message": "Authentication failed."})

    conversations = list_conversations(payload["id"])

    if not conversations:
        return JSONResponse(status_code=200, content={"message": f'You dont have any started conversations'})

    return JSONResponse(status_code=200, content={"message": conversations})


@message_router.get('/{username}')
# Returning specific conversation(list of messages) between the authenticated user and user with username as per path parameter.
def get_specific_conversation(username: str, token: str = Header()):

     # token authentication
    payload = verify_access_token(token)
    if not payload:
        return JSONResponse(status_code=401, content={"message": "Authentication failed."})
    
    user_information = find_user_by_username(username)
    if not user_information:
        return JSONResponse(status_code=400, content={"message": f'There is no account with username: {username}'})
    
    messages = list_messages(payload["id"], user_information.id)    

    if not messages:
        return JSONResponse(status_code=204, content={"message": f'There are no messages between you and username: {username}'})

    return messages


@message_router.post('/{username}')
# Creating new message between the authenticated user and user in path parameter.
def create_message(username: str, text: str = Body(..., min_length=1, max_length=200), token: str = Header()):
    
     # token authentication
    payload = verify_access_token(token)
    if not payload:
        return JSONResponse(status_code=401, content={"message": "Authentication failed."})
    
    user_information = find_user_by_username(username)
    if not user_information:
        return JSONResponse(status_code=400, content={"message": f'There is no account with username: {username}'})
    
    result = create(payload["id"], user_information.id, text)

    if result:
        JSONResponse (status_code=201, content={"message":"Message is created"})
    JSONResponse (status_code=201, content={"message":"Message failed"})


