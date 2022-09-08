from collections import namedtuple
from dataclasses import dataclass
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from requests import get
from src.utils.util import json_extract
import requests
from src.log.logger import Logs
from src.models.unsplash.photos import Image, ImageVersion

log = Logs()

LinksCoverPhoto = namedtuple(
    "LinksCoverPhoto",
    field_names=["html", "download", "download_location"],
    defaults=[None, None, None],
)

LinksCollection = namedtuple(
    "LinksCollection",
    field_names=["html", "photos", "related", "self"],
    defaults=[None, None, None, None],
)


class CoverPhoto(BaseModel):
    alt_description: Optional[str]
    blur_hash: Optional[str]
    description: Optional[str]
    likes: Optional[int]
    links: Optional[LinksCoverPhoto]


class CollectionRequest(BaseModel):
    page: Optional[int] = Field(1, ge=1, le=1000)
    per_page: Optional[int] = Field(10, ge=1, le=30)
    share_key: Optional[str]


class Collection(BaseModel):
    collection_id: str
    published_at: Optional[str]
    share_key: Optional[str]
    total_photos: Optional[int]
    title: Optional[str]
    updated_at: Optional[str]
    links: Optional[LinksCollection] = Field(default_factory=LinksCollection)
    cover_photo: Optional[CoverPhoto] = Field(default_factory=CoverPhoto)

    def get_collection_details(self):
        for i in range(3):
            try:
                url = f"https://unsplash.com/collections/{self.collection_id}"
                response = get(url, timeout=3)
                response = get(f"https://unsplash.com/collections/{9679712}")
                r = (
                    response.text.split(
                        '<script>window.__INITIAL_STATE__ = JSON.parse("'
                    )[1]
                    .split("</script>")[0]
                    .strip()[:-3]
                )
                r = r.encode().decode("unicode_escape")
                script = json_extract(json.loads(r), self.collection_id)[0]
                self._parse_collection(script)
                return self
            except requests.exceptions.RequestException as error:
                log.error(f"try number: {i} failed with error: {error}")
                continue
            except Exception as e:
                log.error(f"Error: {e}")
                continue
        raise Exception("Failed to get collection details")

    def _parse_collection(self, script: Dict):
        self.collection_id = script.get("id")
        self.published_at = script.get("published_at")
        self.share_key = script.get("share_key")
        self.total_photos = script.get("total_photos")
        self.title = script.get("title")
        self.updated_at = script.get("updated_at")
        self.total_photos = script.get("total_photos")
        self.links = LinksCollection(
            html=script.get("links", {}).get("html"),
            photos=script.get("links", {}).get("photos"),
            related=script.get("links", {}).get("related"),
            self=script.get("links", {}).get("self"),
        )
        self.cover_photo = CoverPhoto(
            alt_description=script.get("cover_photo", {}).get("alt_description"),
            blur_hash=script.get("cover_photo", {}).get("blur_hash"),
            description=script.get("cover_photo", {}).get("description"),
            likes=script.get("cover_photo", {}).get("likes"),
            links=LinksCoverPhoto(
                html=script.get("cover_photo", {}).get("links", {}).get("html"),
                download=script.get("cover_photo", {}).get("links", {}).get("download"),
                download_location=script.get("cover_photo", {})
                .get("links", {})
                .get("download_location"),
            ),
        )

    def get_collection_photos(self, req: CollectionRequest):
        url = f"https://unsplash.com/napi/collections/{self.collection_id}/photos?per_page={req.per_page}&order_by=latest&page={req.page}&share_key={req.share_key}&xp=unsplash-plus-2%3AControl"
        headers = {
            "authority": "unsplash.com",
            "accept": "*/*",
            "accept-language": "en",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://unsplash.com/collections/{collection_id}",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        }
        for i in range(3):
            try:
                response = get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        images = self._parse_collection_images(response.json())
                        return images
                    except json.JSONDecodeError as e:
                        log.error(f"Error: {e}")
                        continue
            except requests.exceptions.RequestException as error:
                log.error(f"try number: {i} failed with error: {error}")
                continue
        raise Exception("Failed to get collection images")

    def _parse_collection_images(self, images: List[dict]):
        return [
            Image(
                alt_description=image.get("alt_description"),
                created_at=image.get("created_at"),
                description=image.get("description"),
                height=image.get("height"),
                image_id=image.get("id"),
                number_of_likes=image.get("likes"),
                url_versions=ImageVersion(
                    full=image.get("urls", {}).get("full"),
                    regular=image.get("urls", {}).get("regular"),
                    small=image.get("urls", {}).get("small"),
                    thumb=image.get("urls", {}).get("thumb"),
                ),
            )
            for image in images
        ]
