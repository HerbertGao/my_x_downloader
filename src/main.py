from config import AUTO_ORGANIZE, DOWNLOAD_DIR, TARGET_DIR
from downloader import load_downloaded_ids, save_downloaded_id, call_media_downloader
from x_api import get_liked_tweets_internal


def main():
    try:
        tweets = get_liked_tweets_internal()
    except Exception as e:
        print("获取点赞 tweets 失败：", e)
        return

    print(f"从 API 获取到 {len(tweets)} 条点赞的 tweet 数据")
    downloaded_ids = load_downloaded_ids()

    for entry in tweets:
        # 假设 tweet 数据结构中，rest_id 存储 tweet id
        tweet_data = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
        tweet = tweet_data.get("tweet", {})
        tweet_id = tweet.get("rest_id") or tweet_data.get("rest_id")
        if not tweet_id:
            continue
        if tweet_id in downloaded_ids:
            continue
        # 这里可以打印更多信息，比如 tweet 作者、文本等（视返回数据结构而定）
        print(f"处理 tweet: {tweet_id}")
        if call_media_downloader(tweet_id):
            save_downloaded_id(tweet_id)
    print("全部处理完成。")

    if AUTO_ORGANIZE:
        print("开始整理下载的文件目录...")
        from organize_files import organize_files
        organize_files(DOWNLOAD_DIR, TARGET_DIR)


if __name__ == "__main__":
    main()
