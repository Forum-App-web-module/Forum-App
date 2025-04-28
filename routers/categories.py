from fastapi import APIRouter, Response
from services import category_service

category_router = APIRouter(prefix="/categories", tags=["Categories"])

@category_router.get('/')
def view_categories():
    return category_service.get_all

@category_router.get('/{category_id}')
def view_category(category_id: int):
    categroy = category_service.get_category_by_id(category_id)
    if not categroy:
        return Response(content='{"message":"No tcategory found for this id"}', status_code=404)
    
    return categroy

@category_router.get('/{category_id}/topics')
def view_category_topics(category_id: int):
    topics = category_service.get_topics_by_category(category_id)
    if not topics:
        return Response(content='{"message":"No topics found for this category"}', status_code=204)
    
    return topics