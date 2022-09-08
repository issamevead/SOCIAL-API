from __future__ import annotations
from json import JSONDecodeError
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional
from requests import get
import requests
from src.log.logger import Logs


@dataclass
class ImageVersion:
    full: Optional[str]
    regular: Optional[str]
    small: Optional[str]
    thumb: Optional[str]


@dataclass
class Image:
    alt_description: Optional[int]
    created_at: Optional[int]
    description: Optional[str]
    height: Optional[str]
    image_id: Optional[str]
    number_of_likes: Optional[int]
    url_versions: Optional[ImageVersion]


class BaseRequest(BaseModel):
    """Collections Request Schema"""

    keyword: str
    page: Optional[int] = Field(ge=1, default=1)
    per_page: Optional[int] = Field(ge=20, default=20)


class Photos(BaseModel):
    alt_description: Optional[str]
    blur_hash: Optional[str]
    color: Optional[str]
    created_at: Optional[str]
    description: Optional[str]
    height: Optional[int]
    id: Optional[str]
    likes: Optional[int]
    promoted_at: Optional[str]
    updated_at: Optional[str]
    urls: Optional[ImageVersion]
    width: Optional[int]

    def get_photos(self, req: BaseRequest):
        url = f"https://unsplash.com/napi/search/photos?query={req.keyword}&per_page={req.per_page}&page={req.page}&xp=unsplash-plus-2%3AControl"
        headers = {
            "authority": "unsplash.com",
            "accept": "*/*",
            "accept-language": "en",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://unsplash.com/s/photos/{req.keyword}",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        }
        for _ in range(3):
            try:
                response = get(url, headers=headers)
                if response.status_code == 200:
                    photots = self._parse_photos(response.json())
                    return photots
            except JSONDecodeError as error:
                raise ValueError("Invalid JSON response") from error
            except requests.exceptions.RequestException as error:
                Logs.error(f"Error while getting user details: {error}")
                continue
        raise ValueError("Unable to get user details")

    def _parse_photos(self, response: dict):
        return [
            Photos(
                alt_description=photo["alt_description"],
                blur_hash=photo["blur_hash"],
                color=photo["color"],
                created_at=photo["created_at"],
                description=photo["description"],
                height=photo["height"],
                id=photo["id"],
                likes=photo["likes"],
                promoted_at=photo["promoted_at"],
                updated_at=photo["updated_at"],
                urls=ImageVersion(
                    full=photo["urls"]["full"],
                    regular=photo["urls"]["regular"],
                    small=photo["urls"]["small"],
                    thumb=photo["urls"]["thumb"],
                ),
                width=photo["width"],
            )
            for photo in response.get("results", [])
        ]
