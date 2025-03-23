import json
import urllib.parse

import requests

import config


def get_liked_tweets_internal():
    """
    直接调用 X 内部 GraphQL 接口获取点赞数据。
    需要 Bearer Token 和 X-Csrf-Token（使用 ct0 值）两个额外请求头。
    当 config.ALL 为 True 时，会循环获取所有点赞数据，直到没有下一页（cursor 无变化）为止。
    返回解析后的 tweet 列表。
    """
    headers = {
        "Authorization": f"Bearer {config.BEARER_TOKEN}",
        "Cookie": f"auth_token={config.AUTH_TOKEN}; ct0={config.CT0}",
        "X-Csrf-Token": config.CT0,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    all_tweets = []
    cursor = None
    while True:
        variables = {
            "userId": config.USER_ID,
            "count": int(config.COUNT),
            "includePromotedContent": False,
            "withClientEventToken": False,
            "withBirdwatchNotes": False,
            "withVoice": True,
            "withV2Timeline": True
        }
        if cursor:
            variables["cursor"] = cursor

        variables_encoded = urllib.parse.quote(json.dumps(variables, separators=(',', ':')))
        features_encoded = urllib.parse.quote(config.LIKES_FEATURES)
        fieldToggles_encoded = urllib.parse.quote(config.LIKES_FIELDTOGGLES)

        url = f"{config.LIKES_API_URL}?variables={variables_encoded}&features={features_encoded}&fieldToggles={fieldToggles_encoded}"

        # 打印 URL 和 headers，便于调试
        print("请求 URL:", url)
        print("请求 headers:", headers)

        proxies = None
        if config.ENABLE_PROXY:
            proxies = {
                "http": config.HTTP_PROXY,
                "https": config.HTTP_PROXY
            }
            print("使用 HTTP 代理:", proxies)

        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code != 200:
            raise Exception(f"API 请求失败: {response.status_code} {response.text}")
        data = response.json()

        tweets = []
        new_cursor = None
        try:
            instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
            for instruction in instructions:
                if instruction.get("type") == "TimelineAddEntries":
                    for entry in instruction.get("entries", []):
                        entry_id = entry.get("entryId", "")
                        if entry_id.startswith("tweet-"):
                            tweets.append(entry)
                        elif entry_id.startswith("cursor-bottom-"):
                            # 获取 cursor 的值
                            new_cursor = entry.get("content", {}).get("value")
            print(f"本页获取到 {len(tweets)} 条 tweet，cursor: {new_cursor}")
        except Exception as e:
            print("解析点赞数据失败:", e)
            break

        all_tweets.extend(tweets)

        # 如果未启用 ALL 模式，则只返回第一页数据
        if not config.ALL:
            break

        # 如果没有新的 cursor 或新 cursor 与上一次相同，则认为没有更多数据
        if not new_cursor or new_cursor == cursor:
            break
        cursor = new_cursor

    return all_tweets
