from __future__ import annotations

from typing import List, Optional
from urllib.parse import quote

import requests
from pydantic import BaseModel, Field
from requests import post
from src.log.logger import Logs
from src.models.instagram.post import PostRestrictedInfos
from src.models.instagram.reel import (Dimension, Reel, ReelPostRequest,
                                       ReelPostRequestContinuation, ReelTools,
                                       ReelVersion)
from src.utils.proxies import Proxies
from src.utils.util import json_extract

QUERY_HASH = "69cba40317214236af40e7efa697781d"
cursor = ""

log = Logs()


class UserRestrictedInfos(BaseModel):
    username: str
    user_id: Optional[int]
    is_private: Optional[bool]
    is_verified: Optional[bool]
    profile_pic_url: Optional[str]
    user_full_name: Optional[str]


class User(UserRestrictedInfos):
    is_professional_account: Optional[bool]
    number_of_followers: Optional[int]
    number_of_following: Optional[int]
    number_of_posts: Optional[int]
    biography: Optional[str]
    external_url: Optional[str]
    related_users: List[UserRestrictedInfos] = Field(default_factory=list)

    def _get_next_vars(self, cursor, number_of_posts) -> str:
        """Formulate variables for the query."""
        return {
            "id": self.user_id,
            "first": number_of_posts,
            "after": cursor,
        }

    def _instagram_call(self, query_hash, cursor: str, number_of_posts) -> dict:
        var = self._get_next_vars(cursor, number_of_posts)
        a = quote(str(var).replace(" ", "").replace("'", '"'))
        url = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={a}"
        headers = {
            "authority": "www.instagram.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9",
            "cookie": "ig_nrcb=1; csrftoken=hf5MXNY4XWrWJSRqG9NUdTkf6GRl6dfu; mid=YwZR3gALAAFeLOglEDRYh02J7tJF; ig_did=B90D69C8-27AF-45D1-A023-FEAD2DE9E41A; datr=tjUHY1_GtwW19NgjLFIw5rTC; csrftoken=5EaeghvFnfZdJ2FhuX9rH6CnFwU6Idaa; ig_did=456545FC-015E-4F1F-9432-CC858F153006; ig_nrcb=1; mid=YwZVowALAAF9NbINoRJlwldd6o7w",
            "referer": f"https://www.instagram.com/{self.username}/",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "viewport-width": "612",
            "x-asbd-id": "198387",
            "x-csrftoken": "hf5MXNY4XWrWJSRqG9NUdTkf6GRl6dfu",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
            "x-requested-with": "XMLHttpRequest",
        }
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            try:
                proxy = next(proxies)
                response = requests.get(
                    url, headers=headers, proxies=proxy.to_dict(), timeout=15
                )
            except StopIteration:
                raise Exception("No proxy left")
            except Exception:
                continue
            if response is not None and response.status_code == 200:
                return response.json()
        return {"status": "error"}

    def _instagram_post_parser(self, response_json):
        if response_json["status"] == "ok":
            user_data = response_json.get("data", {}).get("user", None)
            if user_data is None:
                return [], ""
            nodes = json_extract(
                user_data.get("edge_owner_to_timeline_media", {}).get("edges", []),
                "node",
            )
            cursor_info = user_data.get("edge_owner_to_timeline_media", {}).get(
                "page_info", {}
            )
            posts = []
            for node in nodes:
                post_id = node.get("id")
                shortcode = node.get("shortcode")
                captions = json_extract(node["edge_media_to_caption"], "text")
                captions = " ".join(captions)
                likes = json_extract(node.get("edge_media_preview_like", {}), "count")
                n_likes = likes[0] if likes else 0
                comments = json_extract(node.get("edge_media_to_comment", {}), "count")
                n_comments = comments[0] if comments else 0
                images = json_extract(node, "display_url")
                posts.append(
                    PostRestrictedInfos(
                        post_id=post_id,
                        shortcode=shortcode,
                        media_caption=captions,
                        media_likes_number=n_likes,
                        media_comments_number=n_comments,
                        images=images,
                    )
                )
            return posts, cursor_info.get("end_cursor")

    def _instagram_details_parser(self, response):
        try:
            rows = response["data"]["user"]
        except:
            return None
        cursor = (
            rows.get("edge_owner_to_timeline_media", {})
            .get("page_info", {})
            .get("end_cursor")
        )
        self.number_of_posts = rows.get("edge_owner_to_timeline_media", {}).get("count")
        self.number_of_followers = rows.get("edge_followed_by", {}).get("count")
        self.number_of_following = rows.get("edge_follow", {}).get("count")

        self.user_id = rows.get("id")
        self.biography = rows.get("biography")
        self.user_full_name = rows.get("full_name")
        self.is_professional_account = rows.get("is_business_account")
        self.external_url = rows.get("external_url")
        self.profile_pic_url = rows.get(
            "profile_pic_url_hd", rows.get("profile_pic_url")
        )
        self.is_private = rows.get("is_private")
        self.is_verified = rows.get("is_verified")
        for e in json_extract(rows.get("edge_related_profiles", {}), "node"):
            self.related_users.append(
                UserRestrictedInfos(
                    username=e.get("username"),
                    user_id=e.get("id"),
                    profile_pic_url=e.get(
                        "profile_pic_url",
                    ),
                    user_full_name=e.get("full_name"),
                    is_private=e.get("is_private"),
                    is_verified=e.get("is_verified"),
                )
            )
        return cursor

    def get_user_details(self):
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.username}"
        headers = {
            "authority": "i.instagram.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9",
            "cookie": "_js_ig_did=4743D1B2-888A-4199-BD97-63849C03070B; _js_datr=3VEGYwDc4o1YXpvN---R3dcB; csrftoken=5EaeghvFnfZdJ2FhuX9rH6CnFwU6Idaa; ig_did=456545FC-015E-4F1F-9432-CC858F153006; ig_nrcb=1; mid=YwZVowALAAF9NbINoRJlwldd6o7w",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "x-asbd-id": "198387",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
        }
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            proxy = next(proxies)
            try:
                response = requests.get(
                    url, headers=headers, proxies=proxy.to_dict(), timeout=10
                )
                if response is not None and response.status_code == 200:
                    cursor = self._instagram_details_parser(response.json())
                    return self, cursor
            except requests.exceptions.RequestException as error:
                log.error(
                    f"Error while getting user details: {error} using proxy {proxy}"
                )
            except StopIteration:
                raise StopIteration("No proxy left")
        raise ValueError(f"Unable to get user details for username: {self.username}")

    def get_user_posts(
        self, number_of_posts: int, cursor=None
    ) -> List[PostRestrictedInfos]:
        """Get the posts of the user."""
        if cursor is None:
            user, cursor = self.get_user_details()
            if user.is_private is True:
                raise ValueError(
                    f"user {self.username} is private, thus we cannot get its posts"
                )
        if cursor is None:
            raise Exception(f"unable to get user posts for user: {self.username}")

        call = self._instagram_call(QUERY_HASH, cursor, number_of_posts)
        posts, new_cursor = self._instagram_post_parser(call)
        return user, posts, new_cursor

    def get_user_posts_continuation(
        self, number_of_posts: int, cursor=None
    ) -> List[PostRestrictedInfos]:
        """Get the posts of the user."""
        if cursor is None:
            raise Exception(f"unable to get user posts for user: {self.username}")

        call = self._instagram_call(QUERY_HASH, cursor, number_of_posts)
        posts, new_cursor = self._instagram_post_parser(call)
        return posts, new_cursor

    def _reel_parser(self, data):
        reels_data = []
        reels = json_extract(data.get("items", []), "media")
        cursor = data.get("paging_info", {}).get("max_id")
        for reel in reels:
            eel = Reel(reel_pk=reel.get("pk"))
            eel.reel_shortcode = reel.get("code")
            eel.reel_id = reel.get("id")
            eel.reel_caption = (
                reel.get("caption", {}).get("text")
                if reel.get("caption", {}) is not None
                else None
            )
            eel.number_of_comments = reel.get("comment_count")
            eel.number_of_likes = reel.get("like_count")
            eel.reel_view_count = reel.get("view_count")
            eel.reel_play_count = reel.get("play_count")
            eel.reel_dimensions = Dimension(
                reel.get("original_width"),
                reel.get("original_height"),
            )
            eel.has_audio = reel.get("has_audio")
            eel.has_shared_to_fb = reel.get("has_shared_to_fb")
            eel.can_viewer_save = reel.get("can_viewer_save")
            eel.can_viewer_reshare = reel.get("can_viewer_reshare")
            eel.reel_duration = reel.get("video_duration")
            eel.reel_versions = [
                ReelVersion(**version) for version in reel.get("video_versions", [])
            ]
            reels_data.append(eel)
        return reels_data, cursor

    def get_user_reels(self, load: ReelPostRequest):
        user, _ = self.get_user_details()
        if user.user_id is None:
            raise ValueError(f"unable to get user id for user: {self.username}")
        payload = f"target_user_id={user.user_id}&page_size={load.page_size}&include_feed_video=true"
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            try:
                proxy = next(proxies)
                response = post(
                    ReelTools.URL_USER_REELS.value,
                    headers=ReelTools.HEADERS_USER_REELS.value,
                    data=payload,
                    proxies=proxy.to_dict(),
                )
                if response.status_code == 200:
                    reels, cursor = self._reel_parser(response.json())
                    return user, reels, cursor
            except StopIteration:
                raise StopIteration("no more proxies")
            except Exception:
                continue
        return user, [], None

    def get_user_reels_continuation(self, load: ReelPostRequestContinuation):
        payload = f"target_user_id={load.user_id}&page_size={load.page_size}&include_feed_video=true&max_id={load.continuator_token}"
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            try:
                proxy = next(proxies)
                response = post(
                    ReelTools.URL_USER_REELS.value,
                    headers=ReelTools.HEADERS_USER_REELS.value,
                    data=payload,
                    proxies=proxy.to_dict(),
                )
                if response.status_code == 200:
                    return self._reel_parser(response.json())
            except StopIteration:
                raise StopIteration("No proxy left")
            except Exception:
                continue
        return [], None
