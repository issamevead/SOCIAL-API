import json
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import quote

import requests
from src.utils.constantes import *
from src.utils.util import json_extract


@dataclass
class TagPost:
    post_id: int
    shortcode: str

    media_caption: str
    media_likes_number: Optional[int]
    media_comments_number: Optional[int]
    images: List[str]


@dataclass
class InstagramRequest:
    tag: str
    post_per_call: int = field(default=12)
    max_iteration: int = field(default=20)
    cursor: str = field(default="")


@dataclass
class TagPosts:
    tag: str = field(default="")
    number_of_posts: int = field(default=50)
    posts: List[TagPost] = field(default_factory=list)


class InstagramTagScrapper:
    def __init__(self, request: InstagramRequest, posts: TagPosts) -> None:
        self.request = request
        self.tag_posts = posts
        self.initiate()

    def initiate(self):
        url = URL_WEB_HASHTAG_QUERY.format(self.request.tag)
        response = self.get(url, headers=HASHTAG_HEADERS)
        self.tag_posts.tag = self.request.tag
        if response is not None and response.status_code == 200:
            new_posts, self.request.cursor = self.instagram_tag_call_parser(
                response.json()
            )
            self.tag_posts.posts.extend(new_posts)

    def instagram_tag_call_parser(self, response_json: dict):
        self.tag_posts.number_of_posts = response_json.get("count", None)
        end_cursor = json_extract(response_json, "end_cursor")

        edge_hashtag_to_media = (
            response_json.get("data", {})
            .get("hashtag", {})
            .get("edge_hashtag_to_media", {})
        )
        nodes = json_extract(edge_hashtag_to_media, "node")
        posts = []
        for node in nodes:
            post_id = node.get("id", None)
            shortcode = node.get("shortcode", None)

            media_caption = json_extract(node, "text")
            caption_text = media_caption[0] if len(media_caption) > 0 else ""

            media_likes_number = json_extract(
                json_extract(node, "edge_liked_by"), "count"
            )
            n_likes = media_likes_number[0] if len(media_likes_number) > 0 else None

            media_comments_number = json_extract(
                json_extract(node, "edge_media_to_comment"), "count"
            )
            n_comments = (
                media_comments_number[0] if len(media_comments_number) > 0 else None
            )

            images = json_extract(node, "display_url")
            posts.append(
                TagPost(post_id, shortcode, caption_text, n_likes, n_comments, images)
            )
        return posts, end_cursor

    def get_next_page(self):
        return {
            "tag_name": self.request.tag,
            "first": self.request.post_per_call,
            "after": self.request.cursors[-1] if len(self.request.cursors) > 0 else "",
        }

    def process(self):
        for _ in range(self.request.max_iteration):
            query_hatag_vars = self.get_next_page()
            a = quote(str(query_hatag_vars).replace(" ", "").replace("'", '"'))
            url = URL_HASHTAG_QUERY.format(self.request.tag, a)
            response = requests.get(url)
            if response is not None and response.status_code == 200:
                new_posts, self.request.cursor = self.instagram_tag_call_parser(
                    response.json()
                )
                if self.request.cursor is None or len(new_posts.posts) == 0:
                    break
                self.tag_posts.posts.extend(new_posts)


# a = InstagramTagScrapper(
#     BaseInfo(5, get_()), InstagramRequest("wordcup"), TagPosts()
# )
