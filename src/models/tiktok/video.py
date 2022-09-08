"""
Tiktok Video Class and Methods
"""
from dataclasses import dataclass
import json
from bs4 import BeautifulSoup

import requests

from src.utils.proxies import Proxies


@dataclass
class VideoModel:
    """Tiktok Video Model"""

    video_id: str = None
    description: str = None
    create_time: str = None
    author: str = None
    statistics: dict = None
    cover: dict = None
    download_url: str = None
    video_definition: str = None
    format: str = None
    bitrate: str = None
    duration: int = None


@dataclass
class VideoDetails:
    """Schema Class for a Youtube video"""

    video_id: str = None
    details: VideoModel = None


class Video:
    """Schema Class for a Tiktok video"""

    @staticmethod
    def get_video_details(video_id):
        """Return User Id"""
        url = f"https://api2.musical.ly/aweme/v1/aweme/detail/?aweme_id={video_id}"
        headers = {
            "User-Agent": "okhttp/3.12.0",
            "Host": "api2.musical.ly",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        proxies = Proxies.rand_proxy()
        for _ in range(2):
            proxy = next(proxies)
            try:
                response = requests.get(url, headers=headers, proxies=proxy.to_dict())
                r = response.json()
                video = VideoModel(
                    video_id=video_id,
                    description=r["aweme_detail"]["desc"],
                    create_time=r["aweme_detail"]["create_time"],
                    author=r["aweme_detail"]["author"]["nickname"],
                    statistics={
                        "number_of_comments": r["aweme_detail"]["statistics"]["comment_count"],
                        "number_of_hearts": r["aweme_detail"]["statistics"]["digg_count"],
                        "number_of_plays": r["aweme_detail"]["statistics"]["play_count"],
                        "number_of_reposts": r["aweme_detail"]["statistics"]["share_count"],
                    },
                    cover=r["aweme_detail"]["video"]["cover"]["url_list"][0],
                    download_url=r["aweme_detail"]["video"]["download_addr"]["url_list"][0],
                    video_definition=r["aweme_detail"]["video"]["ratio"],
                    duration=int(r["aweme_detail"]["video"]["duration"] / 1000),
                )
                return VideoDetails(video_id, video)
            except Exception:
                proxies = Proxies.rand_proxy(secure=True)
                continue
        raise ValueError(f"Video with id={video_id} not found")

    @staticmethod
    def get_video_details_alt(video_id):
        url = f"https://m.tiktok.com/v/{video_id}.html"

        payload = {}
        headers = {
            "authority": "m.tiktok.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
        }
        proxies = Proxies.rand_proxy()
        for _ in range(2):
            proxy = next(proxies)
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    data=payload,
                    proxies=proxy.to_dict(),
                    timeout=20,
                )
                soup = BeautifulSoup(response.text, "html.parser")
                metadata = soup.find("script", {"id": "sigi-persisted-data"})
                data = "{" + metadata.string.split("]={")[1].split("};")[0] + "}"
                data = json.loads(data)
                list_videos = data["ItemModule"]
                list_videos = [
                    list_videos.get(video) for video in list_videos if video == video_id
                ]
                video = list_videos[0]
                video = Video(
                    video_id=video["id"],
                    description=video["desc"],
                    author=video["author"],
                    create_time=video["createTime"],
                    statistics={
                        "number_of_comments": video["stats"]["commentCount"],
                        "number_of_hearts": video["stats"]["diggCount"],
                        "number_of_plays": video["stats"]["playCount"],
                        "number_of_reposts": video["stats"]["shareCount"],
                    },
                    video_definition=video["video"]["definition"],
                    cover=video["video"]["cover"],
                    download_url=video["video"]["downloadAddr"],
                    bitrate=video["video"]["bitrate"],
                    duration=video["video"]["duration"],
                )
                return VideoDetails(video_id, video)
            except Exception:
                proxies = Proxies.rand_proxy(secure=True)
                continue
        raise ValueError(f"Video with id={video_id} not found")
