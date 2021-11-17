import json
import requests
from urllib.parse import urlparse, unquote
from requests.cookies import RequestsCookieJar
from requests.structures import CaseInsensitiveDict

from . import ALWAYS_ECHO_RESULT, logger


def parser_cookies_by_headers(headers: CaseInsensitiveDict):
    cookies = RequestsCookieJar()
    cookie_str = headers.get("Cookie")
    if cookie_str:
        for cookie in cookie_str.strip().split(";"):
            key, value = cookie.strip().split("=")
            cookies.set(key.strip(), value.strip())
    return cookies


def check_response(
    response: requests.Response, operate=r"请求", ignore_error=True
) -> bool:
    """检查response是否成功"""
    if response.status_code == 200:
        content_type = response.headers.get("content-type")
        if content_type and "json" in content_type:
            operate = operate.split("\n")[0]
            if response.json().get("code") == 0:
                status = True
            elif response.json().get("success"):
                status = True
            else:
                msg = f"【{operate}】失败，错误详情：{response.text}"
                if ignore_error:
                    status = False
                    logger.error(msg)
                else:
                    format_output(response, level="error")
                    raise ValueError(msg)

            # 根据请求结果与调试标志输出
            if not status or ALWAYS_ECHO_RESULT:
                if status:
                    level = "debug"
                else:
                    level = "error"
                format_output(response, level=level)
            return status
        else:
            return True
    else:
        if ignore_error:
            format_output(response, level="warning")
            return False
        else:
            format_output(response, level="error")
            raise ValueError(response.text)


def format_output(obj, level="debug"):
    _logger = getattr(logger, level)
    if isinstance(obj, (dict, list, tuple)):
        _logger(json.dumps(obj, ensure_ascii=False, indent=4))
    elif isinstance(obj, requests.Response):
        _logger(f"请求地址：{obj.request.method}, {obj.request.url}")
        _logger(
            f"请求头部：{json.dumps(dict(obj.request.headers), ensure_ascii=False, indent=4)}"
        )
        if obj.request.body:
            if obj.request.headers.get(
                "Content-Type"
            ) and "application/json" in obj.request.headers.get("Content-Type"):
                if isinstance(obj.request.body, bytes):
                    body = json.loads(obj.request.body.decode("utf-8"))
                else:
                    body = json.loads(obj.request.body)
                _logger(f"请求内容：{json.dumps(body, ensure_ascii=False, indent=4)}")
            else:
                if isinstance(obj.request.body, bytes):
                    _logger(f"请求内容：{obj.request.body.decode('utf-8')}")
                else:
                    _logger(f"请求内容：{obj.request.body}")
        _logger(f"响应首行：{obj.status_code}, {obj.reason}, {obj.url}, 耗时：{obj.elapsed}")
        _logger(f"响应头部：{json.dumps(dict(obj.headers), ensure_ascii=False, indent=4)}")
        if obj.text.strip():
            if obj.headers.get(
                "Content-Type"
            ) and "application/json" in obj.headers.get("Content-Type"):
                _logger(f"响应内容：{json.dumps(obj.json(), ensure_ascii=False, indent=4)}")
            else:
                _logger(f"响应内容：{obj.text}")
    else:
        _logger(obj)


def clean_null_key_for_dict(my_dict: dict):
    """将字典中第一层的空值清除"""
    if isinstance(my_dict, dict):
        for key, value in list(my_dict.items()):
            if value is None:
                my_dict.pop(key)
    return my_dict


def parse_url_to_dict(url: str, _all=True, unquote_count: int = 0) -> dict:
    for _ in range(unquote_count):
        url = unquote(url)
    url_obj = urlparse(url)
    query_str = url_obj.query
    url_dict = {item.split("=")[0]: item.split("=")[1] for item in query_str.split("&")}
    if _all:
        url_dict["scheme"] = url_obj.scheme
        url_dict["netloc"] = url_obj.netloc
        url_dict["path"] = url_obj.path
        url_dict["fragment"] = url_obj.fragment
    return url_dict


def pop_key_from_dict(my_dict: dict, key, default=None):
    if key in my_dict:
        value = my_dict.pop(key)
    else:
        value = default
    return value


def query_str_to_dict(_str: str):
    """将URL查询字符串转换成dict"""
    _str = unquote(_str)
    items = _str.split("&")
    payload = {}
    for item in items:
        try:
            key, values = item.split("=")
        except ValueError as e:
            logger.warning("拆包时出现异常，可能是字符串中存在多个【=】导致，启用备用方案拆包：忽略第2个及以后的【=】字符")
            logger.warning("原始字符串：{}".format(item))
            key, values = item.split("=", 1)
        payload[key] = values
    return payload
