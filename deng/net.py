import re
import socket
import logging
from urllib.parse import urlparse


logger = logging.getLogger("DengUtils")


def get_host_ip(reference: str = None) -> str:
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

