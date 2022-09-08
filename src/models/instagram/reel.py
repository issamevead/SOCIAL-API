from collections import namedtuple
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from requests import get

from src.utils.proxies import Proxies


class ReelTools(Enum):
    URL_USER_REELS = "https://i.instagram.com/api/v1/clips/user/"
    HEADERS_USER_REELS = {
        "authority": "i.instagram.com",
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "ig_did=05332B48-6560-42FF-814B-D1E3C10E53E4; datr=E3EQY2xcsH4tAXr6x7pIweWW; csrftoken=kJvJbsvxkhaMJr72InDchvsTfZ5pfXBG; mid=YxBxFAALAAFhtbJsksPqBHE_tA_H; ig_nrcb=1; csrftoken=kJvJbsvxkhaMJr72InDchvsTfZ5pfXBG",
        "origin": "https://www.instagram.com",
        "pragma": "no-cache",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "x-asbd-id": "198387",
        "x-csrftoken": "kJvJbsvxkhaMJr72InDchvsTfZ5pfXBG",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "0",
        "x-instagram-ajax": "1006130495",
    }
    URL_REEL = "https://i.instagram.com/api/v1/media/{}/info/"
    HEADERS_REEL = {
        "authority": "i.instagram.com",
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "cookie": 'ig_did=486CED1B-EE21-4E7A-8845-112B42D8D120; ig_nrcb=1; mid=YtFJXAALAAG6TsXJHER2-yLO2COS; datr=0eoNYxqy3eUsCAxLdyEueoRE; fbm_124024574287414=base_domain=.instagram.com; csrftoken=olEBO5hXlDYMxY90tX7g2RWH7nlxhaAu; ds_user_id=55061268732; sessionid=55061268732%3ATF1fMUDc6aKbdM%3A13%3AAYc1DCqQ32qicBhYzAY3gskiYAPycANUevMnnRT8Yw; fbsr_124024574287414=GM5m0wuLdRxD_iyVyYopIipC5Sy6ZJadJ-zGNpgCVTw.eyJ1c2VyX2lkIjoiMTAwMDg1MjM2MjUxNTMzIiwiY29kZSI6IkFRQ05lenYxSUpXZHBtVng1NmdvNExlbHV4REpKZllhREs0X294UjVIZ2lBaU9ReGNnbkRQMGhjMWE1Sm56SXIzSjB2NEVUbFNrWTNfUzBKaVIzSWNsRDhqcHFjODdMUmFHR21VbXhXRUZyX29meGlfMTNTaGliZ2RvalFlendLamF5cFM0S0twV1dLYVktZVVTb0NaNDVUZTJrVGFHX1prU1dNZ1B5U0dvUGp5bWtEdGRTTG4wZnR5bW9xWC05UUFyUlNfMG45eW1CSUV5aTU5M0x2QUJNdXY1WFNFaXdXamdSeXZDdF80Rjg2Yk9rWXRSN2VYZnBMRFBlbXlqTVRYNzU1NnNHaVVRbzNFNUZiYm9laHJDd0RxWUVnamVCdTU3UjVJWUFlSDF1X20zSThWbEhaVmtpZlQxSlpRWW9RaHlxMHZyUGJBM1V6bWFfRVVzUThpYmlPIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQVBibTVOSVgxODNoQXdDeDlKTUNYMzhXWkFZaWs0WkEzT3lxYlE3VlpDSXExVGwxUExQcExHME5IbTFxWkJnV25weDFjME53Z25zMW82SlFVWkJ6WDBkNVEwWkNHRUFSYlJHd1A2dGhFN2pHdlB6YnlqVjZSbzNaQlpBbUt1dUpSZlM2QjR3dDVqM1BwQWdlZHloWkJrODFkRE1BS1BJUjVBNUFvOG5zTHNySFNkVkdiZG1aQjM2NlFaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjYyMDM1NDU2fQ; rur="RVA\\05455061268732\\0541693571461:01f7f5279bd83455991152e643cbd65c5822a706cfa2d372b28ac90bdcabc5171d3f5ef9"; csrftoken=kJvJbsvxkhaMJr72InDchvsTfZ5pfXBG; ds_user_id=55061268732; rur="RVA\\05455061268732\\0541693571874:01f7e2c99bbb8cb926d41933766210c1db57194b66a50418a22a2fad574056681b412a4e"',
        "origin": "https://www.instagram.com",
        "pragma": "no-cache",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "x-asbd-id": "198387",
        "x-csrftoken": "olEBO5hXlDYMxY90tX7g2RWH7nlxhaAu",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR0FWSbFoV-BL0TCBMTYiAC9sbaPL1wXkRuMJGxmAoICHLG7",
        "x-instagram-ajax": "1006132402",
    }


