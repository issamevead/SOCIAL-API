from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.models.instagram.post import PostRestrictedInfos
from src.models.instagram.user import User
from src.models.instagram.reel import Reel, ReelPostRequest, ReelPostRequestContinuation

router = APIRouter(prefix="/instagram/user", tags=["Instagram"])


class UserPostsResponse(BaseModel):
    continuation_token: Optional[str]
    posts: List[PostRestrictedInfos]


class UserPostsResponseExtended(UserPostsResponse):
    user = User


class UserReelsResponse(BaseModel):
    reels: List[Reel]
    continuation_token: Optional[str]


class UserReelsResponseExtended(UserReelsResponse):
    user: User


@router.get("/details", response_model=User)
def get_user_infos(username: str):
    try:
        user, _ = User(username=username).get_user_details()
        return user
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e


@router.get("/posts", response_model=UserPostsResponseExtended)
def get_user_posts(
    username: str, number_of_posts: Optional[int] = Query(default=50, ge=1, le=50)
):
    try:
        user, posts, cursor = User(username=username).get_user_posts(number_of_posts)
        return UserPostsResponseExtended(
            user=user, posts=posts, continuation_token=cursor
        )
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e


@router.get("/posts/continuation", response_model=UserPostsResponse)
def get_users_posts_continuation(
    username: str,
    user_id: str,
    continuation_token: str,
    number_of_posts: int = Query(default=50, ge=1, le=50),
):
    try:
        posts, cursor = User(
            username=username, user_id=user_id
        ).get_user_posts_continuation(number_of_posts, continuation_token)
        return UserPostsResponse(posts=posts, continuation_token=cursor)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e


@router.post("/reels", response_model=UserReelsResponseExtended)
def get_user_reels(account: ReelPostRequest):
    try:
        user, reels, cursor = User(username=account.username).get_user_reels(account)
        return UserReelsResponseExtended(
            user=user, reels=reels, continuation_token=cursor
        )
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e


@router.post("/reels/continuation", response_model=UserReelsResponse)
def get_user_reels_continuation(account: ReelPostRequestContinuation):
    try:
        reels, cursor = User(
            username=account.username, user_id=account.user_id
        ).get_user_reels_continuation(account)
        return UserReelsResponse(reels=reels, continuation_token=cursor)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
