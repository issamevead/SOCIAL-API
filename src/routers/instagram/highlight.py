from fastapi import APIRouter, HTTPException, Query
from src.models.instagram.highlight import Highlight

router = APIRouter(prefix="/instagram/highlights", tags=["Instagram"])


@router.get("", response_model=Highlight)
def get_reel_details(username: str, user_id: int = Query(description="Put the user id")):
    try:
        return Highlight(username=username, user_id=user_id).get_user_highlights()
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
