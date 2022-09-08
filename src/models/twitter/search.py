from contextlib import suppress
from datetime import datetime
from typing import Optional, List
from enum import Enum
import os

from pydantic import BaseModel
import requests

from src.models.twitter.user import User
from src.models.twitter.tweet import Tweet
from src.utils.util import get_timestamp_from_date, json_extract, url_quote
from src.utils.network import get_guest_token


class SearchSection(Enum):
    """Search Section Enum"""

    TOP: str = "top"
    LATEST: str = "latest"  # live
    PEOPLE: str = "people"
    PHOTOS: str = "photos"
    VIDEOS: str = "videos"


class SearchSectionQuery(Enum):
    """Search Section Query Enum"""

    TOP: str = ""
    LATEST: str = "tweet_search_mode=live"  # live
    PEOPLE: str = "result_filter=user"
    PHOTOS: str = "result_filter=image"
    VIDEOS: str = "result_filter=video"


class Search(BaseModel):
    """Tweet Data Class"""

    tweets: List[Optional[Tweet]] = None

    def _parse_search_users(self, users):
        """Parse search users"""
        final_users = []
        users = [users[user] for user in users]
        for user in users:
            user_object = User(
                user_id=user.get("id_str"),
                creation_date=user.get("created_at"),
                timestamp=get_timestamp_from_date(user.get("created_at")),
                username=user.get("screen_name"),
                name=user.get("name"),
                follower_count=user.get("followers_count"),
                following_count=user.get("friends_count"),
                is_private=user.get("protected"),
                is_verified=user.get("verified"),
                location=user.get("location"),
                description=user.get("description"),
                number_of_tweets=user.get("statuses_count"),
                profile_pic_url=user.get("profile_image_url_https"),
            )
            with suppress(IndexError):
                user_object.external_url = json_extract(user, "expanded_url")[0]
            final_users.append(user_object)
        return final_users

    def _parse_search_results(self, tweets: dict, users: dict):
        """Parse search results"""
        final_tweets = []
        tweets = [tweets[tweet] for tweet in tweets]
        for tweet in tweets:
            tweet_user_id = tweet.get("user_id_str", {})
            user = users.get(tweet_user_id, {})
            count = json_extract(tweet, "viewCount")
            count = count[0] if count else None
            count = count if (isinstance(count, int)) and count > 0 else None
            tweet_object = Tweet(
                tweet_id=tweet.get("id_str"),
                creation_date=tweet.get("created_at"),
                timestamp=get_timestamp_from_date(tweet.get("created_at")),
                text=tweet.get("full_text"),
                favorite_count=tweet.get("favorite_count"),
                retweet_count=tweet.get("retweet_count"),
                reply_count=tweet.get("reply_count"),
                quote_count=tweet.get("quote_count"),
                retweet=tweet.get("retweeted"),
                language=tweet.get("lang"),
                video_view_count=count,
                user=User(
                    user_id=tweet_user_id,
                    creation_date=user.get("created_at"),
                    timestamp=get_timestamp_from_date(user.get("created_at")),
                    username=user.get("screen_name"),
                    name=user.get("name"),
                    follower_count=user.get("followers_count"),
                    following_count=user.get("friends_count"),
                    is_private=user.get("protected"),
                    is_verified=user.get("verified"),
                    location=user.get("location"),
                    description=user.get("description"),
                    number_of_tweets=user.get("statuses_count"),
                    profile_pic_url=user.get("profile_image_url_https"),
                ),
            )
            with suppress(IndexError):
                tweet_object.media_url = tweet.get("media", {}).get("media_url_https")
            with suppress(IndexError):
                tweet_object.user.external_url = json_extract(user, "expanded_url")[0]
            final_tweets.append(tweet_object)
        return final_tweets

    def search(
        self,
        query: str,
        mode: SearchSection = SearchSection.TOP.value,
        count: int = 20,
        language: str = "en",
        continuation_token: Optional[str] = None,
        min_replies: Optional[int] = None,
        min_likes: Optional[int] = None,
        min_retweets: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """Return search results"""
        token = os.environ.get("GUEST_TOKEN")
        if min_likes is not None:
            query = f"{query} min_faves:{min_likes}"
        if min_retweets is not None:
            query = f"{query} min_retweets:{min_retweets}"
        if min_replies is not None:
            query = f"{query} min_replies:{min_replies}"
        if start_date is not None:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            query = f"{query} since:{start_date.year}-{start_date.month}-{start_date.day}"
        if end_date is not None:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query = f"{query} until:{end_date.year}-{end_date.month}-{end_date.day}"
        query = url_quote(query)
        search_mode = f"&={SearchSectionQuery[mode.value.upper()].value}"
        url = f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={query}&count={count}{search_mode}&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo"
        if continuation_token:
            continuation_token = url_quote(continuation_token)
            url += f"&cursor={continuation_token}"
        payload = {}
        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": language.value,
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "cookie": 'personalization_id="v1_xSmqUavEIyQ7H2AOipPrgA=="; guest_id_marketing=v1%3A164346125100661461; guest_id_ads=v1%3A164346125100661461; guest_id=v1%3A164346125100661461; _ga=GA1.2.25750695.1651354472; _gid=GA1.2.1927393315.1651354472; g_state={"i_p":1651530966838,"i_l":2}; ct0=664a22bcdf50e0259323f46b80abb30a; gt=1521163716968001542; guest_id=v1%3A165141059176729512; guest_id_ads=v1%3A165141059176729512; guest_id_marketing=v1%3A165141059176729512; personalization_id="v1_9RT+otgqcurodHweygMK2g=="',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": f"https://twitter.com/search?q={query}",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "x-csrf-token": "664a22bcdf50e0259323f46b80abb30a",
            "x-guest-token": token,
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": language.value,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        try:
            for _ in range(3):
                response = requests.request("GET", url, headers=headers, data=payload)
                if response.status_code == 403:
                    token = get_guest_token()
                    headers["x-guest-token"] = token
                    os.environ["GUEST_TOKEN"] = token
                if response.status_code == 200:
                    break
            data = response.json()
            global_object = data.get("globalObjects", {})
            tweets = global_object.get("tweets", {})
            users = global_object.get("users", {})
            cursors = json_extract(data, "cursor")
            results = []
            if mode == SearchSection.PEOPLE:
                results = self._parse_search_users(users)
            else:
                results = self._parse_search_results(tweets, users)
            continuation_token = None
            for cursor in cursors:
                if cursor.get("cursorType", "").startswith("Bottom"):
                    continuation_token = cursor.get("value")
            return {"results": results, "continuation_token": continuation_token}
        except Exception as error:
            raise ValueError(f"Unable to get data for query = {query}") from error
