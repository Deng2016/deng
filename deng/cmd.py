import logging
import subprocess
from typing import Sequence


logger = logging.getLogger("DengUtils")


class ExecuteCMDException(Exception):
    """执行外部命令异常"""

    pass


def bytes_to_str(src, *, encoding=None):
    if isinstance(src, bytes):
        error_list = []
        for encoding in ("utf-8", "GBK"):
            try:
                return str(src, encoding=encoding).strip()
            except UnicodeDecodeError as e:
                error_list.append(e)
        for error in error_list:
            logger.exception(error)
            logger.warning(f"bytes转换成str出错：{src}")
    return src


def execute_cmd(
    *popenargs,
    input=None,
    capture_output=True,
    timeout=None,
    check=False,
    level="debug",
    encoding="utf-8",
    **kwargs,
):
    kwargs["input"] = input
    kwargs["capture_output"] = capture_output
    kwargs["timeout"] = timeout
    kwargs["check"] = check
    if encoding:
        kwargs["encoding"] = encoding
    if isinstance(popenargs, Sequence):
        if isinstance(popenargs[0], str):
            cmd_text = popenargs[0]
        elif isinstance(popenargs[0], Sequence):
            cmd_text = " ".join(popenargs[0])
        else:
            raise ValueError(f"参数遇到未知情况：{popenargs}")
    else:
        raise ValueError(f"参数遇到未知情况：{popenargs}")

    if level:
        getattr(logger, level)(f"执行命令：{cmd_text}")
    _res = subprocess.run(*popenargs, **kwargs)
    if _res.returncode == 0:
        if _res.stdout:
            if level:
                getattr(logger, level)(_res.stdout)
        return _res
    else:
        error_outout = bytes_to_str(_res.stderr or _res.stdout)
        error_msg = f"执行命令出错：{cmd_text}\n{error_outout}"
        logger.error(error_msg)
        raise ExecuteCMDException(error_msg)


def check_shell_run_result(res_code, desc=""):
    """检查结果，非0时报错"""
    if res_code == 0:
        return True
    else:
        raise ExecuteCMDException(f"{desc}命令执行失败，返回结果={res_code}")
