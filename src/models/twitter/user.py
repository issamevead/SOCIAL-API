from typing import Optional
from contextlib import suppress
import os

from pydantic import BaseModel
import requests

from src.utils.util import get_timestamp_from_date, json_extract, url_quote
from src.utils.network import get_guest_token


class User(BaseModel):
    """Twitter User Data Class"""

    creation_date: Optional[str] = None
    user_id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None
    location: Optional[str] = None
    name: Optional[str] = None
    profile_pic_url: Optional[str] = None
    username: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[str] = None
    number_of_tweets: Optional[int] = None
    bot: bool = False
    timestamp: Optional[int] = None

    def get_user_details(self, username: str):
        """Get user details from twitter"""
        url = f"https://twitter.com/i/api/graphql/Bhlf1dYJ3bYCKmLfeEQ31A/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D"
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
            "referer": f"https://twitter.com/{username}",
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
                if response.status_code in (403, 429):
                    token = get_guest_token()
                    headers["x-guest-token"] = token
                    os.environ["GUEST_TOKEN"] = token
                if response.status_code == 200:
                    break
            data = response.json()
            self.user_id = (
                data.get("data", {}).get("user", {}).get("result", {}).get("rest_id")
            )
            data = json_extract(data, "legacy")
            if data:
                data = data[0]
                self.creation_date = data.get("created_at")
                self.timestamp = get_timestamp_from_date(self.creation_date)
                self.username = data.get("screen_name")
                self.name = data.get("name")
                self.follower_count = data.get("followers_count")
                self.following_count = data.get("friends_count")
                self.is_private = data.get("protected")
                self.is_verified = data.get("verified")
                self.location = data.get("location")
                self.name = data.get("name")
                self.profile_pic_url = data.get("profile_image_url_https")
                self.username = data.get("screen_name")
                self.description = data.get("description")
                self.number_of_tweets = data.get("statuses_count")
                with suppress(IndexError):
                    self.external_url = json_extract(data, "expanded_url")[0]
                return self
            else:
                raise ValueError(f"Twitter user with username = {username} not found")
        except Exception as error:
            raise ValueError(
                f"Twitter user with username = {username} not found"
            ) from error

    def get_user_tweets(
        self, username: str, count: int = 40, continuation_token: str = None
    ):
        """Get the list of user tweets"""
        user = self.get_user_details(username)
        if not user:
            raise ValueError(f"Twitter user with username = {username} not found")
        encoded_cursor = ""
        if continuation_token:
            encoded_cursor = url_quote(f',"cursor":"{continuation_token}"')
        url = f"https://twitter.com/i/api/graphql/cHgRKiUCS0R9UF0Io63POQ/UserTweets?variables=%7B%22userId%22%3A%22{user.user_id}%22%2C%22count%22%3A{count}{encoded_cursor}%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%2C%22__fs_responsive_web_like_by_author_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Atrue%2C%22__fs_interactive_text_enabled%22%3Atrue%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_responsive_web_edit_tweet_api_enabled%22%3Afalse%7D"

        if continuation_token:
            import json

            j = json.dumps(
                {
                    "dont_mention_me_view_api_enabled": True,
                    "interactive_text_enabled": True,
                    "responsive_web_uc_gql_enabled": True,
                    "vibe_api_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": False,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                    "responsive_web_enhance_cards_enabled": False,
                }
            )
            url = f"{url}{url_quote(f'features={j}')}"

        token = os.environ.get("GUEST_TOKEN")

        payload = {}
        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": 'personalization_id="v1_xSmqUavEIyQ7H2AOipPrgA=="; guest_id_marketing=v1%3A164346125100661461; guest_id_ads=v1%3A164346125100661461; guest_id=v1%3A164346125100661461; _ga=GA1.2.25750695.1651354472; _gid=GA1.2.1927393315.1651354472; g_state={"i_p":1651361679725,"i_l":1}; ct0=b4f0e042e2fc673efed6ff99e5c120cd; gt=1520887758813810689; guest_id=v1%3A165141059176729512; guest_id_ads=v1%3A165141059176729512; guest_id_marketing=v1%3A165141059176729512; personalization_id="v1_9RT+otgqcurodHweygMK2g=="',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": f"https://twitter.com/{username}",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "x-csrf-token": "b4f0e042e2fc673efed6ff99e5c120cd",
            "x-guest-token": token,
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "en",
        }
        from src.models.twitter.tweet import Tweet

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
            entries = json_extract(data, "entries")
            tweets = []
            if entries:
                for entry in entries[0]:
                    if entry.get("entryId", "").startswith("cursor-bottom-"):
                        continuation_token = entry.get("content", {}).get("value")
                        continue
                    if not entry.get("entryId", "").startswith("tweet"):
                        continue
                    datas = json_extract(entry, "legacy")
                    user = User()
                    tweet = Tweet()
                    video_count = json_extract(entry, "viewCount")
                    video_count = video_count[0] if video_count else 0
                    video_count = (
                        video_count
                        if (isinstance(video_count, int)) and video_count > 0
                        else None
                    )
                    tweet.video_view_count = video_count
                    for data in datas:
                        if data.get("default_profile") is not None:
                            user = User(
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
                                user.external_url = json_extract(data, "expanded_url")[
                                    0
                                ]
                            tweet.user = user
                        else:
                            if data.get("retweeted_status_result") is not None:
                                tweet = tweet.retweet_parse(
                                    data.get("retweeted_status_result")
                                )
                                tweet.retweet = True
                                break
                            tweet.tweet_id = data.get("id_str")
                            tweet.creation_date = data.get("created_at")
                            tweet.timestamp = get_timestamp_from_date(
                                tweet.creation_date
                            )
                            tweet.text = data.get("full_text")
                            tweet.language = data.get("lang")
                            tweet.retweet_count = data.get("retweet_count")
                            tweet.favorite_count = data.get("favorite_count")
                            tweet.reply_count = data.get("reply_count")
                            tweet.quote_count = data.get("quote_count")
                            user.user_id = data.get("user_id_str")
                            medias = json_extract(data, "media_url_https")
                            medias = list(set(medias))
                            tweet.media_url = medias if len(medias) > 0 else None
                    if tweet.tweet_id is None:
                        continue
                    tweets.append(tweet)
            return {
                "results": Tweet.order_by_timestamp(tweets),
                "continuation_token": continuation_token,
            }
        except Exception as error:
            raise ValueError(
                f"Tweets for user with username = {username} not found"
            ) from error

    def get_username_by_id(self, user_id: int):
        """Get the list of user tweets"""
        url = f"https://twitter.com/i/api/graphql/_w0cTirS6nTtBhFocRr6Kg/UserByRestId?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D"

        token = os.environ.get("GUEST_TOKEN")

        payload = {}
        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": 'personalization_id="v1_xSmqUavEIyQ7H2AOipPrgA=="; guest_id_marketing=v1%3A164346125100661461; guest_id_ads=v1%3A164346125100661461; guest_id=v1%3A164346125100661461; _ga=GA1.2.25750695.1651354472; _gid=GA1.2.1927393315.1651354472; g_state={"i_p":1651530966838,"i_l":2}; gt=1521209939108286471; ct0=79b8352376c7b899150c5357e3945a11; guest_id=v1%3A165141059176729512; guest_id_ads=v1%3A165141059176729512; guest_id_marketing=v1%3A165141059176729512; personalization_id="v1_9RT+otgqcurodHweygMK2g=="',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": "https://twitter.com/AymaneHachcham",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "x-csrf-token": "79b8352376c7b899150c5357e3945a11",
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
            username = json_extract(data, "screen_name")
            if username:
                return {"user_id": user_id, "username": username[0]}
            raise ValueError(f"Username for user id = {user_id} not found")
        except Exception as error:
            raise ValueError(f"Username for user id = {user_id} not found") from error

    def get_user_following(
        self, user_id: int, count: int = 20, continuation_token: str = None
    ):

        """Get the list of user following"""
        encoded_cursor = ""
        if continuation_token:
            encoded_cursor = url_quote(f',"cursor":"{continuation_token}"')

        url = f"https://twitter.com/i/api/graphql/Iu9o_AnYAuPWI6g1kgH_QA/Following?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A{count}{encoded_cursor}%2C%22includePromotedContent%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22__fs_responsive_web_like_by_author_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Atrue%2C%22__fs_interactive_text_enabled%22%3Atrue%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_responsive_web_edit_tweet_api_enabled%22%3Afalse%7D"

        payload = {}
        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": 'guest_id_marketing=v1%3A165159671676170563; guest_id_ads=v1%3A165159671676170563; personalization_id="v1_mTarCSUUA6hiCRqJavKZZA=="; guest_id=v1%3A165159671676170563; gt=1521533031202365441; _ga=GA1.2.2111906023.1651596718; _gid=GA1.2.1770956198.1651596718; _sl=1; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIz51YqAAToMY3NyZl9p%250AZCIlMjRmMDRjM2Q3NzQzZWUzM2NkYjJmMzkxMjQwYzBlZTc6B2lkIiVkZWVj%250AYzliYzBlNzYwNjkwN2RjNTNkZGFmYmEzYTA3Mg%253D%253D--8fe542bfceeef4f7cdc8568ba7080188d528def2; kdt=STf2Ez0vkghVgQwRKuG801acwSQ7SfjiD1nv6oMM; auth_token=c6a79b51cc97849a4ac25d77e451bbfa5902f549; ct0=80ed9f7ab25392601d3646c64b7210827ca852e91fa11115b7862f6760b49398291b153fc9a474fe7951b69f9fc9fd3c2cc0582026926904ed8e0acacd4f0998e58004c23a28a7a682bc616a239eba94; twid=u%3D96479162; att=1-29kdSxeFYu9YwqbwuPcBdw3Hp3DRs8Z4cfVUuoqs',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": "https://twitter.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "x-csrf-token": "80ed9f7ab25392601d3646c64b7210827ca852e91fa11115b7862f6760b49398291b153fc9a474fe7951b69f9fc9fd3c2cc0582026926904ed8e0acacd4f0998e58004c23a28a7a682bc616a239eba94",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en",
        }

        try:
            response = requests.get(url, headers=headers, params=payload)
            if response.status_code == 200:
                r = response.json()
                entries = json_extract(r, "entries")
                if entries:
                    entries = entries[0]
                users = []
                continuation_token = None
                for entry in entries:
                    if entry.get("entryId", "").startswith("cursor-bottom-"):
                        continuation_token = entry.get("content", {}).get("value")
                        continue
                    l = json_extract(entry, "legacy")
                    if not l:
                        continue
                    l = l[0]
                    user = User(
                        user_id=entry.get("entryId", "").replace("user-", ""),
                        name=l.get("name"),
                        creation_date=l.get("created_at"),
                        timestamp=get_timestamp_from_date(l.get("created_at")),
                        username=l.get("screen_name"),
                        follower_count=l.get("followers_count"),
                        following_count=l.get("friends_count"),
                        number_of_tweets=l.get("statuses_count"),
                        location=l.get("location"),
                        description=l.get("description"),
                        is_private=l.get("protected"),
                        is_verified=l.get("verified"),
                        profile_pic_url=l.get("profile_image_url_https"),
                    )
                    with suppress(IndexError):
                        user.external_url = json_extract(l, "expanded_url")[0]
                    users.append(user)
                return {"results": users, "continuation_token": continuation_token}
            raise ValueError(f"Following for user id = {user_id} not found")
        except Exception as error:
            raise ValueError(f"Following for user id = {user_id} not found") from error

    def get_user_followers(
        self, user_id: int, count: int = 20, continuation_token: str = None
    ):
        """Get a list of a user followers"""
        encoded_cursor = ""
        if continuation_token:
            encoded_cursor = url_quote(f',"cursor":"{continuation_token}"')

        url = f"https://twitter.com/i/api/graphql/E4u86hU-nCR6P_oNYKt4cw/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A{count}{encoded_cursor}%2C%22includePromotedContent%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22__fs_responsive_web_like_by_author_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Atrue%2C%22__fs_interactive_text_enabled%22%3Atrue%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_responsive_web_edit_tweet_api_enabled%22%3Afalse%7D"
        payload = {}
        headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": 'guest_id_marketing=v1%3A165159671676170563; guest_id_ads=v1%3A165159671676170563; personalization_id="v1_mTarCSUUA6hiCRqJavKZZA=="; guest_id=v1%3A165159671676170563; gt=1521533031202365441; _ga=GA1.2.2111906023.1651596718; _gid=GA1.2.1770956198.1651596718; _sl=1; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIz51YqAAToMY3NyZl9p%250AZCIlMjRmMDRjM2Q3NzQzZWUzM2NkYjJmMzkxMjQwYzBlZTc6B2lkIiVkZWVj%250AYzliYzBlNzYwNjkwN2RjNTNkZGFmYmEzYTA3Mg%253D%253D--8fe542bfceeef4f7cdc8568ba7080188d528def2; kdt=STf2Ez0vkghVgQwRKuG801acwSQ7SfjiD1nv6oMM; auth_token=c6a79b51cc97849a4ac25d77e451bbfa5902f549; ct0=80ed9f7ab25392601d3646c64b7210827ca852e91fa11115b7862f6760b49398291b153fc9a474fe7951b69f9fc9fd3c2cc0582026926904ed8e0acacd4f0998e58004c23a28a7a682bc616a239eba94; twid=u%3D96479162; att=1-29kdSxeFYu9YwqbwuPcBdw3Hp3DRs8Z4cfVUuoqs',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": "https://twitter.com/elonmusk/followers",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
            "x-csrf-token": "80ed9f7ab25392601d3646c64b7210827ca852e91fa11115b7862f6760b49398291b153fc9a474fe7951b69f9fc9fd3c2cc0582026926904ed8e0acacd4f0998e58004c23a28a7a682bc616a239eba94",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en",
        }

        try:
            response = requests.get(url, headers=headers, params=payload)
            if response.status_code == 200:
                r = response.json()
                entries = json_extract(r, "entries")
                if entries:
                    entries = entries[0]
                users = []
                continuation_token = None
                for entry in entries:
                    if entry.get("entryId", "").startswith("cursor-bottom-"):
                        continuation_token = entry.get("content", {}).get("value")
                        continue
                    l = json_extract(entry, "legacy")
                    if not l:
                        continue
                    l = l[0]
                    user = User(
                        user_id=entry.get("entryId", "").replace("user-", ""),
                        name=l.get("name"),
                        creation_date=l.get("created_at"),
                        timestamp=get_timestamp_from_date(l.get("created_at")),
                        username=l.get("screen_name"),
                        follower_count=l.get("followers_count"),
                        following_count=l.get("friends_count"),
                        number_of_tweets=l.get("statuses_count"),
                        location=l.get("location"),
                        description=l.get("description"),
                        is_private=l.get("protected"),
                        is_verified=l.get("verified"),
                        profile_pic_url=l.get("profile_image_url_https"),
                    )
                    with suppress(IndexError):
                        user.external_url = json_extract(l, "expanded_url")[0]
                    users.append(user)
                return {"results": users, "continuation_token": continuation_token}
            raise ValueError(f"Following for user id = {user_id} not found")
        except Exception as error:
            raise ValueError(f"Following for user id = {user_id} not found") from error
