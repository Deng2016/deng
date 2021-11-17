import time
import math
import datetime


def get_timestamp(length: int = 10, utc=False) -> int:
    """��ȡϵͳʱ��ʱ���"""
    assert length in (10, 13), "ʱ������Ȳ�������ֻ��10λ��13λʱ���"
    if utc:
        current_timestamp = datetime.datetime.utcnow().timestamp()
    else:
        current_timestamp = datetime.datetime.now().timestamp()
    return int(str(current_timestamp * 1000)[:length])


def get_current_time(_format: str = "long", offset: int = 0):
    if not isinstance(offset, int):
        raise ValueError(f"offset�����Ƿ���Ԥ��Ϊint���ͣ�ʵ��Ϊ{type(offset)}")

    # ��ȡ��ǰʱ��
    part2, part1 = math.modf(time.time())
    part1 = time.localtime(part1 - offset)
    if _format.lower() == "short":
        return time.strftime("%Y-%m-%d", part1)
    else:
        _temp = time.strftime("%Y-%m-%d %H:%M:%S", part1)
        if _format.lower() == "super":
            return _temp + str(part2)[1:8]
        else:
            return _temp


def str_to_time(time_str: str, _format="long"):
    if not time_str:
        raise ValueError(f"time_str�����Ƿ���{time_str}")

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
