import os

from dotenv import load_dotenv

# 加载项目根目录下的 .env 文件
load_dotenv()


def load_private_tokens(filename="data/private_tokens.env"):
    tokens = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    tokens[key] = value
    else:
        raise FileNotFoundError(f"{filename} 不存在，请先运行 src/setup.py 初始化。")
    return tokens


private_tokens = load_private_tokens("data/private_tokens.env")

# 从 private_tokens.env 中加载
USER_ID = private_tokens["USER_ID"]
BEARER_TOKEN = private_tokens["BEARER_TOKEN"]
AUTH_TOKEN = private_tokens["AUTH_TOKEN"]
CT0 = private_tokens["CT0"]
PERSONALIZATION_ID = private_tokens["PERSONALIZATION_ID"]

# MOCK 模式开关及 Mock 数据存储文件
MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() in ("true", "1", "yes")
MOCK_LIKED_TWEETS_FILE = os.getenv("MOCK_LIKED_TWEETS_FILE", "data/mock/mock_liked_tweets.json")

# 查询tweet数量
COUNT = os.getenv("COUNT", "20")
# 下载全部tweet
ALL = os.getenv("ALL", "False").lower() in ("true", "1", "yes")

# 下载媒体的基础目录
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "data/downloads")

# 下载记录文件，保存已处理 tweet 的 ID，避免重复下载
DOWNLOAD_RECORD = os.getenv("DOWNLOAD_RECORD", "data/downloaded_tweet_ids.txt")

# 文件命名格式（例如使用 {USERNAME} 作为模板变量）
FILE_FORMAT = os.getenv("FILE_FORMAT", "{USERNAME} {ID}")

# 自动整理目录开关（True 表示自动整理，False 表示不整理）
AUTO_ORGANIZE = os.getenv("AUTO_ORGANIZE", "False").lower() in ("true", "1", "yes")

# 目标路径，用于整理归类下载的文件，默认目标目录为 "data/organized"
TARGET_DIR = os.getenv("TARGET_DIR", "data/organized")

# 代理设置：ENABLE_PROXY 为开关，若为 True 则使用代理
ENABLE_PROXY = os.getenv("ENABLE_PROXY", "True").lower() in ("true", "1", "yes")

# 分别配置 HTTP 和 SOCKS5 代理
HTTP_PROXY = os.getenv("HTTP_PROXY", "http://127.0.0.1:7890")
SOCKS_PROXY = os.getenv("SOCKS_PROXY", "socks5://127.0.0.1:7891")

# 内部 API 的配置
LIKES_API_URL = os.getenv("LIKES_API_URL", "https://x.com/i/api/graphql/nWpDa3j6UoobbTNcFu_Uog/Likes")
LIKES_FEATURES = os.getenv("LIKES_FEATURES",
                           '{"rweb_video_screen_enabled":false,"profile_label_improvements_pcf_label_in_post_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":true,"responsive_web_jetfuel_frame":false,"responsive_web_grok_share_attachment_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"responsive_web_grok_analysis_button_from_backend":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_grok_image_annotation_enabled":false,"responsive_web_enhance_cards_enabled":false}')
LIKES_FIELDTOGGLES = os.getenv("LIKES_FIELDTOGGLES", '{"withArticlePlainText":false}')
