import time
import math
import datetime


def get_timestamp(length: int = 10, utc=False) -> int:
    """获取系统时间时间戳"""
    assert length in (10, 13), "时间戳长度参数错误，只有10位与13位时间戳"
    if utc:
        current_timestamp = datetime.datetime.utcnow().timestamp()
    else:
        current_timestamp = datetime.datetime.now().timestamp()
    return int(str(current_timestamp * 1000)[:length])


def get_current_time(
    _format: str = "long", offset: int = 0, sep1="-", sep2=":"
):
    if not isinstance(offset, int):
        raise ValueError(f"offset参数非法，预期为int类型，实际为{type(offset)}")

    # 获取当前时间
    part2, part1 = math.modf(time.time())
    part1 = time.localtime(part1 - offset)
    if _format.lower() == "short":
        return time.strftime(f"%Y{sep1}%m{sep1}%d", part1)
    else:
        _temp = time.strftime(
            f"%Y{sep1}%m{sep1}%d %H{sep2}%M{sep2}%S", part1
        )
        if _format.lower() == "super":
            return _temp + str(part2)[1:8]
        else:
            return _temp


def str_to_time(time_str: str, _format="long"):
    if not time_str:
        raise ValueError(f"time_str参数非法：{time_str}")

    if _format == "long":
        return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    else:
        day = datetime.datetime.strptime(time_str, "%Y-%m-%d")
        return day.date()


def time_to_str(_time: datetime.datetime, _format="long"):
    if _format == "long":
        return _time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return _time.strftime("%Y-%m-%d")
