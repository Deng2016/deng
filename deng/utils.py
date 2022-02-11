"""工具函数，与打包逻辑无直接关联"""
# coding = utf-8
import os
import uuid
import json
import logging
import inspect
import datetime
import subprocess
from typing import Sequence
from pathlib import Path
from decimal import Decimal


logger = logging.getLogger("DengUtils")


class ExecuteCMDException(Exception):
    """执行外部命令异常"""

    pass


def pop_key_from_dict(my_dict: dict, key, default=None):
    if key in my_dict:
        value = my_dict.pop(key)
    else:
        value = default
    return value


def execute_cmd(
    *popenargs,
    input=None,
    capture_output=True,
    timeout=None,
    check=False,
    level="info",
    encoding="utf-8",
    **kwargs,
):
    """通过subprocess库执行命令行"""
    kwargs["input"] = input
    kwargs["capture_output"] = capture_output
    kwargs["timeout"] = timeout
    kwargs["check"] = check
    ignore_error_log = pop_key_from_dict(kwargs, "ignore_error_log", default=True)
    cmd_output_level = pop_key_from_dict(kwargs, "cmd_output_level", default=level)
    if encoding:
        kwargs["encoding"] = encoding
    if isinstance(popenargs, Sequence):
        if isinstance(popenargs[0], str):
            cmd_text = popenargs[0]
        elif isinstance(popenargs[0], Sequence):
            cmd_text = " ".join(popenargs[0])
        elif isinstance(popenargs[0], Path):
            cmd_text = popenargs[0].name
            kwargs["cwd"] = popenargs[0].parent
        else:
            raise ValueError(f"参数遇到未知情况：{popenargs}")
    else:
        raise ValueError(f"参数遇到未知情况：{popenargs}")

    if level:
        getattr(logger, level)(f"执行命令：{cmd_text}")

    # 增加异常兼容逻辑，处理npm时的可能报错
    for run_count in range(2):
        try:
            _res = subprocess.run(*popenargs, **kwargs)
        except IndexError as e:
            if run_count == 0:
                logger.exception(e)
                logger.warning(f"运行报错，当前{capture_output=}，翻转capture_output参数，再次尝试运行……")
                kwargs["capture_output"] = not kwargs["capture_output"]
            else:
                error_msg = f"执行命令出错：{os.getcwd()} - {cmd_text}\n{str(e)}"
                if not ignore_error_log:
                    logger.error(error_msg)
                raise ExecuteCMDException(error_msg)
        except Exception as e:
            error_msg = f"执行命令出错：{os.getcwd()} - {cmd_text}\n{str(e)}"
            if not ignore_error_log:
                logger.error(error_msg)
            raise ExecuteCMDException(error_msg)
        else:
            if _res.returncode == 0:
                if _res.stdout and cmd_output_level:
                    # 有些命令如npm，会将警告信息打印在stderr中
                    output = f"{byte_to_str(_res.stderr)}\n{byte_to_str(_res.stdout)}"
                    getattr(logger, cmd_output_level)(output)
                return _res
            else:
                error_output = (
                    byte_to_str(_res.stderr) + "\n" + byte_to_str(_res.stdout)
                )
                error_msg = f"执行命令出错：{os.getcwd()} - {cmd_text}\n{error_output}"
                if not ignore_error_log:
                    logger.error(error_msg)
                raise ExecuteCMDException(error_msg)


def check_shell_run_result(res_code, desc=""):
    """检查结果，非0时报错"""
    if res_code == 0:
        return True
    else:
        raise ExecuteCMDException(f"{desc}命令执行失败，返回结果={res_code}")


def my_json_serializable(o):
    """补充标准库中json serializable逻辑"""
    if isinstance(o, datetime.datetime):
        return o.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, uuid.UUID):
        return str(o)
    if isinstance(o, Path):
        return str(o)
    if isinstance(o, Decimal):
        return float(o)
    if hasattr(o, "__html__"):
        return str(o.__html__())

    try:
        return str(o)
    except Exception:
        raise TypeError(
            f"Object of type {o.__class__.__name__} " f"is not JSON serializable"
        )


class MyJSONEncoder(json.encoder.JSONEncoder):
    """自定义JSON序列化类"""

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, uuid.UUID):
            return str(o)
        if hasattr(o, "__html__"):
            return str(o.__html__())
        raise TypeError(
            f"Object of type {o.__class__.__name__} " f"is not JSON serializable"
        )


def get_caller_info(level: int = 0) -> tuple:
    """获取调用方名称与描述"""
    # 获取调用方描述
    desc = inspect.stack()[level + 1].frame.f_code.co_consts[0]
    if desc:
        desc = desc.split("\n")[0].strip()
    func_name = inspect.stack()[level + 1].frame.f_code.co_name
    return func_name, desc


def byte_to_str(src, encoding=None):
    if isinstance(src, bytes):
        error_list = []
        encoding_list = ["utf-8", "GBK", "GB2312", "GB18030", "ISO-8859-1"]
        if encoding:
            # 已经存在时删除再插入到第一位，确保指定的编码第一个运行
            if encoding in encoding_list:
                encoding_list.remove(encoding)
            encoding_list.insert(encoding, 0)

        for encoding in encoding_list:
            try:
                return str(src, encoding=encoding).strip()
            except UnicodeDecodeError as e:
                error_list.append(e)
        if error_list:
            logger.warning(f"bytes转换成str时出错，尝试的编码有：{encoding_list}，原始对象：{src}")
    return src.strip() if isinstance(src, str) else src


def to_boolean(flag, default=False):
    """将字符串或数字转换成布尔型"""
    if isinstance(flag, bool):
        return flag
    elif flag is None or len(str(flag)) == 0:
        return default
    elif str(flag).lower() in ("false", "no", "0"):
        return False
    else:
        return True


def get_digit_from_input(params=None):
    """从键盘获取一个数字，并做规范性检查
    :param params: Union[List, Tuple],如果给出则输入的数字必须在params内。
    """
    while True:
        num_str = eval(input("请输入一个有效数字："))
        if num_str.isdigit():
            num_int = int(num_str)
            if isinstance(params, (tuple, list)) and len(params) > 0:
                if num_int in params:
                    break
                else:
                    print("输入的不是一个有效选项！")
            else:
                break
        else:
            print("输入的不是一个数字！")
    return num_int
