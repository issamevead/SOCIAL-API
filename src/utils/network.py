import requests


def get_guest_token():

    url = "https://api.twitter.com/1.1/guest/activate.json"

    payload = {}
    headers = {
        "authority": "api.twitter.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "cache-control": "no-cache",
        "content-length": "0",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": 'guest_id_marketing=v1%3A165141020576783951; guest_id_ads=v1%3A165141020576783951; personalization_id="v1_FPFqgD9GYvgbNTjNHE3HdQ=="; guest_id=v1%3A165141020576783951; ct0=b9dc3f7462e39951690286e717bcd71a; gt=1520750742243577858',
        "dnt": "1",
        "origin": "https://twitter.com",
        "pragma": "no-cache",
        "referer": "https://twitter.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
        "x-csrf-token": "b9dc3f7462e39951690286e717bcd71a",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["guest_token"]
