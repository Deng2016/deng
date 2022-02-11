import sys
import logging
from typing import List


# 始终显示所有HTTP请求的详情
ALWAYS_ECHO_RESULT = False

log_format = logging.Formatter(
    "[%(asctime)s] %(filename)s/%(lineno)s/%(funcName)s/%(levelname)s: %(message)s"
)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.DEBUG)

logger = logging.getLogger("DengUtils")
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def configure_logger(level: int, handlers: List[logging.Handler]):
    """配置日志处理器
    :param level: int, 指定日志级别
    :param handlers: List[Handler], 日志处理器列表"""

    # 设置日志级别
    if level in (
        logging.NOTSET,
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.FATAL,
    ):
        logger.setLevel(level)
    else:
        raise ValueError(f"level参数非法：{level}")

    # 往日志句柄中添加处理器
    for handler in handlers:
        if isinstance(handler, logging.Handler):
            logger.addHandler(handler)
        else:
            raise TypeError(f"类型错误，预期为{logging.Handler}类型，实际为{type(handler)}类型")

    logger.info("日志配置完成")
