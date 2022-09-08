"""Youtube Video Router"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.models.youtube.video import Video
from src.models.youtube.comments import Comments

router = APIRouter(prefix="/youtube/video", tags=["Youtube"])


class VideoDetailsRequest(BaseModel):
    """Video Id Request Schema"""

    video_id: str


@router.get("/details", response_model=Video)
def get_video_details(
    video_id: str, subtitles: Optional[bool] = Query(False, description="Get Subtitles")
):
    """Return Video Details"""
    try:
        return Video(video_id=video_id).details(subtiles=subtitles)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/comments", response_model=Comments)
def get_comments(video_id: str):
    """Return Video Comments"""
    try:
        return Comments(video_id=video_id).get_comments(continuation_token=None)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/comments/continuation", response_model=Comments)
def get_comments_continuation(video_id: str, continuation_token: str):
    """Return Video Comments"""
    try:
        return Comments(video_id=video_id).get_comments(
            continuation_token=continuation_token
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
