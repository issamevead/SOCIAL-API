"""Tiktok Video Search"""
import time
import asyncio
from typing import List
from dataclasses import dataclass
import urllib

import requests
from src.models.tiktok.user import UserDetails

from src.utils.util import parse_cookies_to_str
from src.utils.proxies import Proxies
from src.models.tiktok.video import VideoModel



@dataclass
class SearchResultVideo:
    """Schema Class for a Tiktok Search Result Video"""

    query: str = None
    videos: List[VideoModel] = None


@dataclass
class SearchResultUser:
    """Schema Class for a Tiktok Search Result Video"""

    query: str = None
    users: List[UserDetails] = None


def get_timestamp():
    """Return Timestamp"""
    return int(round(time.time() * 1000))


def url_quote(query):
    """Return URL quote String"""
    return urllib.parse.quote(query)


class Search:
    """Schema Class for a Tiktok Search"""

    @staticmethod
    def search_general(query: str) -> dict:
        """Search for videos, users and channels"""
        query = url_quote(query)
        url = f"https://m.tiktok.com/api/search/general/full/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=0.8&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.84%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7082044281019909637&device_platform=web_pc&focus_state=true&from_page=search&history_len=16&is_fullscreen=false&is_page_visible=true&keyword={query}&offset=0&os=mac&priority_region=&referer=&region=MA&screen_height=1050&screen_width=1680&tz_name=Africa%2FCasablanca&verifyFp=verify_l1seyuuj_eaK6alvu_jIDu_4T9A_8Ao9_xlmLW1EynINT&webcast_language=en&msToken=sAeGUC2CDPH2aP0LUHBdQjLJ8r4Y71oy4ukjQDc-eSDXXDdoSvbdZafQRIxsKmOr9Q8CmK0FaSqEzQ77r0i5uJhMeZPksd9IMI4s5Sq_0d2LqCBDcmBLK2GVsrwxrh09CWCNjNQwHpD1dEIkBA==&X-Bogus=DFSzswV7N/sANJOMSAgPTV/F6qxi&_signature=_02B4Z6wo00001QRoB-gAAIDAfKbs7uoxByUEaANAACNSac"
        session = requests.Session()
        response = session.get(
            f"https://www.tiktok.com/search?q={query}&t={get_timestamp()}"
        )
        cookies = session.cookies.get_dict()
        payload = {}
        headers = {
            "authority": "m.tiktok.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "sec-ch-ua-platform": '"macOS"',
            "accept": "*/*",
            "origin": "https://www.tiktok.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.tiktok.com/",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "cookie": parse_cookies_to_str(cookies),
        }
        proxies = Proxies.rand_proxy()
        for _ in range(3):
            proxy = next(proxies)
            try:
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    data=payload,
                    timeout=20,
                    proxies=proxy.to_dict(),
                )
                data = response.json()["data"]
                list_videos = [video.get("item") for video in data if video.get("item")]
                videos = []
                for video in list_videos:
                    video = VideoModel(
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
                        video_definition=video["video"]["ratio"],
                        cover=video["video"]["cover"],
                        download_url=video["video"]["downloadAddr"],
                        bitrate=video["video"]["bitrate"],
                        duration=video["video"]["duration"],
                    )
                    videos.append(video)
                return SearchResultVideo(query=query, videos=videos)
            except Exception:
                proxies = Proxies.rand_proxy(secure=True)
                continue
        raise ValueError(f"Video Search for query {query} not found")

    @staticmethod
    def search_accounts(query: str) -> dict:
        """Search for videos, users and channels"""
        query = url_quote(query)
        url = f"https://www.tiktok.com/api/search/user/full/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=0.8&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.84%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&cursor=0&device_id=7082044281019909637&device_platform=web_pc&focus_state=true&from_page=search&history_len=3&is_fullscreen=false&is_page_visible=true&keyword={query}&os=mac&priority_region=&referer=&region=MA&screen_height=1050&screen_width=1680&tz_name=Africa%2FCasablanca&verifyFp=verify_l1seyuuj_eaK6alvu_jIDu_4T9A_8Ao9_xlmLW1EynINT&webcast_language=en&msToken=X9GJmCT3uO0zefU5AftAQK3HVOArTA8Qcn8Ac4_sFl5RRBBemf2EKBC3dHW3N51jU8ZfsceCcwibocqz9LHFrUJOVWze_U9oqPAPOCsM7U703b1BE8l8eIO8aLSnlhF70g1PFNCMKsJCXKKLFg==&X-Bogus=DFSzswVOl7vANxSnSAgjQV/F6qyn&_signature=_02B4Z6wo00001o6hVPQAAIDD9m-.8q220w6OoVBAAMIJ8a"
        session = requests.Session()
        response = session.get(
            f"https://www.tiktok.com/search?q={query}&t={get_timestamp()}"
        )
        cookies = session.cookies.get_dict()
        payload = {}
        headers = {
            "authority": "m.tiktok.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "sec-ch-ua-platform": '"macOS"',
            "accept": "*/*",
            "origin": "https://www.tiktok.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.tiktok.com/",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "cookie": parse_cookies_to_str(cookies),
        }

        proxies = Proxies.rand_proxy()
        for _ in range(3):
            proxy = next(proxies)
            proxy = {
                "http": f"{proxy.protocol}://{proxy.ip}:{proxy.port}",
                "https": f"{proxy.protocol}://{proxy.ip}:{proxy.port}",
            }
            try:
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    data=payload,
                    timeout=20,
                    proxies=proxy,
                )
                data = response.json()
                data = response.json()["user_list"]
                list_users = [
                    video.get("user_info") for video in data if video.get("user_info")
                ]
                users = []
                for user in list_users:
                    user = UserDetails(
                        user_id=user["uid"],
                        username=user["unique_id"],
                        followers=user["follower_count"],
                        following=None,
                        verified=bool(user["custom_verify"]),
                        profile_image=user["avatar_thumb"]["url_list"][0],
                    )
                    users.append(user)
                return SearchResultUser(query=query, users=users)
            except Exception:
                continue
        raise ValueError(f"Video Search for query {query} not found")

    @staticmethod
    def search_videos(query: str) -> dict:
        """Search for videos, users and channels"""
        query = url_quote(query)
        url = f"https://m.tiktok.com/api/search/general/full/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=0.8&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.84%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7082044281019909637&device_platform=web_pc&focus_state=true&from_page=search&history_len=16&is_fullscreen=false&is_page_visible=true&keyword={query}&offset=0&os=mac&priority_region=&referer=&region=MA&screen_height=1050&screen_width=1680&tz_name=Africa%2FCasablanca&verifyFp=verify_l1seyuuj_eaK6alvu_jIDu_4T9A_8Ao9_xlmLW1EynINT&webcast_language=en&msToken=sAeGUC2CDPH2aP0LUHBdQjLJ8r4Y71oy4ukjQDc-eSDXXDdoSvbdZafQRIxsKmOr9Q8CmK0FaSqEzQ77r0i5uJhMeZPksd9IMI4s5Sq_0d2LqCBDcmBLK2GVsrwxrh09CWCNjNQwHpD1dEIkBA==&X-Bogus=DFSzswV7N/sANJOMSAgPTV/F6qxi&_signature=_02B4Z6wo00001QRoB-gAAIDAfKbs7uoxByUEaANAACNSac"

        payload = {}
        headers = {
            "authority": "m.tiktok.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "sec-ch-ua-platform": '"macOS"',
            "accept": "*/*",
            "origin": "https://www.tiktok.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.tiktok.com/",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "cookie": "tt_csrf_token=c5weakEh-z51l2VopGm_xGqt6ddBhjT0foAg; _abck=CC8D62AD3D9AAA59550D9884BE2E6D5E~-1~YAAQvrR7XL7ezhiAAQAAzTlrHwcIQ75GWjsim8EhWOvQ4v6qnqRZV6e9sQAuAnqM06lJO8na8DSSDFkS8r1oUT9NHfriXuEvgyXDIF6V4I76jqLZVIJxF8a5wdk2utaMGl37fno5rLLCIZyk1881bmRCDgcdnTjtL23VxpMFSWDS1AkCSP6wPEh4zpl4do2hjpTOag5hFKpdMJrhh+ErJqnWp1A/iAcXV20g6G4Yzta4Ec1xHoekxLM+C5UeOrk9fHEqIUXAJAZ78m6d9wtgfg4y2wbQlauV3iVGwmf4BBtqWFtQiAYxcqqAHqrsoCknE7f6uat19E6RtHloODUKPEAJheBbIQLgKDaCJSxFShL2znIqaBDBlqM2LKvAdfi91bRBBDku2p10ug==~-1~-1~-1; bm_sz=4B5DF1AEDBB977CEC52C7194FBB5AF5E~YAAQvrR7XMDezhiAAQAAzTlrHw8rjQ4BnVSmKR/gH/uHv+AnWVh1IhukshFlWlfZUA3OIgk0OJ4355kC3OkqFKETR3wHuiDlJK1wfdLl84uBZFEwM7O5G0ThIJDm9YradWJ4/1AUn0G/3rKwZdDMO3iXyRUe1QDVCWqYghnpYQIxs5JHdCh2nHByv4wof4Eqwvix6sDNxxKRUK8WmA9o+johxUFN/4NaJOCaWBekNFWQMXc5qa8CLFfjYY/1jEcXAq9T6I72WN3MHEkHXmCaLT5kMC6uCkYByeePLBUzd68hEPk=~4405044~3551544; csrfToken=xl3vJziXLmvrC7oD7Wn8MszA; bm_mi=4DD94A5749FB43554F650208A2DC9760~EhsxRfO2RFHYNqLI4MPJfVOFbhziJ0PcqvnXnUq3UUMRNoyRtOJpim3PF+QLiczkgrBYS5faoPajyfL4JfI26oiirLby+m/vZyIZHGFCTH8yyREnrDq4z/ur3fkZ+IddZvB3qa8CyfnwsHdqSwP5rUbFYnRQTaCJKD+rMZShzll/t4mkqNc/u0TIGqyyOTSTgtrKZUZLFd4w4lQKEXexa8aYahIyGuM2f98WTGDU3Mg=; bm_sv=FD622C5D7AFA3376D59679B1FE84CA3D~USxUXyCzc0S7xe3S3+Kz5M0L5UserZoRWrEIAlONLjvMWOi1qM8xUEP5Apbs0PteZmphnXZDO/bRbCfM5B+1aBEcdW1TxMu7UIw7ZRQOGtkDAMsKtdd01Gk7iT8tZwOcUF4Llgr3gtkeeypvJdgxGaER+syUWqDV09CtV9fr5H0=; ttwid=1%7C6eaPXeOGttJsSB5moV4GbOrZ8TMvrjUqnkuPBjhZA3s%7C1649799026%7C58dd3f216e5e2da2fde90aa7906f96eaa1f61035cca8fccdc05f744a471d0ea7; ak_bmsc=FBFF1ED4A816054A0D483641F1989762~000000000000000000000000000000~YAAQTgwXAmSGFgOAAQAAaHKwHw+KkWZKfePwNPDUgS3HY5OQxPC6FO9Ns7VTyuOzvrBA1KxsiChPqI64nZ7X8kaL2ASHdCzkCN5yxZkUNgA1/JsNElgP1bGgmbeeDB/+sAM0rUR2wk11l5ksaLBr4v0oc/3wM8y0atH2HmqLw61/a8GPMCYWZMTAgB+5lqO7JT7NCSnCIPRKDD1LTEE+JblB5QZazuKIGAg8eowTyeCAFiVW9DDiJRP96/b93OolG+rgxzmfh1YNJ1a+CwN3hsrOqvT8EWS/hIAqzTwaBOxkk50lI/1PFNiwM26AWyxCA8GwZvjJTp860DNbMT6rMfJ9aYppgbMxND5EhRRvd3h6Bj0F1N1NAcOFQb5uuOJNB3tYeSvVtvo+qtCfPA5Vi1Ogz5aZCWnZatlUvOu4O4Wour9nMQ==; msToken=l6L8yzjALeYwflvPBtXQ3qvHA8QRQh6JA2SFSFwSAqUQsUmYa8s8Pd1s13JZpMykWbSpAs4lKThAXaYP92fPePRI7Ji1_URfS2sjSO1cZXTwaVOr0u0C6zgGckNQ6UjrBbo4F-8SmR2qEPa1Cg==; _abck=193EAE615AB03C4876D93CDAD4E94C6E~-1~YAAQv7R7XJGQxB2AAQAAYZyDHwdfqzHp+UlBiYj7EEruodW1Wrhi7q1a2B5E+xP5LL/v0DNRpIqS8VuICLyPuQeib6KOHm+Dhu7H9XZZ9pAh3XmbtOiVd3O5CrBj/kzOiPCCNv2cEo9FlTESxT9izCaY6j2DXyHItJ1YgjNN6empDJ3hXBBjb87yEwQ5+1nqclIyc+CgT/wMSTouXAEQDPRkIv/edpnN9KLAGNUyULtPamblZWDKnf7TU4IP1z+ec7omOewYawZCA/x1dHmrOwr/28zVB+3G8xo0YEKCKvIU006TuBFRktggpwQqOdzlrD03R5E0f8SHsfO3eQuYloU7oKUtc0nuay9ig20HGPgTC46bwItIHjdu5OIDYJG3CwDOddbFE2WeCw==~-1~-1~-1; ak_bmsc=051B018DE8129114B4FEC0877ABA186C~000000000000000000000000000000~YAAQv7R7XJKQxB2AAQAAYZyDHw/EbYZjS+mvF3W5j0ptYVCnfQVWnMcQqGLSv9jTmAr0E0p4fqwEPi6m31DvQHj0Iwwal6IkF3qajEvnxGKRHy5IiNc+9JRZ/1v2A0OmJjo9TstM6hlVrOHixDBz4X0y503ko8y+n8kMcW6MF0Tis3X/iNL0dJhpX0HESwGWa/WtmIrPAE1qCs506/5BSfigPHaPupg0J4+TONshyunZJCeqTq6riKDdMW6y28cJ6w7449nG+08GZ6hwZK4NYS6taYEd1TE2OJr8yWrERWsdrHCaJtZRI3n3nZj6ENwNzlnn5NlyNLnPKPD1V6k0QD3pBPFo7IovoBuJAYbjAOiSjyianEFgabID91KK; bm_sz=B9A7E4B48931E490E8B3E3C83002BC87~YAAQv7R7XJOQxB2AAQAAYpyDHw/nsCfl3XVDOC9ssx4HCKGhKjLIXv4PespmOPdM+/U5NGKfzc0BN4I02ZZbjF9INe/vYt1kYcnAAgWmxMkTU3hlHScBq5NZqG6hEVcML3Z+/Gd84epfTBOVFEP024uIORCO/UL34jFthrPajYtY63ecZmH6nxEvYK2cZcl3d7hGT4B2eTrWk16QiSA4wmFN686J3B2WNV1vY21Sap0iPv7KnBHGNHpAeTraUqQalLyBhKP82hwMCP7Eadbk9KWfiJDwiMETTI7FPjSB2tHzlBo=~4604228~4474416; msToken=Hbemm0POD0yFpnLHR9S-AyxYn_lXON0DbHdFtbYMLxs2SBmPA7rXsJbf7F7GJEBhz_dM0IbkglnRgAOsHDBEm8W6ynVkTx5TOWi4eLXT64AaJf9bmQ7OhJc68mUMqben2a6Fej2AyZHbNz1Z; tt_csrf_token=cdAs8IH2-EXlV2v0k6DnbCRnTZy9nQWwY2q8; ttwid=1%7C62EW8bkx1Cg76n9lKzJSFsOMHJcXxNz294lVk9wdfxY%7C1649796160%7C2263d66dec4ac1d1debdc5bb37a22092bd7eb39b00f7c3538994edb615a22115",
        }

        proxies = Proxies.rand_proxy()
        for _ in range(3):
            proxy = next(proxies)
            proxy = {
                "http": f"{proxy.protocol}://{proxy.ip}:{proxy.port}",
                "https": f"{proxy.protocol}://{proxy.ip}:{proxy.port}",
            }
            try:
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    data=payload,
                    timeout=20,
                    proxies=proxy,
                )
                data = response.json()
                list_videos = data["Search"]
                list_videos = [list_videos.get(video) for video in list_videos]
                videos = []
                for video in list_videos:
                    video = VideoModel(
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
                    videos.append(video)
                return SearchResultVideo(query=query, videos=videos)
            except Exception:
                continue
        raise ValueError(f"Video Search for query {query} not found")
