from email.header import Header

from fastapi import APIRouter, Body

from security.jwt_auth import verify_access_token
from security.authorization import admin_auth
from services import category_service
from common.responses import NotFound, NoContent, Created, BadRequest

category_router = APIRouter(prefix="/categories", tags=["Categories"])

#view all categories
@category_router.get('/')
def view_categories():
    categories = category_service.get_all()
    return categories

#view category by ID
@category_router.get('/{category_id}')
def view_category(category_id: int):
    category = category_service.get_category_by_id(category_id)
    if not category:
        return NotFound(content="No category found with this ID")
    
    return category

#View topics for a category
@category_router.get('/{category_id}/topics')
def view_category_topics(category_id: int):
    topics = category_service.get_topics_by_category(category_id)
    if not topics:
        return NoContent(content="No topics found for this category")
    
    return topics

# Create category
@category_router.post('/', status_code=201)
def create_category(token: str = Header(), name: str = Body(..., min_length=3, max_length=20)):
    # Admin authorization returns an error or None
    if admin_auth(token) is None:
        # call service
        category_service.create_category(name)
        return Created(content=f'Category {name} created')


# Update category privacy
@category_router.put('/privicy/{category_id}', status_code=201)
def update_privacy(category_id: int, is_private: int = Body(...,regex='^(0|1))$'), token: str = Header()):
    # Admin authorization returns an error or None
    if admin_auth(token) is None:
        # call service
        category_service.update_privacy(category_id, is_private)
        return Created(content=f'Category {category_id} privacy updated')

