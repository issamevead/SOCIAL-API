from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.models.tiktok.video import Video

router = APIRouter(prefix="/tiktok/video", tags=["Tiktok"])


class VideoDetailsRequest(BaseModel):
    """Schema Class for a Tiktok Video Details"""

    video_id: str


class VideoDetailsResponse(BaseModel):
    """Schema Class for a Tiktok Video Details"""

    video_id: str = None
    details: Any = None


@router.post("/id", response_model=VideoDetailsResponse)
def post_video_details(data: VideoDetailsRequest):
    """Return User Id"""
    try:
        return Video.get_video_details(data.video_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/id", response_model=VideoDetailsResponse)
def get_video_details_alt(video_id: str):
    """Return User Id"""
    try:
        return Video.get_video_details(video_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
