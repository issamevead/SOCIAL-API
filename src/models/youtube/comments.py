"""
Base Class for Youtube Comments
"""

from __future__ import annotations
from typing import List, Optional, Dict
import json
from json.decoder import JSONDecodeError

import requests
from requests.exceptions import RequestException
from pydantic import BaseModel, Field

from src.utils.util import get_result_from_regex_pattern, json_extract


class Comment(BaseModel):
    """Schema Class for a Youtube video captions"""

    id: Optional[str]
    author_name: Optional[str]
    author_channel_id: Optional[str]
    like_count: Optional[str]
    published_time: Optional[str]
    text: Optional[str]
    number_of_replies: Optional[str]
    thumbnails: List[dict] = Field(default_factory=list)


class Comments(BaseModel):
    """Schema Class for a Youtube video comments"""

    video_id: str
    number_of_comments: Optional[int]
    continuation_token: Optional[str]
    comments: List[Comment] = Field(default_factory=list)

    def _get_video_comments_token(self):

        url = f"https://www.youtube.com/watch?v={self.video_id}"

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
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-ch-ua-full-version": '"96.0.4664.110"',
            "sec-ch-ua-arch": '"arm"',
            "sec-ch-ua-platform-version": '"12.0.1"',
            "sec-ch-ua-model": '""',
            "service-worker-navigation-preload": "true",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "YSC=-XOkHNQwM0A; VISITOR_INFO1_LIVE=KU4yNgSdHaU; PREF=f4=4000000&tz=Africa.Casablanca&f6=40000000; GPS=1; CONSISTENCY=AGDxDeMUFR4Ym2G5zwGfgw0lsjfrmRfm3ilHCC1mIjZMgdV7NYncF8bKbD59ZrmT0BUQD9PSqNecKkTRw87kHN-3HS7XHk22SDZN8-HEDnSpztYMEmjR-Hl9hS0oz9sBHB3ElGuXSQRaCvQ14NOr3sY",
        }

        response = requests.get(url, headers=headers, data=payload).text
        pattern = r'"/youtubei/v1/next"}},"continuationCommand":{"token":"(.*?)"'
        result = get_result_from_regex_pattern(response, pattern, 1)
        if result:
            return result
        return None

    def _comments_request(
        self, continuation_token: Optional[str] = None
    ) -> Optional[Dict]:
        if continuation_token is None:
            continuation_token = self._get_video_comments_token()
            if not continuation_token:
                return None

        url = "https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        payload = json.dumps(
            {
                "context": {
                    "client": {
                        "hl": "en",
                        "gl": "MA",
                        "remoteHost": "41.248.225.176",
                        "deviceMake": "Apple",
                        "deviceModel": "",
                        "visitorData": "CgtLVTR5TmdTZEhhVSiVyv2NBg%3D%3D",
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36,gzip(gfe)",
                        "clientName": "WEB",
                        "clientVersion": "2.20211216.01.02",
                        "osName": "Macintosh",
                        "osVersion": "10_15_7",
                        "originalUrl": f"https://www.youtube.com/watch?v={self.video_id}",
                        "screenPixelDensity": 2,
                        "platform": "DESKTOP",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "configInfo": {
                            "appInstallData": "CJXK_Y0GEL3rrQUQt8utBRDb660FEIDqrQUQu8f9EhCY6q0FEJHXrQUQ38j9EhDYvq0FEJH4_BI%3D"
                        },
                        "screenDensityFloat": 2,
                        "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                        "timeZone": "Africa/Casablanca",
                        "browserName": "Chrome",
                        "browserVersion": "96.0.4664.110",
                        "screenWidthPoints": 1189,
                        "screenHeightPoints": 764,
                        "utcOffsetMinutes": 60,
                        "connectionType": "CONN_CELLULAR_4G",
                        "memoryTotalKbytes": "8000000",
                        "mainAppWebInfo": {
                            "graftUrl": f"https://www.youtube.com/watch?v={self.video_id}",
                            "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
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
                                "encryptedTokenJarContents": "AGDxDeMUFR4Ym2G5zwGfgw0lsjfrmRfm3ilHCC1mIjZMgdV7NYncF8bKbD59ZrmT0BUQD9PSqNecKkTRw87kHN-3HS7XHk22SDZN8-HEDnSpztYMEmjR-Hl9hS0oz9sBHB3ElGuXSQRaCvQ14NOr3sY",
                                "expirationSeconds": "600",
                            }
                        ],
                    },
                    "clickTracking": {
                        "clickTrackingParams": "CJQBELsvGAIiEwii2Lyhq_D0AhWcH_EFHep_D4A="
                    },
                    "adSignalsInfo": {
                        "params": [
                            {"key": "dt", "value": "1639933206060"},
                            {"key": "flash", "value": "0"},
                            {"key": "frm", "value": "0"},
                            {"key": "u_tz", "value": "60"},
                            {"key": "u_his", "value": "2"},
                            {"key": "u_h", "value": "900"},
                            {"key": "u_w", "value": "1440"},
                            {"key": "u_ah", "value": "843"},
                            {"key": "u_aw", "value": "1440"},
                            {"key": "u_cd", "value": "30"},
                            {"key": "bc", "value": "31"},
                            {"key": "bih", "value": "764"},
                            {"key": "biw", "value": "1173"},
                            {
                                "key": "brdim",
                                "value": "0,25,0,25,1440,25,1440,843,1189,764",
                            },
                            {"key": "vis", "value": "1"},
                            {"key": "wgl", "value": "true"},
                            {"key": "ca_type", "value": "image"},
                        ]
                    },
                },
                "continuation": continuation_token,
            }
        )
        headers = {
            "authority": "www.youtube.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "content-type": "application/json",
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20211216.01.02",
            "x-goog-visitor-id": "CgtLVTR5TmdTZEhhVSiVyv2NBg%3D%3D",
            "sec-ch-ua-platform": '"macOS"',
            "accept": "*/*",
            "origin": "https://www.youtube.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "same-origin",
            "sec-fetch-dest": "empty",
            "referer": f"https://www.youtube.com/watch?v={self.video_id}",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "YSC=-XOkHNQwM0A; VISITOR_INFO1_LIVE=KU4yNgSdHaU; PREF=f4=4000000&tz=Africa.Casablanca&f6=40000000; GPS=1; CONSISTENCY=AGDxDeMUFR4Ym2G5zwGfgw0lsjfrmRfm3ilHCC1mIjZMgdV7NYncF8bKbD59ZrmT0BUQD9PSqNecKkTRw87kHN-3HS7XHk22SDZN8-HEDnSpztYMEmjR-Hl9hS0oz9sBHB3ElGuXSQRaCvQ14NOr3sY",
        }
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except (RequestException, JSONDecodeError):
            return None

    def _parse_comments(self, response: Dict) -> List[Optional[Comment]]:
        comments = json_extract(response, "commentRenderer")
        processed_comments = []
        for comment in comments:
            comment = Comment(
                id=comment.get("commentId"),
                author_name=comment.get("authorText", {}).get("simpleText"),
                author_channel_id=comment.get("authorEndpoint", {})
                .get("browseEndpoint", {})
                .get("browseId"),
                like_count=comment.get("voteCount", {}).get("simpleText"),
                published_time=comment.get("publishedTimeText", {})
                .get("runs", [{}])[0]
                .get("text"),
                text=comment.get("contentText", {}).get("runs", [{}])[0].get("text"),
                thumbnails=comment.get("authorThumbnail", {}).get("thumbnails", []),
                number_of_replies=comment.get("replyCount"),
            )
            processed_comments.append(comment)
        return processed_comments

    def get_comments(self, continuation_token: Optional[str]) -> Comments:
        response = self._comments_request(continuation_token)
        if response is None:
            return Comments(
                video_id=self.video_id,
                next_page_token=None,
                comments=[],
                total_results=0,
            )
        comments = self._parse_comments(response)
        cont = json_extract(response, "continuationCommand")
        cont = list(filter(lambda token: "_" not in token.get("token"), cont))
        try:
            cont = cont[len(cont) - 1]
            token = cont.get("token")
        except IndexError:
            token = None
        self.comments = comments
        self.number_of_comments = len(self.comments)
        self.continuation_token = token
        return self
