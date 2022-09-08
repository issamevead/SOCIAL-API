"""
Base Class for Youtube Channel
"""
from __future__ import annotations
from contextlib import suppress
from typing import List, Optional, Dict, Tuple
import json
from json.decoder import JSONDecodeError
from urllib.parse import parse_qs, unquote, urlparse

import requests
from requests.exceptions import RequestException
from pydantic import BaseModel, Field

from src.models.youtube.video import Video
from src.utils.util import get_result_from_regex_pattern, json_extract


class ChannelVideos(BaseModel):
    """Channel Videos"""

    continuation_token: Optional[str]
    videos: List[Video] = Field(default_factory=list)


class Channel(BaseModel):
    channel_id: str
    title: Optional[str]
    description: Optional[str]
    subscriber_count: Optional[str]
    links: List[Optional[Dict]] = Field(default_factory=list)
    avatar: List[Dict] = Field(default_factory=list)
    banner: List[Dict] = Field(default_factory=list)
    verified: bool = False

    def _channel_details_request(self) -> Optional[Dict]:
        url = f"https://www.youtube.com/channel/{self.channel_id}/about"

        payload = {}
        headers = {
            "authority": "www.youtube.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-ch-ua-full-version": '"96.0.4664.55"',
            "sec-ch-ua-arch": '"arm"',
            "sec-ch-ua-platform-version": '"12.0.1"',
            "sec-ch-ua-model": '""',
            "service-worker-navigation-preload": "true",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "GPS=1; YSC=NfiHlXrpQcA; CONSENT=PENDING+861; VISITOR_INFO1_LIVE=ry8y6Sfm1QU; PREF=tz=America/Los_Angeles&f6=40000000",
        }

        with suppress(Exception):
            response = requests.get(url, headers=headers, data=payload).text
            pattern = r"ytInitialData = (.*?});"
            result = get_result_from_regex_pattern(response, pattern, 1)
            if result:
                return json.loads(result)
        return None

    def _parse_channel_details(self, response: Dict) -> Channel:
        header = response.get("header", {}).get("c4TabbedHeaderRenderer", {})
        metadata = response.get("metadata", {})
        links = header.get("headerLinks", {}).get("channelHeaderLinksRenderer", {})
        unprocesses_links = links.get("primaryLinks", [])
        unprocesses_links.extend(links.get("secondaryLinks", []))
        processed_links = []
        for link in unprocesses_links:
            endpoint = (
                link.get("navigationEndpoint", {}).get("urlEndpoint", {}).get("url", "")
            )
            with suppress(KeyError):
                endpoint = unquote(parse_qs(urlparse(endpoint).query)["q"][0])
            processed_links.append(
                {
                    "name": link.get("title", {}).get("simpleText"),
                    "endpoint": endpoint,
                }
            )

        self.title = header.get("title")
        self.description = metadata.get("channelMetadataRenderer", {}).get(
            "description"
        )
        self.subscriber_count = header.get("subscriberCountText", {}).get("simpleText")
        self.links = processed_links
        self.avatar = header.get("avatar", {}).get("thumbnails")
        self.banner = header.get("banner", {}).get("thumbnails")
        self.verified = bool(header.get("badges", None))

    def _channel_videos_request(self) -> Optional[Dict]:
        url = f"https://www.youtube.com/channel/{self.channel_id}/videos"

        payload = {}
        headers = {
            "authority": "www.youtube.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-ch-ua-full-version": '"96.0.4664.55"',
            "sec-ch-ua-arch": '"arm"',
            "sec-ch-ua-platform-version": '"12.0.1"',
            "sec-ch-ua-model": '""',
            "service-worker-navigation-preload": "true",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "YSC=En5WgxXyUcs; VISITOR_INFO1_LIVE=v5PfZHLN2fc; CONSENT=PENDING+861; PREF=tz=Africa.Casablanca&f6=40000000; GPS=1; SIDCC=AJi4QfHzN_Cvt899e2SEkjchcrfuHHJEv_F-ASkLFSxH8HAS0H3qEMUFp3A60_CIYbQrXsawnp9k; __Secure-3PSIDCC=AJi4QfEVDCWdF1F3J5FqN9nmghY_6K2lPSDur5O_IP9b0BpfYBmlyqihd0TRpRhE3CChK0bq8oM",
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            pattern = r"ytInitialData = (.*?)};"
            result = get_result_from_regex_pattern(response.text, pattern, 1) + "}"
            if result:
                return json.loads(result)
            return None
        except (RequestException, JSONDecodeError):
            return None

    def _parse_channel_videos(
        self, response: Dict
    ) -> Tuple[List[Optional[Video]], Optional[str]]:
        videos = []
        token = None
        with suppress(Exception):
            items = json_extract(response, "gridRenderer")
            if len(items) == 0:
                items = json_extract(response, "continuationItems")
                if len(items) == 0:
                    return [], None
                items = [{"items": items[0]}]
            items = items[0].get("items")
            for item in items:
                if item.get("continuationItemRenderer", None):
                    token = json_extract(item, "token")
                    token = token[0] if token else None
                    continue
                video = item.get("gridVideoRenderer", {})
                videos.append(
                    Video(
                        channel_id=self.channel_id,
                        video_id=video.get("videoId"),
                        title=video.get("title").get("runs")[0].get("text"),
                        published_time=video.get("publishedTimeText", {}).get(
                            "simpleText"
                        ),
                        number_of_views=video.get("viewCountText", {}).get(
                            "simpleText"
                        ),
                        thumbnails=video.get("thumbnail").get("thumbnails"),
                        video_length=video.get("thumbnailOverlays")[0]
                        .get("thumbnailOverlayTimeStatusRenderer", {})
                        .get("text", {})
                        .get("simpleText"),
                        description=None,
                    )
                )
        return videos, token

    def details(self) -> Channel:
        response = self._channel_details_request()
        if response is not None:
            self._parse_channel_details(response)
        return self

    def videos(self) -> ChannelVideos:
        response = self._channel_videos_request()
        videos, token = self._parse_channel_videos(response)
        return ChannelVideos(videos=videos, continuation_token=token)
