from dataclasses import dataclass
import json
from typing import List

import requests
from bs4 import BeautifulSoup

from src.utils.util import json_extract
from src.utils.proxies import Proxies
from src.models.tiktok.video import VideoModel


@dataclass
class UserDetails:
    """Schema Class for a Youtube video"""

    username: str = None
    user_id: str = None
    profile_image: str = None
    following: int = None
    followers: int = None
    total_videos: int = None
    total_heart: int = None
    verified: bool = None


@dataclass
class UserId:
    """Schema Class for a Youtube video"""

    username: str = None
    user_id: str = None


@dataclass
class UserVideos:
    """Schema Class for a Youtube video"""

    username: str = None
    videos: List[VideoModel] = None


@dataclass
class User:
    """Schema Class for a Youtube video"""

    username: str = None
    user_id: str = None

    @staticmethod
    def get_user_id(username: str) -> int:
        url = f"https://www.tiktok.com/api/user/detail/?from_page=user&uniqueId={username}"

        # url = f"https://www.tiktok.com/api/user/detail/?aid=1988&app_language=fr&app_name=tiktok_web&battery_info=1&browser_language=fr-FR&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F103.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7140300747681777157&device_platform=web_pc&focus_state=false&from_page=user&history_len=2&is_fullscreen=false&is_page_visible=true&language=fr&os=windows&priority_region=&referer=&region=MA&screen_height=1080&screen_width=1920&secUid=MS4wLjABAAAAxnIsMUN4ZDTAfSOgt7UGPFf83VSMu8eetI2airVwxMxIlQ-upWYBuCgoBtJtxsaE&tz_name=Africa%2FCasablanca&uniqueId={username}&webcast_language=fr&msToken=1-XrQyx6olgZKar1CHAodqe_5TWPBLTe_tTRnDmSb3rr9Nc8XaunAezpBVU_pM4G4nXsHYpLMTdIYQ-nAsYMbJTmNGnX69bTBpc965OWULZW12U-RC617E1i8yTE1dNDqOnYyf4=&X-Bogus=DFSzswVODlbANGA/SQ/VLwOZax5d&_signature=_02B4Z6wo000014lwQ3QAAIDAVRxc3Euy-deJcEfAAIFTb8"

        payload = {}
        headers = {
            "authority": "www.tiktok.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": "_ttp=21akth2rpoX0jdOBHnOhNvKd64l; tt_csrf_token=alWAEGSv-sLRRQcLSo09921w_FD3vV-yuNLQ; __tea_cache_tokens_1988={%22_type_%22:%22default%22%2C%22user_unique_id%22:%226953619906265744898%22%2C%22timestamp%22:1658250762465}; _abck=B321D7862A19CE6DC0B3F366181D02D7~-1~YAAQBFQVAocETvmCAQAA3ZWDEwjXYo8WZhn0ME4Nv79ygV0RDiGCJca/x2YNgEBgppWGf7f9MGRwSDQRpTv6n4ejPEk7xxJlmJ4OQnlgQuF3U6gXthBxSPFBEzCWQS9mejjrTStLsTYTS9rcbGyShESOrvDCKcmx1BoX0toBCJrRjOSgMBfeh7Ls30hpC0AzSVHRXKGhB19pavgAiZp3C8BxMx16NgsPPBKuZWPRmhlvZvcMRwvewyrYPvcF+y/wbZVyn0yJl1IWeHaF6Ev7NXKJnAlsfCb4ZLWgqLzR/HMqhp/xQDp011giz+glvX5easfVo2zwPFX9gYaLiguLblvCuLV7PqkgEUw6CaUf/xkt+X3HdBGz28vcDk3DE1URXMSRf+iPMpsftQ==~-1~-1~-1; ak_bmsc=91F6F5F8B8FBA35834CB00FA1191847C~000000000000000000000000000000~YAAQBFQVAogETvmCAQAA3ZWDExE3v9KPG/Niy4pTKHJzlXUpLuqLoQDzST2xYFgvDtjE3QXHFAcAx3BSV1jqZ8V/67TCHb9/80qv9hdZrgS1RboTFuxM3uk7wbfSS7wZsr6uKQiD/bOCIIErcoHGfIP/s+TW/DuDPo6PzS+O6TVbHCoRvXP/aw9nAQHqyc+G36K7fnZoZIbxf51bz6hXuq1t74epBpThvxn6HgNQTw3GOE6mdllieTIqwsNWEIInX5anze8lFj51Fr8LeL7q5dumPywDcQLuAhVRATji9M9PZbo+um/toxbu9/UBZ7TlR/yglcnwMyPRJ9Egg02ZQ0CYUNY/OUC5p5Nqq5hdfuTyl+arxtMdihCnZEtMWVuA6n6fpJ3i5N4=; bm_sz=E47C291C50B73444B05590B33F15CA9E~YAAQBFQVAokETvmCAQAA3pWDExGNod3B8cL6QKQ6hw0jmAc/UO8J4hR1yxiah2sL3gKbsQLEH6Cu7zaUDCZwD8FhUxh0fFebeanYYd163I/H7AZhbn12Zn1muG6EBZMAOXWB7A9FGb8Xh6nlmK0yBPA0xJ09dZFTkPlM2RrqXzAz/vSByEzrIlBv98J/cs3vDHYY2qWHM4G/l12glLAETLJIKCCcQOp50C1OiQVT0oHOHFFNG5S0HANYdVk/ooGDFboe04NkxRZZDMjsRJCVHxvOTifB5NYzBXk5zGd44P3PHTw=~3422262~3621431; ttwid=1%7CDg8tjfOo2dC9UJrlgRfJ2DJ7GYd2SSSyLpyEx9iDcNE%7C1662480061%7Cc5b1eb8640aa876f99cc845608a0910bace6970c8279d5a99af39ef4c6fff951; msToken=2pN2CBfBqcp-QI3BjuZvGFUzIi_NKVzeRsOfjSgf3kLMQIrGWU29-WkvtyXUoU7nXbXTF7JNvd3udjYtKu6aHrXrJS6xhV2O79kz8ECOvPOn2Kq1XjvA0M-5zVWz4Zjdy5lLaPA=; msToken=E-59bDozxVqQ96D1Hhk_h_bcg3R_BpW6w0vAW_a-nUjaQJQpooDRVfn58APRCy7mGggrhDzmBeyc_oqWR2Pb6nUAEYsivGpAFI9WhL-CFUSV1j-efE6YJcoRnkxR3wyzemUL4ik=; bm_sv=CD5C4ECB49081FF54335B3EE04EAFBAE~YAAQV2RkXx048PaCAQAA+zTdExGJI0L71oL0qf/sVm3ws++pMTVGPC9XwoudVRPKrf2aRDzPxynJmN6pE23QkqnmrsLl9Qlv/PHRwbsPygDwIvIBHXPBnlByzDuWipyORtdpdzIXYaM2JzGXFwptGsGfN7yCN2yNBP6yvCklwaq+nKoQJqCt5kBdyer06+VuBLiu/D4mXlUYrhWsoq7Rqn54O5qx17SzISvWtKriLhFN8O0JMX9OnWMSFIk5HNFE~1; _abck=B39241FB40F63851A1F866348B137710~-1~YAAQ5RzAUcpqM/KCAQAAVPe5Ewi9kD6Dg+AmPS5LVO6zWo5kq+ISQ4RubWvhJzLFAH1wV049LVvpP6ld1ehA7yIadb3h71THpY59dJ3sm80c86a7kY124pKcaulBHccjJEz6TRUke4ZDyVQsX1rB5LxbRYgt1RAj2dC4FSKT7OZeaOBOf2e4RCdSJorQjnDkZgHmwEV4bUwHWvzLBxy6gLE3NVo/tTgcNwj2noYKh+BnVrFgwvfUhNAOOQOKiz5yjjOT0XnwBAYkg27LvRWKnPptMWBc4E9XamBQXRme4Y20i7ptE66YBytglgBtHxEaWIGCtQIeoDmcMqvOcLIDkhsaC+ARNQ6YX7utix/c13CdLVQF3SIedNsrq9I=~-1~-1~-1; ak_bmsc=F7BF9C6B5223EF8DD2026D8874C4DCD8~000000000000000000000000000000~YAAQVmRkXz88KvKCAQAAF/rPExHgSt8ElhJTin5BgJ7QnClcUBspI/LU4aLxscUCerKqy7Fd9xAIPDm0cHv9/nZFpMOB9YcJmvS+hEhT/aEB2D3LnR4Ybt4+/jeTqZ/t8k7hO25afy8gm8jKiHr9JRrc9J3gsSJHF48kn/J6YRhNDZk8OCB94PYOb9nQj9liKs34pXnxLHTeA/PYcL/N5dBdeKWagh/yNujr27AUSyVXMdgZ4totn1ujf+QleW6k8Lz86rpXG3iY3NpEZLC33W2xc5mxjpXmW7w/QdNbzBp9om3oY+b3+5BzTsqr5+m6vdlspsNHxY5tEemkL6hTm+2bLhtFiyR4iZ5m/dKcRe1rbarLEpEmaIbtcPvIiRk4lVMtJD9girOS/XYfevQ=; bm_sv=CD5C4ECB49081FF54335B3EE04EAFBAE~YAAQLFQVAtAkJwCDAQAAyLDdExGc7g+vCvg7nE92mF9nZSn783JNqbA2vFLTWbUw5Srb+OA94K6GE+wZK55Det3c771HGOWHIITxfg91h5W2Jjr5Q8YAzNl1saDYYUJHvfMXNA8Sk7yBRAsaHL1LGoWxTNFG12p+AJCQ+s4DLtkfn/jbFvv0LCYR3IHRFYetIWFVjy0f24IBi4XT3g8SumBdSjNUds9/RIrPIsi/bmawVpELdEjrF+CoBzKJpgRa~1; bm_sz=A12E7E200A58FB1A0315203B8A3E86DF~YAAQ5RzAUcxqM/KCAQAAVPe5ExHGUkRE4paFcHD3MkCDnW9P5lcrtHdJEE+Rvo8CGKBA04QTwhXyPtJ6lgU2dJfTZ6Gfko6zgDdJK4Pw0q2bEykW8naaL45t1hQ6QhtPBRF++XY9BAkhO42388WGb4qMrsgKtluV2IdwtlBnl4JPc5k/JAWC0Y+7l45Wofc06CoadbhX9JJHebAPxOhH0tmrDuvQzW3c1pvsjKHr4WWO7eMkrefxjvC60+lSqjkbF2RR0k57pEH+zC1hatWky/6PNiHfXMqlvUEMvf5iOOISblI=~3684164~3687235; msToken=NWXpz37ifO7AS_GHIGCWeNRNByiWuDe0cfTt--7wFmwZ7V7rQLGeuU4Ps4gizSUxaz6Qlu-paB1ykR8ze43n0155wlKBGk8qKfXib4mJ_odU-0aBTMOAybRGlzm8ifJicvqo918=",
            "pragma": "no-cache",
            "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }
        proxies = Proxies.rand_proxy(secure=False)
        for _ in range(2):
            proxy = next(proxies)
            proxy = {
                "http": f"{proxy.protocol}://{proxy.host}:{proxy.port}",
                "https": f"{proxy.protocol}://{proxy.host}:{proxy.port}",
            }
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    data=payload,
                    timeout=10,
                    proxies=proxy,
                )
                r = response.json()
                user_id = json_extract(r, "id")
                if len(user_id) == 0:
                    break
                return User(username=username, user_id=int(user_id[0]))
            except Exception as _:
                proxies = Proxies.rand_proxy(secure=True)
                continue
        raise ValueError(f"User {username} not found")

    @staticmethod
    def get_user_details(username: str) -> int:
        url = f"https://www.tiktok.com/api/user/detail/?aid=1988&app_language=en&app_name=tiktok_web&battery_info=0.78&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.84%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7082044281019909637&device_platform=web_pc&focus_state=true&from_page=user&history_len=4&is_fullscreen=false&is_page_visible=true&language=en&os=mac&priority_region=&referer=&region=MA&screen_height=1050&screen_width=1680&secUid=MS4wLjABAAAA-Dx-shd6fPSLGpwRA_FfsjDDbH35HHnq1CPvCZ9BnqZFgF2178wXxH25_DmUkahw&tz_name=Africa%2FCasablanca&uniqueId={username}&webcast_language=en&msToken=XCA_IHj_IzFKukO4IJyTRveOVixFe6r2ZfXmpN60sRxZja05QA_UB3_cqPr-8Oz3FySKphFL1eTGMPAyari9BWqLlXbSk4r5zqmhyGgC5mV-9l6iZTTIcw3MsFVS4DX4J2IDaWc=&X-Bogus=DFSzswVO5liANxSnSlLCVV/F6qyq"

        payload = {}
        headers = {
            "authority": "www.tiktok.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": f"https://www.tiktok.com/@{username}",
            "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }
        proxies = Proxies.rand_proxy()
        for _ in range(2):
            proxy = next(proxies)
            try:
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    data=payload,
                    timeout=10,
                    proxies=proxy.to_dict(),
                )
                res = response.json()
                return UserDetails(
                    username=json_extract(res, "uniqueId")[0],
                    user_id=int(json_extract(res, "id")[0]),
                    profile_image=json_extract(res, "avatarLarger")[0],
                    following=int(json_extract(res, "followingCount")[0]),
                    followers=int(json_extract(res, "followerCount")[0]),
                    total_videos=int(json_extract(res, "videoCount")[0]),
                    total_heart=int(json_extract(res, "heartCount")[0]),
                    verified=json_extract(res, "verified")[0],
                )
            except Exception:
                proxies = Proxies.rand_proxy(secure=True)
                continue
        raise ValueError(f"User {username} not found")

    @staticmethod
    def get_videos(username: str) -> List[VideoModel]:

        url = f"https://www.tiktok.com/@{username}"

        payload = {}
        headers = {
            "authority": "www.tiktok.com",
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
            "cookie": "tt_csrf_token=GZ11NIxWsyRBCs2XfsbTKHxX; _abck=CC8D62AD3D9AAA59550D9884BE2E6D5E~-1~YAAQrp4XAoOvuv1/AQAAjFOaAAdGF+6ev5wht3XYQEnZvPfIqlFZKcpw0hopVk8LruvFKBSKy0d/EoHvUUGARgDJTTV7n7swHJzOxt0cqGM3lTqUAFvgug+Rq5kaRXq3JEJT8UZohQwIMuGq8F5GF4uzjpUGbpfjMqq2twL/xriSpl8WrqWbNxqLfGPOqhRhnFnI+iJNBPv/ss+FNf3jl6PzhSvy8CH1+je0b+nNaN4g75uzbQdnT5/tk+cUf9ekxZvHeso7zwaCVXuDpdI/QrOn/35AydH+QO6c5zuhsHMgKK7FKr2NqoF8CIXXl96u7+Zi/ClPLqCJNQW67zNl/YU/eXKabGuqOx4dzd+ZVNUd38a94gUZ1vVkg3+pWyPO5nmRVUY9BxKQWA==~-1~-1~-1; ak_bmsc=4E5806A5F182207FF4AC91F62A74D759~000000000000000000000000000000~YAAQrp4XAoSvuv1/AQAAjFOaAA9HOhgZ5VHYnbPTEt2QLQQjYdnxTxbJQFIdVgHO5XGC5rZ+4TckXfxu1YNo9sUJoX/zFDFsZa10vYipY29ORC+EKK6CkrVXUFNlUph1S5NPRkvJEkfJRj2cy1io3jVft4FRSC5/63PHm/5IxdyU9WfVYxQlTV4AR4f0tCZFqRg/pmmW5gXu5TrXmXEJlnY2WvG98waFjKHQEPSutdLhvAfsilceHKS3AW5UpgpVkK3APvU+tYFd1slGd9DHbBT3hPiJKOPBfi/ljls/ac9Ux7uyHqTedY3aKGv3RqUET/7hl3jej3uzeZ1WjEGYseUjcbtmFh/6C4XC24Klezx0L05LjYT8OYa6HZBNWY1e2QIftOOfAAuP; bm_sz=4C564413D72F3AB8FD90D56722714E64~YAAQrp4XAoWvuv1/AQAAjFOaAA8BaMm1o5OcEpN1Fq85MdF2C+ZYLO12AtTWVljnDD0Dd9ZIPSQUMfuACyPT4jTjINfPafMz47cvkMZIfPTX/Z7JDkWKiI8PqiTiXgvUGiYaCr57mmXVxrf/jlMJfcequlLVq4B+XjDZ232CVKapQ95wHsFvccWNm2bpe1x9GWSye52/oopN59YXBdG9KpL+Bx0uWo25YjGj3o1eFIQj3RnPo48iuj8dCFu8Y52mjsbEMS1xHiIvrS9M9ouzVlpDVc4quWwM1Nt9R0wzG+3jHBw=~3225141~3749682; __tea_cache_tokens_1988={%22_type_%22:%22default%22}; bm_mi=0EA26A9829399D1F9DED88E861CEEBFF~nMRQ4hSFq5KgiLCfxHrIXPvA+FQevFCJK5ep58HlSh92TMHUrjvDjHAaln7rXDMc9SdzrEQ/o08mSYDoWIugHwuL3pOC8zkIjwxuznbJzSNErI70mOP5pmmWRj9+5Pz1Tx8+EhdQssL7yc6QMbQJck4Tv8PlzD8K5qVnx638sq/2ssVjjot0p6amWQFBFQsOUbfvzev3K+UBIKUyjKDo+oGqh4hOnYZgWbJIenRxftlmfWR6Xb3YiwQbIYtLRVuw; ttwid=1%7C6eaPXeOGttJsSB5moV4GbOrZ8TMvrjUqnkuPBjhZA3s%7C1649277581%7Cb9bfabc3429906c033fceb558f56e2d78d124177414a8bb5d4e9f051773febac; msToken=KG22SN53lJoT9k2nzrGqnqk3jF0qtXNUKioHFnMXWNjm94AAzZ1uSs-Dhm9Lv7HDoTzFldr7ZR9wSee0SSlsPRKvbvKm2PduXxbYChA-L_LPF_ivIFLwQiV2xIiQHJCEW-JwSo4m-o8yozi69g==; msToken=5NDOKmi0GjRPMfA4g6-OWzZmcux_hmF3nASPPzRCfl278cOcy18lhLVBRwLhB9clMO5QclpetX_dBzgXkFL0hgrkhLz_-6Hp8g3paFcQzb51ZmUyqICspIr74R-4yrHvYQBxXPlPuTd9EPxO9Q==; bm_sv=3A6489C41D04B80DA2B58B842B7AB2E2~s4nPK5/et8MVx/dYCX59eq1Bechc7x1XY2UzYE6Mdli3CXj8qfjtOZO8qXVHzY4NAPncaYpCU8LN8ADPd9x1dQiJMYhiEZTplIeP1IfmoeRhk8bO7CeikLDRG42IuyVIjFnoUFBPARQOhOShQnCNgp6dY2/jFDZ1hRbC30+rJ0c=; _abck=CC8D62AD3D9AAA59550D9884BE2E6D5E~-1~YAAQDlQVAi9AFA2AAQAAenUpEAdLvkFMc0K0OSUimQJ65o8ViVqFB9+lxRg/npuqaKX/QUWz0GjVpjcTEFjU8TojiAQyszJ9OtVg0eiOpzwSXj6eMZrrkeKRA2ssmd6Hvdrh36Z/XPZyNXBJcAKuAg09N5e5peYRlxYV8yvx75gZtT+nWBb4GdQJHqFHgXpCkuzDpKe06PluAMHLx9HVjc6NAiCPgr4SOA8UK5RnIIeYgfMaMJ5HBz+SNlTrWwrBe6ENMtVj0hpIr45rD5L51e1rKqG+DHZNmOtZYsnaryZhWqdFMPxsUkBYFKj35YjxYnMR6I7qc7edLGbDt8srFJwjJin8gsVTluuYG3K+1qc=~-1~-1~-1; msToken=bhsEhdavCsRBce-vJgUlszfJFbRlzd2bCgIKU0ZUUM4UosgsIDJyW2V_AC4YP_ZUIVhQvMuX9VGFCrd9td2fqzYFYiA404gRBEtuvUaKR_UUh_kCXDGTenvZM3vb3E5mQvMxNHldK_Ek1w7qYA==; tt_csrf_token=ixvWTwMn-fxgsNzu798S0x-W0o89qedhoCNE",
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
                soup = BeautifulSoup(response.text, "html.parser")
                metadata = soup.find("script", {"id": "sigi-persisted-data"})
                data = "{" + metadata.string.split("]={")[1].split("};")[0] + "}"
                data = json.loads(data)
                list_videos = data["ItemModule"]
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
                return UserVideos(username=username, videos=videos)
            except Exception:
                proxies = Proxies.rand_proxy(secure=True)
                continue
        raise ValueError(f"Videos for {username} not found")