class ReelPostRequest(BaseModel):
    username: str = Field(min_length=1)
    page_size: int = Field(default=20)


class ReelPostRequestContinuation(ReelPostRequest):
    user_id: int = Field(gt=0)
    continuator_token: Optional[str]


Dimension = namedtuple(
    "Dimension", ["original_width", "original_height"], defaults=(0, 0)
)


ReelVersion = namedtuple(
    "ReelVersion",
    ["height", "id", "type", "url", "width"],
    defaults=(None, None, None, None, None),
)


class Reel(BaseModel):
    reel_pk: str
    reel_shortcode: Optional[str]
    reel_id: Optional[str]
    reel_caption: Optional[str]
    number_of_comments: Optional[int]
    number_of_likes: Optional[int]
    reel_view_count: Optional[int]
    reel_play_count: Optional[int]
    has_audio: Optional[bool]
    has_shared_to_fb: Optional[int]
    reel_duration: Optional[float]
    can_viewer_save: Optional[bool]
    can_viewer_reshare: Optional[bool]
    reel_dimensions: Dimension = Field(default_factory=Dimension)
    reel_versions: List[ReelVersion] = Field(default_factory=list)

    def get_reel_details(self):
        proxies = Proxies.rand_proxy(secure=True)
        for _ in range(3):
            try:
                proxy = next(proxies)
                response = get(
                    ReelTools.URL_REEL.value.format(self.reel_pk),
                    headers=ReelTools.HEADERS_REEL.value,
                    proxies=proxy.to_dict(),
                )
                return self._reel_parser(response.json())
            except StopIteration:
                raise Exception("No proxy left")
            except Exception:
                continue
        raise Exception(f"Reel data for {self.reel_pk} not found")

    def _reel_parser(self, response: dict):
        from src.models.instagram.user import UserRestrictedInfos

        data = response.get("items", [])
        if not data:
            raise Exception(f"Reel data for {self.reel_pk} not found")
        if len(data) > 0:
            data = data[0]
        self.reel_shortcode = data.get("code")
        self.reel_id = data.get("id")
        self.reel_caption = data.get("caption", {}).get("text")
        self.number_of_comments = data.get("comment_count")
        self.number_of_likes = data.get("like_count")
        self.reel_view_count = data.get("view_count")
        self.reel_play_count = data.get("play_count")
        self.reel_dimensions = Dimension(
            data.get("original_width"),
            data.get("original_height"),
        )
        self.has_audio = data.get("has_audio")
        self.has_shared_to_fb = data.get("has_shared_to_fb")
        self.can_viewer_save = data.get("can_viewer_save")
        self.can_viewer_reshare = data.get("can_viewer_reshare")
        self.reel_duration = data.get("video_duration")
        self.reel_versions = [
            ReelVersion(**version) for version in data.get("video_versions", [])
        ]
        user_data = data.get("user", {})
        user = UserRestrictedInfos(
            username=user_data.get("username"),
            user_id=user_data.get("pk"),
            user_full_name=user_data.get("full_name"),
            is_private=user_data.get("is_private"),
            is_verified=user_data.get("is_verified"),
            profile_pic_url=user_data.get("profile_pic_url"),
        )

        return user, self