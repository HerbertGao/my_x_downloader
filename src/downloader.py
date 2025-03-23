import os
import subprocess

import requests

import config

DOWNLOAD_RECORD = config.DOWNLOAD_RECORD


def load_downloaded_ids():
    if os.path.exists(DOWNLOAD_RECORD):
        with open(DOWNLOAD_RECORD, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    return set()


def save_downloaded_id(tweet_id):
    os.makedirs(os.path.dirname(DOWNLOAD_RECORD), exist_ok=True)
    with open(DOWNLOAD_RECORD, "a", encoding="utf-8") as f:
        f.write(tweet_id + "\n")


def download_file(url, save_path):
    try:
        proxies = None
        if config.ENABLE_PROXY:
            proxies = {
                "http": config.SOCKS_PROXY,
                "https": config.SOCKS_PROXY
            }
            # print("媒体下载使用 SOCKS5 代理:", proxies)
        r = requests.get(url, stream=True, timeout=30, proxies=proxies)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"下载成功：{save_path}")
    except Exception as e:
        print(f"下载失败：{url}，错误：{e}")


def call_media_downloader(tweet_id, output_dir=None):
    """
    使用 twitter-media-downloader 工具下载指定 tweet 的媒体（视频和图片）。
    """
    if output_dir is None:
        output_dir = config.DOWNLOAD_DIR
    os.makedirs(output_dir, exist_ok=True)
    file_format = config.FILE_FORMAT if hasattr(config, "FILE_FORMAT") else "{USERNAME} {ID}"
    # 构造命令行调用
    cmd = [
        "./twitter-media-downloader",
        f"--tweet={tweet_id}",
        "--all",
        f"--output={output_dir}",
        f"--file-format={file_format}",
    ]
    # 使用 SOCKS5 代理下载媒体
    if config.ENABLE_PROXY:
        cmd.append(f"--proxy={config.SOCKS_PROXY}")
    cmd.append("--cookies")
    print("调用命令：", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("下载失败：", result.stderr)
        return False
    else:
        print("下载成功：", result.stdout)
        return True


if __name__ == "__main__":
    test_tweet_id = "1896117448191176953"
    output_dir = os.path.join(config.DOWNLOAD_DIR, "twitter", "example_user")
    if call_media_downloader(test_tweet_id, output_dir):
        print("处理完成")
    else:
        print("处理失败")
