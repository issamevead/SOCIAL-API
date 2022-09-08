from fastapi import APIRouter, HTTPException
from src.models.instagram.user import UserRestrictedInfos
from src.models.instagram.post import Post
from pydantic import BaseModel

router = APIRouter(prefix="/instagram/post", tags=["Instagram"])


class OnePostResponse(BaseModel):
    user: UserRestrictedInfos
    post: Post


@router.get("/details", response_model=OnePostResponse)
def get_post_infos(shortcode: str):
    try:
        user, post = Post(shortcode=shortcode).get_post_details()
        return OnePostResponse(user=user, post=post)
    except ValueError as e:
        raise HTTPException(status_code=406, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
