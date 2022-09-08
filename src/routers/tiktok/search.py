"""Search Router"""
from typing import Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.tiktok.search import Search

router = APIRouter(prefix="/tiktok/search", tags=["Tiktok"])


class SearchQuery(BaseModel):
    """Search Query Schema"""

    query: str


class SearchGeneralResponse(BaseModel):
    """Schema Class for a Tiktok Search Result Video"""

    query: str = None
    videos: List[Any] = None


class SearchUsersResponse(BaseModel):
    """Schema Class for a Tiktok Search Result Video"""

    query: str = None
    users: List[Any] = None


@router.post("/general/query", response_model=SearchGeneralResponse)
def post_search_general(data: SearchQuery):
    """Return Search Result"""
    try:
        return Search.search_general(data.query)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/general/query", response_model=SearchGeneralResponse)
def get_search_general(query: str):
    """Return Search Result"""
    try:
        return Search.search_general(query)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/accounts/query", response_model=SearchUsersResponse)
def post_search_accounts(data: SearchQuery):
    """Return Search Result"""
    try:
        return Search.search_accounts(data.query)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/accounts/query", response_model=SearchUsersResponse)
def get_search_accounts(query: str):
    """Return Search Result"""
    try:
        return Search.search_accounts(query)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/videos/query", response_model=SearchGeneralResponse)
def post_search_videos(data: SearchQuery):
    """Return Search Result"""
    try:
        return Search.search_videos(data.query)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/general/query", response_model=SearchGeneralResponse)
def get_search_videos(query: str):
    """Return Search Result"""
    try:
        return Search.search_videos(query)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
