from json import JSONDecodeError
from typing import Dict, List, Optional

import requests
from pydantic import BaseModel, Field
from requests import get

from src.log.logger import Logs
from src.models.unsplash.photos import BaseRequest
from src.models.unsplash.collection import (
    Collection,
    CoverPhoto,
    LinksCollection,
    LinksCoverPhoto,
)

log = Logs()


class CollectionsRequest(BaseModel):
    keyword: str
    page: int = Field(default=1)
    per_page: int = Field(default=20)


class Collections(BaseModel):

    total: Optional[int]
    total_pages: Optional[int]
    collections: List[Collection] = Field(default_factory=list)

    def get_collections_related_to_keyword(self, req: BaseRequest):
        url = f"https://unsplash.com/napi/search/collections?query={req.keyword}&per_page={req.per_page}&page={req.page}&xp=unsplash-plus-2%3AControl"
        headers = {
            "authority": "unsplash.com",
            "accept": "*/*",
            "accept-language": "en",
            "cache-control": "no-cache",
            "cookie": "ugid=87bbe79c5cfaaf2526cb97153351d4955541872; xp-unsplash-plus-2=Control; lux_uid=166256177240584319; _sp_ses.0295=*; uuid=5a65b390-2ebb-11ed-8c11-dff4a3ef6282; xpos=%7B%7D; _ga=GA1.2.182237806.1662561773; _gid=GA1.2.1954460327.1662561773; _gat=1; _sp_id.0295=7fd36639-7801-48fe-8387-caed8d718c89.1662561772.1.1662561793.1662561772.c8a9fed2-b5c0-4760-976b-d4a2cbe21b5c; ugid=87bbe79c5cfaaf2526cb97153351d4955541872",
            "pragma": "no-cache",
            "referer": f"https://unsplash.com/s/collections/{req.keyword}",
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
                    self._parse_collections(response.json())
                    return self
            except JSONDecodeError as error:
                raise ValueError("Invalid JSON response") from error
            except requests.exceptions.RequestException as error:
                log.error(f"Error while getting user details: {error}")
                continue
        raise Exception("Error while getting user details")

    def _parse_collections(self, json_response: Dict):
        self.total_pages = json_response.get("total_pages")
        self.total = json_response.get("total")
        for collection in json_response.get("results", []):
            self.collections.append(
                Collection(
                    collection_id=collection.get("id"),
                    published_at=collection.get("published_at"),
                    share_key=collection.get("share_key"),
                    total_photos=collection.get("total_photos"),
                    title=collection.get("title"),
                    updated_at=collection.get("updated_at"),
                    links=LinksCollection(
                        html=collection.get("links", {}).get("html"),
                        photos=collection.get("links", {}).get("photos"),
                        related=collection.get("links", {}).get("related"),
                        self=collection.get("links", {}).get("self"),
                    ),
                    cover_photo=CoverPhoto(
                        alt_description=collection.get("cover_photo", {}).get(
                            "alt_description"
                        ),
                        blur_hash=collection.get("cover_photo", {}).get("blur_hash"),
                        description=collection.get("cover_photo", {}).get(
                            "description"
                        ),
                        likes=collection.get("cover_photo", {}).get("likes"),
                        links=LinksCoverPhoto(
                            html=collection.get("cover_photo", {})
                            .get("links", {})
                            .get("html"),
                            download=collection.get("cover_photo", {})
                            .get("links", {})
                            .get("download"),
                            download_location=collection.get("cover_photo", {})
                            .get("links", {})
                            .get("download_location"),
                        ),
                    ),
                )
            )
