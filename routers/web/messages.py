from fastapi import APIRouter, Body, Header, Request, Form, Path
from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templatges
from services.message_service import list_conversations, list_messages
from services.user_service import find_user_by_username


message_router = APIRouter(prefix='/messages')
templates = CustomJinja2Templatges(directory="templates")

@message_router.get('/')
# Returning all conversations of the authenticated user.
def get_conversations(request: Request):
    
    # token authentication
    payload = get_user_if_token(request)

    conversations = list_conversations(payload["key"]["id"])

    private_messages = []
    for conv in conversations:

        user_information = find_user_by_username(conv)

        messages = list_messages(payload["key"]["id"], user_information.id)    

        if messages:
            private_messages.append(messages[-1])

    return templates.TemplateResponse(request=request, name="prefixed/messages.html",context={"messages": private_messages})


# @message_router.post('/{username}')
# # Creating new message between the authenticated user and user in path parameter.
# def create_message(username: str, text: str = Body(..., min_length=1, max_length=200), token: str = Header()):
    
#      # token authentication
#     payload = verify_access_token(token)
    
#     user_information = find_user_by_username(username)
#     if not user_information:
#         return BadRequest(content = f'There is no account with username: {username}')
    
#     result = create(payload["key"]["id"], user_information.id, text)

#     if result:
#         return Created(content = "Message is created")