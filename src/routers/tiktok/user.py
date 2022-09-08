"""User Router"""
from typing import Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.tiktok.user import User
from src.models.tiktok.video import VideoModel

router = APIRouter(prefix="/tiktok/user", tags=["Tiktok"])


class UserId(BaseModel):
    """User Id Request Schema"""

    username: str


class UserIdResponse(BaseModel):
    """User Id Response Schema"""

    username: str
    user_id: str


class UserDetailsResponse(BaseModel):
    """Schema Class for a Tiktok User Details"""

    username: str = None
    user_id: str = None
    profile_image: str = None
    following: int = None
    followers: int = None
    total_videos: int = None
    total_heart: int = None
    verified: bool = None


class UserVideosResponse(BaseModel):
    """Schema Class for a Tiktok User's Videos"""

    username: str = None
    videos: List[Any] = None


@router.post("/id", response_model=UserIdResponse)
def post_user_id(data: UserId):
    """Return User Id"""
    try:
        return User.get_user_id(data.username)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/id", response_model=UserIdResponse)
def get_user_id(username: str):
    """Return User Id"""
    try:
        return User.get_user_id(username)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/details", response_model=UserDetailsResponse)
def post_user_details(data: UserId):
    """Return User Details"""
    try:
        return User.get_user_details(data.username)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/details", response_model=UserDetailsResponse)
def get_user_details(username: str):
    """Return User Details"""
    try:
        return User.get_user_details(username)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/videos", response_model=UserVideosResponse)
def get_user_videos(username: str):
    """Return User Videos"""
    try:
        return User.get_videos(username)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/videos", response_model=UserVideosResponse)
def post_user_videos(data: UserId):
    """Return User Videos"""
    try:
        return User.get_videos(data.username)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
