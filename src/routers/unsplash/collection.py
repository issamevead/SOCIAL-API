from typing import List, Optional
from src.models.unsplash.collection import CollectionRequest, Collection
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/unsplash/collection", tags=["Unsplash"])


@router.get("/details", response_model=Collection)
def get_collection_details(collection_id: str):
    """Return Tweet Details"""
    try:
        return Collection(collection_id=collection_id).get_collection_details()
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/photos", response_model=List)
def get_collection_photos(
    collection_id: str,
    page: int = 1,
    per_page: int = 10,
    share_key: Optional[str] = None,
):
    try:
        request = CollectionRequest(page=page, per_page=per_page, share_key=share_key)
        return Collection(collection_id=collection_id).get_collection_photos(request)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
