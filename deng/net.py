import re
import socket
import logging
import requests
from pathlib import Path
from contextlib import closing
from urllib.parse import urlparse


logger = logging.getLogger("DengUtils")


def get_host_ip(reference: str = "") -> str:
    """获取主机ip地址
    :param reference: str, 参考地址，本地可能存在多个IP，获取能够访问此地址的IP
    """
    # 支持http或https地址，从中提取域名/主机地址
    absolute_http_url_regexp = re.compile(r"^https?://", re.I)
    if absolute_http_url_regexp.match(reference):
        url_obj = urlparse(reference)
        reference = url_obj.netloc

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((reference if reference else "114.114.114.114", 80))
        ip = s.getsockname()[0]
        logger.debug(f"获取本机IP地址成功：{ip}")
    except Exception as e:
        logger.debug(e)
        logger.warning(f"获取本机IP地址失败")
        ip = ""
    finally:
        s.close()
    return ip


def is_valid_ip(ip):
    """Returns true if the given string is a well-formed IP address.
    Supports IPv4 and IPv6.
    """
    # IP地址必须是字符串
    if not isinstance(ip, str):
        return False

    if not ip or "\x00" in ip:
        # getaddrinfo resolves empty strings to localhost, and truncates
        # on zero bytes.
        return False

    try:
        res = socket.getaddrinfo(
            ip, 0, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_NUMERICHOST
        )
        return bool(res)
    except socket.gaierror as e:
        if e.args[0] == socket.EAI_NONAME:
            return False
        raise


def verify_download_url(url: str, timeout=3):
    """校验URL下载地址是否存在"""
    try:
        res = requests.head(url, timeout=timeout)
    except Exception as e:
        return False
    else:
        if res.status_code < 400:
            return True
        else:
            return False


def download_file(url: str, file_save_path: Path):
    """下载文件"""
    # 检查存储文件夹是否存在，不存在时创建
    if not file_save_path.parent.exists():
        file_save_path.parent.mkdir(parents=True)
    # 覆盖提醒
    if file_save_path.exists():
        logger.warning(f"目标文件已经存在，直接覆盖！")
    # 开始下载
    with closing(requests.get(url, stream=True)) as _res:
        with open(file_save_path, mode="wb") as _app:
            for chunk in _res.iter_content(chunk_size=10 * 1024 * 1024):
                if chunk:
                    _app.write(chunk)
    # 检查下载结果
    if file_save_path.exists():
        logger.info(f"下载成功，保存路径：{file_save_path}")
        return True
    else:
        raise FileNotFoundError(f"下载失败：{url}")
