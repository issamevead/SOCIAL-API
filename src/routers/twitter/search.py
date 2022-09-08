"""Tweet Router"""
from typing import Dict, Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, validator

from src.models.twitter.search import Search, SearchSection
from src.utils.countries import Languages

router = APIRouter(prefix="/twitter/search", tags=["Twitter"])


class SearchRequest(BaseModel):
    """Tweet Id Request Schema"""

    query: str
    limit: Optional[int] = Field(default=5, le=20, ge=1)
    section: Optional[SearchSection] = Field(default="top")
    language: Optional[Languages] = Field(default="en")
    min_replies: Optional[int] = Field(default=None, ge=0)
    min_likes: Optional[int] = Field(default=None, ge=0)
    min_retweets: Optional[int] = Field(default=None, ge=0)
    start_date: Optional[str] = Field(
        default=None,
        regex=r"^\d{4}-\d{2}-\d{2}$",
    )
    end_date: Optional[str] = Field(default=None, regex=r"^\d{4}-\d{2}-\d{2}$")

    @validator("start_date", "end_date")
    def validate_start_date(cls, value):
        if value is not None:
            return datetime.strptime(value, "%Y-%m-%d")
        return value


class SearchContinuationRequest(SearchRequest):
    """Tweet Id Request Schema"""

    continuation_token: str


class SearchResponse(BaseModel):
    """Search Response Schema"""

    results: List[Optional[Dict]]
    continuation_token: Optional[str] = None


@router.post("/", response_model=SearchResponse)
def post_search(data: SearchRequest):
    """Return Tweet search"""
    try:
        return Search().search(
            query=data.query,
            mode=data.section,
            count=data.limit,
            language=data.language,
            min_replies=data.min_replies,
            min_likes=data.min_likes,
            min_retweets=data.min_retweets,
            start_date=data.start_date,
            end_date=data.end_date,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/", response_model=SearchResponse)
def get_search(
    query: str,
    section: Optional[SearchSection] = Query(default=SearchSection.TOP),
    limit: Optional[int] = Query(default=5, ge=1, le=20),
    language: Optional[Languages] = Query(default=Languages.ENGLISH),
    min_replies: Optional[int] = Query(default=None, ge=0),
    min_likes: Optional[int] = Query(default=None, ge=0),
    min_retweets: Optional[int] = Query(default=None, ge=0),
    start_date: Optional[str] = Query(
        default=None, regex=r"^\d{4}-\d{2}-\d{2}$", description="YYYY-MM-DD"
    ),
    end_date: Optional[str] = Query(default=None, regex=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Return Tweet search"""
    try:
        return Search().search(
            query=query,
            mode=section,
            count=limit,
            language=language,
            min_replies=min_replies,
            min_likes=min_likes,
            min_retweets=min_retweets,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post(
    "/continuation",
    response_model=SearchResponse,
)
def post_search_continuation(data: SearchContinuationRequest):
    """Return Tweet search"""
    try:
        return Search().search(
            query=data.query,
            mode=data.section,
            count=data.limit,
            language=data.language,
            min_replies=data.min_replies,
            min_likes=data.min_likes,
            min_retweets=data.min_retweets,
            continuation_token=data.continuation_token,
            start_date=data.start_date,
            end_date=data.end_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get(
    "/continuation",
    response_model=SearchResponse,
)
def get_search_continuation(
    query: str,
    section: Optional[SearchSection] = Query(default=SearchSection.TOP),
    limit: Optional[int] = Query(default=5, ge=1, le=20),
    continuation_token: Optional[str] = None,
    language: Optional[Languages] = Query(default=Languages.ENGLISH),
    min_replies: Optional[int] = Query(default=None, ge=0),
    min_likes: Optional[int] = Query(default=None, ge=0),
    min_retweets: Optional[int] = Query(default=None, ge=0),
    start_date: Optional[str] = Query(
        default=None, regex=r"^\d{4}-\d{2}-\d{2}$", description="YYYY-MM-DD"
    ),
    end_date: Optional[str] = Query(default=None, regex=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Return Tweet search"""
    try:
        return Search().search(
            query=query,
            mode=section,
            count=limit,
            language=language,
            min_replies=min_replies,
            min_likes=min_likes,
            min_retweets=min_retweets,
            continuation_token=continuation_token,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
