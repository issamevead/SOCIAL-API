"""Tweet Handler Module"""
from typing import Optional, List, Any
from contextlib import suppress
import os
import json

from pydantic import BaseModel
import requests

from src.models.twitter.user import User
from src.utils.util import get_timestamp_from_date, json_extract
from src.utils.network import get_guest_token


class Tweet(BaseModel):
    """Tweet Data Class"""

    tweet_id: Optional[str] = None
    creation_date: Optional[str] = None
    text: Optional[str] = None
    media_url: Optional[List[str]] = None
    user: Optional[User] = None
    language: Optional[str] = None
    favorite_count: Optional[int] = None
    retweet_count: Optional[int] = None
    reply_count: Optional[int] = None
    quote_count: Optional[int] = None
    retweet: Optional[bool] = False
    timestamp: Optional[int] = None
    video_view_count: Optional[int] = None

    @staticmethod
    def order_by_timestamp(tweets: List[Any]):
        """Order Tweets by Timestamp"""
        if tweets is not None:
            return sorted(tweets, key=lambda x: x.timestamp, reverse=True)
        return tweets

    def retweet_parse(self, data: dict):
        """Parse Retweet Data"""
        tweet = data.get("result", {}).get("legacy", {})
        user = data.get("result", {}).get("core", {})
        des = json_extract(user, "description")
        des = list(
            filter(lambda x: isinstance(x, str) and x.strip() == "Automated", des)
        )
        user = json_extract(user, "legacy")
        user = list(filter(lambda x: x.get("created_at") is not None, user))
        user = user[0] if user else {}
        external_url = None
        with suppress(IndexError):
            external_url = json_extract(data, "expanded_url")[0]
        count = json_extract(data, "viewCount")
        count = count[0] if count else None
        count = count if (isinstance(count, int)) and count > 0 else None
        return Tweet(
            tweet_id=tweet.get("id_str"),
            creation_date=tweet.get("created_at"),
            timestamp=get_timestamp_from_date(tweet.get("created_at")),
            text=tweet.get("full_text"),
            language=tweet.get("lang"),
            retweet_count=tweet.get("retweet_count"),
            favorite_count=tweet.get("favorite_count"),
            reply_count=tweet.get("reply_count"),
            quote_count=tweet.get("quote_count"),
            retweet=True,
            video_view_count=count,
            user=User(
                creation_date=user.get("created_at"),
                username=user.get("screen_name"),
                name=user.get("name"),
                follower_count=user.get("followers_count"),
                following_count=user.get("friends_count"),
                is_private=user.get("protected"),
                is_verified=user.get("verified"),
                location=user.get("location"),
                profile_pic_url=user.get("profile_image_url_https"),
                description=user.get("description"),
                number_of_tweets=user.get("statuses_count"),
                bot=bool(des),
                external_url=external_url,
            ),
        )

    def get_tweet_details(self, tweet_id: str) -> dict:
        """Return Tweet Details"""
        url = f"https://twitter.com/i/api/graphql/6n-3uwmsFr53-5z_w5FTVw/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{tweet_id}%22%2C%22referrer%22%3A%22profile%22%2C%22rux_context%22%3A%22HHwWhICzkbKa55kqAAAA%22%2C%22with_rux_injections%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%2C%22__fs_responsive_web_like_by_author_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Atrue%2C%22__fs_interactive_text_enabled%22%3Atrue%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_responsive_web_edit_tweet_api_enabled%22%3Afalse%7D"
        token = os.environ.get("GUEST_TOKEN")

        payload = {}
        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": 'personalization_id="v1_xSmqUavEIyQ7H2AOipPrgA=="; guest_id_marketing=v1%3A164346125100661461; guest_id_ads=v1%3A164346125100661461; guest_id=v1%3A164346125100661461; ct0=8830613edb8b1c7ca737fa2f185e2d0c; gt=1520516975646154758; _ga=GA1.2.25750695.1651354472; _gid=GA1.2.1927393315.1651354472; g_state={"i_p":1651361679725,"i_l":1}',
            "dnt": "1",
            "pragma": "no-cache",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "x-csrf-token": "8830613edb8b1c7ca737fa2f185e2d0c",
            "x-guest-token": token,
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "en",
        }

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
            items = json_extract(data, "entries")
            with open("tweet_data.json", "w") as f:
                json.dump(items, f)
            if items:
                items = items[0]
                for item in items:
                    if tweet_id in item.get("entryId"):
                        tweet_data = json_extract(item, "legacy")
                        
                        for data in tweet_data:
                            if data.get("default_profile") is not None:
                                count = json_extract(data, "viewCount")
                                if count:
                                    count = count[0]
                                    count = count if isinstance(count, int) and count > 0 else None
                                    self.video_view_count = count
                                self.user = User(
                                    creation_date=data.get("created_at"),
                                    timestamp=get_timestamp_from_date(
                                        data.get("created_at")
                                    ),
                                    username=data.get("screen_name"),
                                    name=data.get("name"),
                                    follower_count=data.get("followers_count"),
                                    following_count=data.get("friends_count"),
                                    is_private=data.get("protected"),
                                    is_verified=data.get("verified"),
                                    location=data.get("location"),
                                    profile_pic_url=data.get("profile_image_url_https"),
                                    description=data.get("description"),
                                    number_of_tweets=data.get("statuses_count"),
                                )
                                with suppress(IndexError):
                                    self.user.external_url = json_extract(
                                        data, "expanded_url"
                                    )[0]
                            else:
                                if data.get("retweeted_status_result") is not None:
                                    return self.retweet_parse(
                                        data.get("retweeted_status_result")
                                    )
                                count = json_extract(data, "viewCount")
                                if count:
                                    count = count[0]
                                    count = count if isinstance(count, int) and count > 0 else None
                                    self.video_view_count = count
                                self.tweet_id = data.get("id_str")
                                self.creation_date = data.get("created_at")
                                self.text = data.get("full_text")
                                with suppress(IndexError):
                                    medias = json_extract(data, "media_url_https")
                                    medias = list(set(medias))
                                    self.media_url = medias if len(medias) > 0 else None
                                self.language = data.get("lang")
                                self.favorite_count = data.get("favorite_count")
                                self.retweet_count = data.get("retweet_count")
                                self.reply_count = data.get("reply_count")
                                self.quote_count = data.get("quote_count")
                                if self.user is not None:
                                    self.user.user_id = data.get("user_id_str")
            return self
        except Exception as error:
            raise ValueError(f"Unable to get data for tweet ID = {tweet_id}") from error
