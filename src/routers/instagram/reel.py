from typing import List
from fastapi import APIRouter, HTTPException, Query
from src.models.instagram.user import UserRestrictedInfos
from src.models.instagram.reel import Reel
from pydantic import BaseModel

router = APIRouter(prefix="/instagram/reel", tags=["Instagram"])


class OneReelsResponse(BaseModel):
    user: UserRestrictedInfos
    reel: Reel


@router.get("/details", response_model=OneReelsResponse)
def get_reel_details(pk: str = Query(description="Put the Pk of the reel")):
    try:
        user, reel = Reel(reel_pk=pk).get_reel_details()
        return OneReelsResponse(user=user, reels=reel)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
