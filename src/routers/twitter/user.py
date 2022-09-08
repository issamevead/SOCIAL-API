"""User Router"""
from optparse import Option
from typing import Dict, Optional, List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.models.twitter.user import User
from src.models.twitter.tweet import Tweet

router = APIRouter(prefix="/twitter/user", tags=["Twitter"])


class UserDetailsRequest(BaseModel):
    """User Id Request Schema"""

    username: str


class UserIdRequest(BaseModel):
    """User Id Request Schema"""

    user_id: int


class UserFollowingRequest(UserIdRequest):
    """User Followers Request Schema"""

    limit: Optional[int] = Query(default=10)


class UserFollowing(BaseModel):
    """Search Response Schema"""

    results: List[Optional[User]]
    continuation_token: Optional[str] = None


class UserFollowingContinuationRequest(UserFollowingRequest):
    """Tweet Id Request Schema"""

    continuation_token: str


class UserTweetsRequest(UserDetailsRequest):
    """User Id Request Schema"""

    limit: Optional[int] = Field(default=10, le=20, ge=1)


class UserTweetsContinuationRequest(UserTweetsRequest):
    """Tweet Id Request Schema"""

    continuation_token: str


class UserTweets(BaseModel):
    """Search Response Schema"""

    results: List[Optional[Tweet]]
    continuation_token: Optional[str] = None


@router.post("/id", response_model=Dict)
def post_user_id(data: UserIdRequest):
    """Return User Details"""
    try:
        return User().get_username_by_id(data.user_id)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/id", response_model=Dict)
def get_user_id(user_id: int):
    """Return User Details"""
    try:
        return User().get_username_by_id(user_id)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/details", response_model=User)
def post_user_details(data: UserDetailsRequest):
    """Return User Details"""
    try:
        return User().get_user_details(data.username)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/details", response_model=User)
def get_user_details(username: str):
    """Return User Details"""
    try:
        return User().get_user_details(username)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/tweets", response_model=UserTweets)
def post_user_tweets(data: UserTweetsRequest):
    """Return User Id"""
    try:
        return User().get_user_tweets(data.username, data.limit)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/tweets", response_model=UserTweets)
def get_user_tweets(
    username: str, limit: Optional[int] = Query(default=40, ge=1, le=100)
):
    """Return User Details"""
    try:
        return User().get_user_tweets(username, limit)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/tweets/continuation", response_model=UserTweets)
def post_user_tweets(data: UserTweetsContinuationRequest):
    """Return User Id"""
    try:
        return User().get_user_tweets(
            data.username, data.limit, data.continuation_token
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/tweets/continuation", response_model=UserTweets)
def get_user_tweets(
    username: str,
    limit: Optional[int] = Query(default=40, ge=1, le=100),
    continuation_token: Optional[str] = Query(default=None),
):
    """Return User Details"""
    try:
        return User().get_user_tweets(username, limit, continuation_token)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/following", response_model=UserFollowing)
def post_user_following(data: UserFollowingRequest):
    """Return User Id"""
    try:
        return User().get_user_following(data.user_id, data.limit)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/following", response_model=UserFollowing)
def get_user_following(
    user_id: str, limit: Optional[int] = Query(default=40, ge=1, le=100)
):
    """Return User Details"""
    try:
        return User().get_user_following(user_id, limit)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/following/continuation", response_model=UserFollowing)
def post_user_following_continuation(data: UserFollowingContinuationRequest):
    """Return User Id"""
    try:
        return User().get_user_following(
            data.user_id, data.limit, data.continuation_token
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/following/continuation", response_model=UserFollowing)
def get_user_following_continuation(
    user_id: str,
    limit: Optional[int] = Query(default=40, ge=1, le=100),
    continuation_token: Optional[str] = Query(None),
):
    """Return User Details"""
    try:
        return User().get_user_following(user_id, limit, continuation_token)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/followers", response_model=UserFollowing)
def post_user_followers(data: UserFollowingRequest):
    """Return User Id"""
    try:
        return User().get_user_followers(data.user_id, data.limit)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/followers", response_model=UserFollowing)
def get_user_followers(
    user_id: str, limit: Optional[int] = Query(default=10, ge=1, le=20)
):
    """Return User Details"""
    try:
        return User().get_user_followers(user_id, limit)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/followers/continuation", response_model=UserFollowing)
def post_user_followers_continuation(data: UserFollowingContinuationRequest):
    """Return User Id"""
    try:
        return User().get_user_followers(
            data.user_id, data.limit, data.continuation_token
        )
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/followers/continuation", response_model=UserFollowing)
def get_user_followers_continuation(
    user_id: str,
    limit: Optional[int] = Query(default=10, ge=1, le=20),
    continuation_token: Optional[str] = Query(None),
):
    """Return User Details"""
    try:
        return User().get_user_followers(user_id, limit, continuation_token)
    except ValueError as error:
        raise HTTPException(status_code=200, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
