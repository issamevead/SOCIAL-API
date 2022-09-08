BASE_URL = "https://www.instagram.com/"
URL_HASHTAG_QUERY = BASE_URL + "graphql/query/?query_hash={}&variables={}"
URL_WEB_HASHTAG_QUERY = (
    "https://i.instagram.com/api/v1/tags/logged_out_web_info/?tag_name={}"
)
HASHTAG_HEADERS = {
    "authority": "i.instagram.com",
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9",
    "cache-control": "no-cache",
    "cookie": "csrftoken=EpHabi7NeB3vNcTsv2EE3zVKWO8Fv2u7; mid=YwyQ8AALAAEY5GhwK_L--_FtVZ3l; ig_did=3011A2E6-F517-4E09-A0E7-3AE2A4CDBD82; ig_nrcb=1; datr=oasMY2v3tyV6vm1bXSEZ7pL9; csrftoken=5EaeghvFnfZdJ2FhuX9rH6CnFwU6Idaa; ig_did=456545FC-015E-4F1F-9432-CC858F153006; ig_nrcb=1; mid=YwZVowALAAF9NbINoRJlwldd6o7w",
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
    "x-csrftoken": "EpHabi7NeB3vNcTsv2EE3zVKWO8Fv2u7",
    "x-ig-app-id": "936619743392459",
    "x-ig-www-claim": "0",
}

QUERY_COMMENTS_VARS = '{"shortcode":{},"child_comment_count":{},"fetch_comment_count":{},"parent_comment_count":{},"has_threaded_comments":{}}'
QUERY_COMMENTS = (
    BASE_URL + "graphql/query/?query_hash=9f8827793ef34641b2fb195d4d41151c&variables={}"
)
COMMENTS_HEADERS = {
    "authority": "www.instagram.com",
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9",
    "cache-control": "no-cache",
    "cookie": "csrftoken=EpHabi7NeB3vNcTsv2EE3zVKWO8Fv2u7; mid=YwyQ8AALAAEY5GhwK_L--_FtVZ3l; ig_did=3011A2E6-F517-4E09-A0E7-3AE2A4CDBD82; ig_nrcb=1; datr=oasMY2v3tyV6vm1bXSEZ7pL9; csrftoken=5EaeghvFnfZdJ2FhuX9rH6CnFwU6Idaa; ig_did=456545FC-015E-4F1F-9432-CC858F153006; ig_nrcb=1; mid=YwZVowALAAF9NbINoRJlwldd6o7w",
    "pragma": "no-cache",
    "referer": "https://www.instagram.com/p/Ch1_0geP05h/",
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
    "x-csrftoken": "EpHabi7NeB3vNcTsv2EE3zVKWO8Fv2u7",
    "x-ig-app-id": "936619743392459",
    "x-ig-www-claim": "0",
    "x-requested-with": "XMLHttpRequest",
}
