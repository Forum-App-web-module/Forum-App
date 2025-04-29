from fastapi import APIRouter, Response
from services import category_service

category_router = APIRouter(prefix="/categories", tags=["Categories"])

#view all categories
@category_router.get('/')
def view_categories():
    categories = category_service.get_all()
    return categories

#view category by ID
@category_router.get('/{category_id}')
def view_category(category_id: int):
    categroy = category_service.get_category_by_id(category_id)
    if not categroy:
        return Response(content='{"message":"No category found for this id"}', status_code=404)
    
    return categroy

#View topics for a category
@category_router.get('/{category_id}/topics')
def view_category_topics(category_id: int):
    topics = category_service.get_topics_by_category(category_id)
    if not topics:
        return Response(content='{"message":"No topics found for this category"}', status_code=204)
    
    return topics