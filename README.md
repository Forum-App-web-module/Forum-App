# Forum-App
Telerik Alpha Python - 1st team project in Web module


Users Endpoints:
- GET "/" + query sort, filter - Search user profiles
- POST "/"  - User Creation
- GET "/{id}" - Search for user / Open account
- PUT "/{id}" - Update account. If authorised as owner - changes without id, is_admin. Can deactivate account. If authorised as Admin - allowed to: is_admin, is_active.
- 
- PUT/block/{id} - block user - ADMIN ONLY
- PUT/promote/{id} - ADMIN ONLY

Messages Endpoints: 
- GET "/"  - Get all conversations(list)
- POST "/" - Create new conversation, sender(from auth)
- GET "/{id}" - Get conversation information + Messages between the users
- POST /new_message/id



