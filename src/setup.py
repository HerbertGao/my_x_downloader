import re
import json
import os
import sys
import urllib.parse

def parse_curl_command(curl_command):
    """
    从提供的 curl 命令中解析出：
      - BearerToken（从 header "authorization: Bearer ..." 中提取）
      - Cookie 字符串（从 -b 参数中提取）
    返回字典，包含 "bearer_token" 和 "cookie_str"
    """
    headers = re.findall(r"-H\s+'([^']+)'", curl_command)
    bearer_token = None
    for header in headers:
        if header.lower().startswith("authorization:"):
            m = re.search(r"Bearer\s+(\S+)", header, re.IGNORECASE)
            if m:
                bearer_token = m.group(1)
                break
    cookie_lines = re.findall(r"-b\s+'([^']+)'", curl_command)
    cookie_str = cookie_lines[0] if cookie_lines else None
    if not bearer_token or not cookie_str:
        raise ValueError("无法解析出 Bearer Token 或 Cookie 字符串，请检查输入的 curl 命令。")
    return {"bearer_token": bearer_token, "cookie_str": cookie_str}

def parse_cookies(cookie_str):
    """
    从 cookie 字符串中提取所需的字段：
      - twid（用户 ID，从中去除前缀 "u="，并 URL decode）
      - auth_token
      - ct0
      - personalization_id
    返回一个字典
    """
    cookies = {}
    parts = cookie_str.split(";")
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            cookies[key] = value

    required_keys = ["twid", "auth_token", "ct0", "personalization_id"]
    result = {}
    for key in required_keys:
        if key not in cookies:
            raise ValueError(f"Cookie 中缺少必需的字段: {key}")
        val = urllib.parse.unquote(cookies[key])
        if key == "twid" and val.startswith("u="):
            val = val[2:]
        result[key] = val
    return result

def save_twmd_cookies(cookies_dict, filename="twmd_cookies.json"):
    """
    根据 cookies_dict 生成符合格式要求的 JSON 文件
    格式示例如下：
    [
      {"Name":"auth_token","Value":"...","Quoted":false, ...},
      {"Name":"ct0","Value":"...","Quoted":false, ...},
      {"Name":"personalization_id","Value":"...","Quoted":true, ...}
    ]
    """
    cookie_list = [
        {
            "Name": "auth_token",
            "Value": cookies_dict["auth_token"],
            "Quoted": False,
            "Path": "",
            "Domain": "twitter.com",
            "Expires": "0001-01-01T00:00:00Z",
            "RawExpires": "",
            "MaxAge": 0,
            "Secure": False,
            "HttpOnly": False,
            "SameSite": 0,
            "Partitioned": False,
            "Raw": "",
            "Unparsed": None
        },
        {
            "Name": "ct0",
            "Value": cookies_dict["ct0"],
            "Quoted": False,
            "Path": "",
            "Domain": "twitter.com",
            "Expires": "0001-01-01T00:00:00Z",
            "RawExpires": "",
            "MaxAge": 0,
            "Secure": False,
            "HttpOnly": False,
            "SameSite": 0,
            "Partitioned": False,
            "Raw": "",
            "Unparsed": None
        },
        {
            "Name": "personalization_id",
            "Value": cookies_dict["personalization_id"],
            "Quoted": True,
            "Path": "",
            "Domain": "twitter.com",
            "Expires": "0001-01-01T00:00:00Z",
            "RawExpires": "",
            "MaxAge": 0,
            "Secure": False,
            "HttpOnly": False,
            "SameSite": 0,
            "Partitioned": False,
            "Raw": "",
            "Unparsed": None
        }
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cookie_list, f, separators=(",", ":"))
    print(f"生成 {filename} 成功！")

def save_private_tokens(user_id, bearer_token, auth_token, ct0, personalization_id, filename="data/private_tokens.env"):
    """
    将 USER_ID、BEARER_TOKEN、AUTH_TOKEN、CT0 和 PERSONALIZATION_ID 写入文件
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"USER_ID={user_id}\n")
        f.write(f"BEARER_TOKEN={bearer_token}\n")
        f.write(f"AUTH_TOKEN={auth_token}\n")
        f.write(f"CT0={ct0}\n")
        f.write(f"PERSONALIZATION_ID={personalization_id}\n")
    print(f"生成 {filename} 成功！")

def main():
    # 从文件中读取 curl 命令（方案1：通过文件重定向）
    curl_file = sys.argv[1] if len(sys.argv) > 1 else "curl_command.txt"
    try:
        with open(curl_file, "r", encoding="utf-8") as f:
            curl_command = f.read()
    except Exception as e:
        print(f"读取 {curl_file} 失败: {e}")
        return

    try:
        parsed = parse_curl_command(curl_command)
        bearer_token = parsed["bearer_token"]
        cookie_str = parsed["cookie_str"]
        cookies_parsed = parse_cookies(cookie_str)
    except Exception as e:
        print("解析失败:", e)
        return

    # 生成 twmd_cookies.json
    twmd_data = {
        "auth_token": cookies_parsed["auth_token"],
        "ct0": cookies_parsed["ct0"],
        "personalization_id": cookies_parsed["personalization_id"]
    }
    save_twmd_cookies(twmd_data, "twmd_cookies.json")
    # 生成 private_tokens 文件，保存全部敏感信息
    save_private_tokens(
        cookies_parsed["twid"],
        bearer_token,
        cookies_parsed["auth_token"],
        cookies_parsed["ct0"],
        cookies_parsed["personalization_id"],
        "data/private_tokens.env"
    )
    print("初始化完成。")

if __name__ == "__main__":
    main()