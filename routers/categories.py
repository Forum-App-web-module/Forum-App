from fastapi import APIRouter, Body, Header
from services import category_service, category_members_service
from common.responses import NotFound, NoContent, BadRequest, Unauthorized, Succesfull
from security.jwt_auth import verify_access_token
from security.authorization import admin_auth

category_router = APIRouter(prefix="/categories", tags=["Categories"])

#view all categories, no authentication required
@category_router.get('/')
def view_categories():
    categories = category_service.get_all()
    return categories

#view category by ID, if a category is private, only members can reach this EP
@category_router.get('/{category_id}')
def view_category(category_id: int, token: str = Header()):
    payload = verify_access_token(token)

    user_id = payload["id"]

    category = category_service.get_category_by_id(category_id)
    if not category:
        return NotFound(content="No category found with this ID")
    
    if category.is_private:
        if not category_members_service.is_member(category_id, user_id):
            return Unauthorized(content="This category is private, you are not a member.")
        
    return category
    

#View topics for a category
@category_router.get('/{category_id}/topics')
def view_category_topics(category_id: int):
    topics = category_service.get_topics_by_category(category_id)
    if not topics:
        return NoContent(content="No topics found for this category")
    
    return topics


# Create a new category, authentication and admin rights required
@category_router.post('/')
def create_category(name: str = Body(..., min_length=1, max_length=45), token: str = Header()):
    payload = verify_access_token(token)
    if not payload or not admin_auth(payload):
        return Unauthorized(content="Admin access required for this action.")
    
    new_id = category_service.create_category(name)
    return Succesfull(content="Category created.")


# Update category privacy, admin rights required
@category_router.put('/{category_id}/privacy')
def update_category_privacy(category_id: int, is_private: bool, token: str = Header()):
    payload = verify_access_token(token)
    if not payload or not admin_auth(payload):
        return Unauthorized(content="Admin access required for this action.")
    
    if not category_service.get_category_by_id(category_id):
        return NotFound(content="No category found with this ID")
    
    new_status = category_service.update_privacy(category_id, is_private)
    return Succesfull(content=f"Category status changed to {new_status}")


@category_router.put('/{category_id}/lock')
def update_category_lock(category_id: int, lock: bool, token: str = Header()):
    payload = verify_access_token(token)
    if not payload or not admin_auth(payload):
        return Unauthorized(content="Admin access required for this action.")
    
    if not category_service.get_category_by_id(category_id):
        return NotFound(content="No category found with this ID")
    
    new_status = category_service.lock_category(category_id, lock)
    return Succesfull(content=f"Category lock status changed to {new_status}")

# TODO:
# should remove below repetition using Depends()
#
# payload = verify_access_token(token)
#    if not payload or not admin_auth(payload):
#        return Unauthorized(content="Admin access required for this action.")