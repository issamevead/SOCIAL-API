from typing import List
from requests import get
from pydantic import BaseModel, Field

from src.utils.util import json_extract
from src.utils.proxies import Proxies


class HighlightUserRestrictedInfos(BaseModel):
    highlight_id: int
    highlight_title: str
    thumbnail_src: str
    thumbnail_cropped: str


class Highlight(BaseModel):
    user_id: int
    username: str
    highlights: List[HighlightUserRestrictedInfos] = Field(default_factory=list)

    def get_user_highlights(self):
        url = f"https://www.instagram.com/graphql/query/?query_hash=d4d88dc1500312af6f937f7b804c68c3&variables=%7B%22user_id%22%3A%22{self.user_id}%22%2C%22include_chaining%22%3Afalse%2C%22include_reel%22%3Afalse%2C%22include_suggested_users%22%3Afalse%2C%22include_logged_out_extras%22%3Atrue%2C%22include_highlight_reels%22%3Atrue%2C%22include_live_status%22%3Afalse%7D"
        headers = {
            "authority": "www.instagram.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr-MA;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6",
            "cookie": 'ig_did=7CA59EA5-2BA8-4AEF-9C13-1ED84CC66E20; ig_nrcb=1; datr=M6sMY0NwQwQrzu_V9BoRNdBc; csrftoken=CzTN5Z3PRZKb0e5sXVlXX73DPQBWWaM9; mid=YwyrNQALAAEyXmlb4LlW6UJsFwQs; csrftoken=kJvJbsvxkhaMJr72InDchvsTfZ5pfXBG; ds_user_id=55061268732; ig_did=359DA3CB-5408-4546-8CEE-42A6AB7431B1; mid=YxDVYgALAAGhXLWSRfHv8pQ1H2MI; rur="NAO\\05455061268732\\0541693585788:01f71a436207a35a7def42d75d7fabba312088684bdd8a279973b5fec68382361fd87398"',
            "referer": f"https://www.instagram.com/{self.username}/reels/",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "viewport-width": "747",
            "x-asbd-id": "198387",
            "x-csrftoken": "CzTN5Z3PRZKb0e5sXVlXX73DPQBWWaM9",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "1006139826",
            "x-requested-with": "XMLHttpRequest",
        }
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            try:
                proxy = next(proxies)
                response = get(url, headers=headers, proxies=proxy.to_dict())
                if response.status_code == 200:
                    self._highlight_parser(response.json())
                    return self
                raise ValueError(f"Highlight for username = {self.username} not found")
            except StopIteration:
                raise ValueError(f"No proxy left")
            except Exception:
                continue
        raise ValueError(f"Highlight for username = {self.username} not found")

    def _highlight_parser(self, data: dict):
        nodes = json_extract(data, "node")
        for highlight in nodes:
            self.user_id = highlight.get("owner", {}).get("id", 0)
            self.username = highlight.get("owner", {}).get("username", "")

            self.highlights.append(
                HighlightUserRestrictedInfos(
                    highlight_id=highlight.get("id", 0),
                    highlight_title=highlight.get("title", ""),
                    thumbnail_src=highlight.get("cover_media", {}).get(
                        "thumbnail_src", ""
                    ),
                    thumbnail_cropped=highlight.get(
                        "cover_media_cropped_thumbnail", {}
                    ).get("url", ""),
                )
            )
