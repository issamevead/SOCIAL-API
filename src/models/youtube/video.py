"""
Base class for a Youtube Video
"""
from __future__ import annotations
from typing import List, Optional, Dict
import json
from xml.etree import ElementTree as ET

import requests
from pydantic import BaseModel, Field


class Subtitle(BaseModel):

    id: Optional[int]
    start: Optional[float]
    duration: Optional[float]
    text: Optional[str]


class VideoCaptions(BaseModel):
    """Schema Class for a Youtube video captions"""

    lang: Optional[str]
    is_available: bool = False
    subtitles: List[Subtitle] = Field(default_factory=list)


class VideoRecommendation(BaseModel):
    """Schema Class for a Youtube video captions"""

    status: dict = Field(default_factory={"status": "ok", "message": ""})
    number_of_videos: Optional[int]
    continuation_token: Optional[str]
    videos: List[Video] = Field(default_factory=list)


class Video(BaseModel):
    """Schema Class for a Youtube video"""

    video_id: str
    title: Optional[str]
    author: Optional[str]
    number_of_views: Optional[str]
    video_length: Optional[str]
    description: Optional[str]
    is_live_content: Optional[str]
    published_time: Optional[str]
    channel_id: Optional[str]
    category: Optional[str]
    type: str = "NORMAL"
    keywords: List[str] = Field(default_factory=list)
    thumbnails: List[dict] = Field(default_factory=list)
    data: List[dict] = Field(default_factory=list)
    subtitles: Optional[VideoCaptions] = Field(default_factory=VideoCaptions)

    def __repr__(self):
        return f"<Video {self.video_id}>"

    def _parse_video_data(self, response: Dict) -> List[Dict]:
        streaming_data = response.get("streamingData", {})
        data = streaming_data.get("formats", [])
        data.extend(streaming_data.get("adaptiveFormats", []))
        return data

    def _parse_video_subtitles(self, response: Dict) -> VideoCaptions:
        video_captions = VideoCaptions()
        captions = response.get("captions", None)
        if captions is None:
            return video_captions
        video_captions.lang = (
            captions.get("playerCaptionsTracklistRenderer", {})
            .get("captionTracks", [{}])[0]
            .get("languageCode")
        )

        base_url = (
            captions.get("playerCaptionsTracklistRenderer", {})
            .get("captionTracks", [{}])[0]
            .get("baseUrl")
        )
        if base_url is None:
            return video_captions
        try:
            caption_response = requests.get(base_url, timeout=20)
            tree = ET.ElementTree(ET.fromstring(caption_response.text))
            root = tree.getroot()
            texts = list(root.iter("text"))
            subtitles = []
            for i, text in enumerate(texts):
                subtitles.append(
                    Subtitle(
                        id=i + 1,
                        start=text.attrib["start"],
                        duration=text.attrib["dur"],
                        text=text.text,
                    )
                )
            video_captions.subtitles = subtitles
            video_captions.is_available = True
            return video_captions
        except requests.exceptions.RequestException:
            return video_captions

    def details(self, subtiles: bool = False) -> Video:
        """Returns a Video object with all details"""
        url = "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        payload = json.dumps(
            {
                "context": {
                    "client": {
                        "hl": "en",
                        "gl": "MA",
                        "remoteHost": "105.159.233.171",
                        "deviceMake": "Apple",
                        "deviceModel": "",
                        "visitorData": "Cgt2NVBmWkhMTjJmYyjn_42NBg%3D%3D",
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36,gzip(gfe)",
                        "clientName": "WEB",
                        "clientVersion": "2.20211124.00.00",
                        "osName": "Macintosh",
                        "osVersion": "10_15_7",
                        "originalUrl": f"https://www.youtube.com/watch?v={self.video_id}",
                        "platform": "DESKTOP",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "configInfo": {
                            "appInstallData": "COf_jY0GELfLrQUQk-qtBRCw1K0FENzerQUQtMX9EhCR-PwSENi-rQU%3D"
                        },
                        "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                        "timeZone": "Africa/Casablanca",
                        "browserName": "Chrome",
                        "browserVersion": "96.0.4664.55",
                        "screenWidthPoints": 672,
                        "screenHeightPoints": 764,
                        "screenPixelDensity": 2,
                        "screenDensityFloat": 2,
                        "utcOffsetMinutes": 60,
                        "memoryTotalKbytes": "8000000",
                        "clientScreen": "WATCH",
                        "mainAppWebInfo": {
                            "graftUrl": f"/watch?v={self.video_id}",
                            "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                            "isWebNativeShareAvailable": False,
                        },
                    },
                    "user": {"lockedSafetyMode": False},
                    "request": {
                        "useSsl": True,
                        "internalExperimentFlags": [],
                        "consistencyTokenJars": [
                            {
                                "encryptedTokenJarContents": "AGDxDePRmp73gyXBIH0BW4PJx7RTg7ha-Z7t3faKzDuKYsFTFCn0jtoP2RdcWkoxP2yAc5U2M2GxGy-bfhynPbKjMRO0pVf6PdIkVXIzTjESrcdkNX30Zvevl4Hclz-WOLRz6nK2F_fK9w_ObjE-sCs",
                                "expirationSeconds": "600",
                            }
                        ],
                    },
                    "clickTracking": {
                        "clickTrackingParams": "CMwBEKQwGAAiEwjEk7GOtLv0AhWDwUkHHeeXB8YyB3JlbGF0ZWRIouig2Mm59aR5mgEFCAEQ-B0="
                    },
                    "adSignalsInfo": {
                        "params": [
                            {"key": "dt", "value": "1638105063874"},
                            {"key": "flash", "value": "0"},
                            {"key": "frm", "value": "0"},
                            {"key": "u_tz", "value": "60"},
                            {"key": "u_his", "value": "7"},
                            {"key": "u_h", "value": "900"},
                            {"key": "u_w", "value": "1440"},
                            {"key": "u_ah", "value": "843"},
                            {"key": "u_aw", "value": "1440"},
                            {"key": "u_cd", "value": "30"},
                            {"key": "bc", "value": "31"},
                            {"key": "bih", "value": "764"},
                            {"key": "biw", "value": "656"},
                            {
                                "key": "brdim",
                                "value": "0,25,0,25,1440,25,1440,843,672,764",
                            },
                            {"key": "vis", "value": "1"},
                            {"key": "wgl", "value": "true"},
                            {"key": "ca_type", "value": "image"},
                        ]
                    },
                },
                "videoId": self.video_id,
                "playbackContext": {
                    "contentPlaybackContext": {
                        "currentUrl": f"/watch?v={self.video_id}",
                        "vis": 0,
                        "splay": False,
                        "autoCaptionsDefaultOn": False,
                        "autonavState": "STATE_NONE",
                        "html5Preference": "HTML5_PREF_WANTS",
                        "signatureTimestamp": 18954,
                        "referer": "https://www.youtube.com/watch?v=eUnVzJsINCI",
                        "lactMilliseconds": "-1",
                    }
                },
                "racyCheckOk": False,
                "contentCheckOk": False,
            }
        )
        headers = {
            "authority": "www.youtube.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
            "content-type": "application/json",
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20211124.00.00",
            "x-goog-visitor-id": "Cgt2NVBmWkhMTjJmYyjn_42NBg%3D%3D",
            "sec-ch-ua-platform": '"macOS"',
            "accept": "*/*",
            "origin": "https://www.youtube.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "same-origin",
            "sec-fetch-dest": "empty",
            "referer": f"https://www.youtube.com/watch?v={self.video_id}",
            "accept-language": "en-US,en;q=0.9",
            "cookie": f"YSC=En5WgxXyUcs; VISITOR_INFO1_LIVE=v5PfZHLN2fc; PREF=tz=Africa.Casablanca&f6=40000000; CONSISTENCY=AGDxDePRmp73gyXBIH0BW4PJx7RTg7ha-Z7t3faKzDuKYsFTFCn0jtoP2RdcWkoxP2yAc5U2M2GxGy-bfhynPbKjMRO0pVf6PdIkVXIzTjESrcdkNX30Zvevl4Hclz-WOLRz6nK2F_fK9w_ObjE-sCs; ST-1b8a0u9=itct=CMwBEKQwGAAiEwjEk7GOtLv0AhWDwUkHHeeXB8YyB3JlbGF0ZWRIouig2Mm59aR5mgEFCAEQ-B0%3D&csn=MC41MjEwMDEzMTcwMDUxNDUx&endpoint=%7B%22clickTrackingParams%22%3A%22CMwBEKQwGAAiEwjEk7GOtLv0AhWDwUkHHeeXB8YyB3JlbGF0ZWRIouig2Mm59aR5mgEFCAEQ-B0%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fwatch%3Fv%3D{self.video_id}%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_WATCH%22%2C%22rootVe%22%3A3832%7D%7D%2C%22watchEndpoint%22%3A%7B%22videoId%22%3A%22{self.video_id}%22%2C%22nofollow%22%3Atrue%2C%22watchEndpointSupportedOnesieConfig%22%3A%7B%22html5PlaybackOnesieConfig%22%3A%7B%22commonConfig%22%3A%7B%22url%22%3A%22https%3A%2F%2Fr4---sn-p5h-jhok.googlevideo.com%2Finitplayback%3Fsource%3Dyoutube%26orc%3D1%26oeis%3D1%26c%3DWEB%26oad%3D3200%26ovd%3D3200%26oaad%3D11000%26oavd%3D11000%26ocs%3D700%26oewis%3D1%26oputc%3D1%26ofpcc%3D1%26msp%3D1%26odeak%3D1%26odepv%3D1%26osfc%3D1%26ip%3D105.159.233.171%26id%3Df8eb60ec914cb95c%26initcwndbps%3D352500%26mt%3D1638114055%26oweuc%3D%22%7D%7D%7D%7D%7D",
        }

        try:
            response = requests.post(url, headers=headers, data=payload).json()
            video_details = response.get("videoDetails", None)
            if not video_details:
                return None
            self.video_id = video_details.get("videoId")
            self.title = video_details.get("title")
            self.author = video_details.get("author")
            self.number_of_views = video_details.get("viewCount")
            self.video_length = video_details.get("lengthSeconds")
            self.description = video_details.get("shortDescription")
            self.is_live_content = video_details.get("isLiveContent")
            self.published_time = (
                response.get("microformat", {})
                .get("playerMicroformatRenderer", {})
                .get("publishDate")
            )
            self.channel_id = video_details.get("channelId")
            self.category = (
                response.get("microformat", {})
                .get("playerMicroformatRenderer", {})
                .get("category")
            )
            self.thumbnails = video_details.get("thumbnail", {}).get("thumbnails", [])
            self.keywords = video_details.get("keywords")
            self.data = self._parse_video_data(response)
            if subtiles is True:
                self.subtitles = self._parse_video_subtitles(response)
            return self
        except Exception as error:
            raise ValueError(
                f"Unable to get data for Video ID = {self.video_id}"
            ) from error
