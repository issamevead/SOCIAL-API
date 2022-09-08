"""Youtube Video Router"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.models.youtube.channel import Channel, ChannelVideos

router = APIRouter(prefix="/youtube/channel", tags=["Youtube"])


@router.get("/details", response_model=Channel)
def get_channel_details(channel_id: str):
    """Return Channel Details"""
    try:
        return Channel(channel_id=channel_id).details()
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/videos", response_model=ChannelVideos)
def get_channel_videos(channel_id: str):
    """Return Channel Videos"""
    try:
        return Channel(channel_id=channel_id).videos()
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
