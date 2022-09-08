"""Tweet Router"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.models.twitter.user import User
from src.models.twitter.tweet import Tweet

router = APIRouter(prefix="/twitter/tweet", tags=["Twitter"])


class TweetDetailsRequest(BaseModel):
    """Tweet Id Request Schema"""

    tweet_id: str


class TweetDetailsResponse(BaseModel):
    """Schema Class for a Tiktok Tweet Details"""

    tweet_id: Optional[str]
    creation_date: Optional[str]
    text: Optional[str]
    media_url: Optional[List[str]]
    user: Optional[User]
    retweet_count: Optional[int]
    favorite_count: Optional[int]
    reply_count: Optional[int]
    quote_count: Optional[int]
    retweet: Optional[bool]
    video_view_count: Optional[int] = None


@router.post("/details", response_model=TweetDetailsResponse)
def post_tweet_details(data: TweetDetailsRequest):
    """Return Tweet Id"""
    try:
        return Tweet().get_tweet_details(data.tweet_id)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/details", response_model=TweetDetailsResponse)
def get_tweet_details(tweet_id: str):
    """Return Tweet Details"""
    try:
        return Tweet().get_tweet_details(tweet_id)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
