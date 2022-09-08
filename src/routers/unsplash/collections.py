from fastapi import APIRouter, HTTPException, Query
from src.models.unsplash.collections import Collections
from src.models.unsplash.photos import BaseRequest

router = APIRouter(prefix="/unsplash/collections", tags=["Unsplash"])


@router.get("", response_model=Collections)
def get_collections_related_to_keyword(
    keyword: str,
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, default=20),
):
    """Return Tweet Details"""
    try:
        request = BaseRequest(keyword=keyword, page=page, per_page=per_page)
        return Collections().get_collections_related_to_keyword(request)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
