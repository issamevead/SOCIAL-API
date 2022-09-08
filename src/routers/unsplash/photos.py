from fastapi import APIRouter, HTTPException

from src.models.unsplash.photos import Photos, BaseRequest

router = APIRouter(prefix="/unsplash/photos", tags=["Unsplash"])


@router.get("/details", response_model=list)
def get_photos(keyword: str, page: int = 1, per_page: int = 10):
    """Return Tweet Details"""
    try:
        request = BaseRequest(keyword=keyword, page=page, per_page=per_page)
        return Photos().get_photos(request)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
