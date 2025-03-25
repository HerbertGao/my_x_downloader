import os
import subprocess
import platform

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

def get_twmd_tool_path():
    system = platform.system().lower()  # 获取操作系统类型
    arch = platform.architecture()[0]  # 获取操作系统架构

    # 判断操作系统类型和架构并返回对应的工具路径
    if system == "darwin":
        if arch == "64bit":
            return os.path.join("twmd", "twmd-darwin-amd64")
        elif arch == "arm64":
            return os.path.join("twmd", "twmd-darwin-arm64")
    elif system == "linux":
        if arch == "64bit":
            return os.path.join("twmd", "twmd-linux-amd64")
        elif arch == "arm64":
            return os.path.join("twmd", "twmd-linux-arm64")
    elif system == "windows":
        if arch == "64bit":
            return os.path.join("twmd", "twmd-windows-amd64.exe")
    else:
        raise Exception(f"不支持的操作系统：{system} {arch}")



def call_media_downloader(tweet_id, output_dir=None):
    """
    使用 twitter-media-downloader 工具下载指定 tweet 的媒体（视频和图片）。
    """
    if output_dir is None:
        output_dir = config.DOWNLOAD_DIR
    os.makedirs(output_dir, exist_ok=True)
    file_format = config.FILE_FORMAT if hasattr(config, "FILE_FORMAT") else "{USERNAME} {ID}"

    # 获取工具路径
    tool_path = get_twmd_tool_path()

    # 构造命令行调用
    cmd = [
        f"./{tool_path}",
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
