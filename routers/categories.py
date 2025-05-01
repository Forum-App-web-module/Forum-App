from fastapi import APIRouter
from fastapi.responses import JSONResponse
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
        return JSONResponse(status_code=404, content={"message":"No category found with this ID"})
    
    return categroy

#View topics for a category
@category_router.get('/{category_id}/topics')
def view_category_topics(category_id: int):
    topics = category_service.get_topics_by_category(category_id)
    if not topics:
        return JSONResponse(status_code=204, content={"message":"No topics found for this category"})
    
    return topics