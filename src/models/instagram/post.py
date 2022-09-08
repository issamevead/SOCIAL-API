from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from requests import get
from src.utils.util import json_extract
from src.utils.proxies import Proxies 


class PostTools(Enum):
    URL = "https://www.instagram.com/graphql/query/?query_hash=9f8827793ef34641b2fb195d4d41151c&variables=%7B%22shortcode%22%3A%22{}%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D"
    HEADERS = {
        "authority": "www.instagram.com",
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "cache-control": "no-cache",
        "cookie": "csrftoken=EpHabi7NeB3vNcTsv2EE3zVKWO8Fv2u7; mid=YwyQ8AALAAEY5GhwK_L--_FtVZ3l; ig_did=3011A2E6-F517-4E09-A0E7-3AE2A4CDBD82; ig_nrcb=1; datr=oasMY2v3tyV6vm1bXSEZ7pL9; csrftoken=5EaeghvFnfZdJ2FhuX9rH6CnFwU6Idaa; ig_did=456545FC-015E-4F1F-9432-CC858F153006; ig_nrcb=1; mid=YwZVowALAAF9NbINoRJlwldd6o7w",
        "pragma": "no-cache",
        "referer": "https://www.instagram.com/p/{}/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "viewport-width": "896",
        "x-asbd-id": "198387",
        "x-csrftoken": "EpHabi7NeB3vNcTsv2EE3zVKWO8Fv2u7",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "0",
        "x-instagram-ajax": "1006124192",
        "x-requested-with": "XMLHttpRequest",
    }


class TagUser(BaseModel):
    username: str
    user_id: int
    user_full_name: str
    profile_pic_url: str
    is_verified: bool


class PostRestrictedInfos(BaseModel):
    shortcode: str
    post_id: Optional[int]
    media_caption: Optional[str]
    media_likes_number: Optional[int]
    media_comments_number: Optional[int]
    images: List[str] = Field(default_factory=list)


class Post(PostRestrictedInfos):
    is_video: Optional[bool]
    is_ad: Optional[bool]
    video_url: Optional[str]
    video_play_count: Optional[int]
    video_duration: Optional[float]
    video_views_count: Optional[int]
    comments_disabled: Optional[bool]
    is_paid_partnership: Optional[bool]
    location: Optional[str]
    tagged_users: Optional[List[TagUser]] = Field(default_factory=list)
    dimensions: Dict[str, int] = Field(default_factory=dict)

    def _instagram_post_parser(self, json_data):
        from src.models.instagram.user import UserRestrictedInfos

        if json_data["status"] == "ok":
            shortcode_media = json_data.get("data", {}).get("shortcode_media", {})

            self.post_id = shortcode_media.get("id")
            self.shortcode = shortcode_media.get("shortcode")

            media_caption = json_extract(
                shortcode_media.get("edge_media_to_caption", {}).get("edges", {}),
                "text",
            )
            if media_caption is not None and len(media_caption) > 0:
                self.media_caption = " ".join(media_caption)

            self.media_likes_number = shortcode_media.get(
                "edge_media_preview_like", {}
            ).get("count", 0)
            self.media_comments_number = shortcode_media.get(
                "edge_media_to_parent_comment", {}
            ).get("count", 0)
            self.images = json_extract(shortcode_media, "display_url")

            self.is_video = shortcode_media.get("is_video")
            self.is_ad = shortcode_media.get("is_ad")
            self.video_url = shortcode_media.get(
                "video_url",
            )
            self.video_play_count = shortcode_media.get("video_view_count")
            self.video_duration = shortcode_media.get("video_duration")
            self.video_views_count = shortcode_media.get("video_view_count")
            self.comments_disabled = shortcode_media.get("comments_disabled")
            self.is_paid_partnership = shortcode_media.get("is_paid_partnership")
            self.location = shortcode_media.get("location")
            self.dimensions = shortcode_media.get("dimensions")

            tagged_users = json_extract(
                shortcode_media.get("edge_media_to_tagged_user", {}).get("edges", {}),
                "node",
            )
            self.tagged_users = [
                TagUser(
                    username=user.get("user", {}).get("username"),
                    user_id=user.get("user", {}).get("id"),
                    user_full_name=user.get("user", {}).get("full_name"),
                    profile_pic_url=user.get("user", {}).get("profile_pic_url"),
                    is_verified=user.get("user", {}).get("is_verified"),
                )
                for user in tagged_users
            ]
            user = UserRestrictedInfos(
                username=shortcode_media.get("owner", {}).get("username"),
                user_id=shortcode_media.get("owner", {}).get("id"),
                user_full_name=shortcode_media.get("owner", {}).get("full_name"),
                profile_pic_url=shortcode_media.get("owner", {}).get("profile_pic_url"),
                is_verified=shortcode_media.get("owner", {}).get("is_verified"),
            )
            return user

    def get_post_details(self) -> Post:

        url = PostTools.URL.value.format(self.shortcode)
        PostTools.HEADERS.value["referer"] = PostTools.HEADERS.value["referer"].format(
            self.shortcode
        )
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            try:
                proxy = next(proxies)
                proxy = proxies.to_dict()
                response = get(
                    url, headers=PostTools.HEADERS.value, proxies=proxy, timeout=10
                )
                user = self._instagram_post_parser(response.json())
                return user, self
            except StopIteration:
                raise Exception("No proxy left")
            except Exception:
                continue
        raise Exception("user has no post")
