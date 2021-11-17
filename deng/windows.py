import os
import json
import time
import ctypes
import logging
from pathlib import Path

from .utils import execute_cmd, byte_to_str


logger = logging.getLogger("DengUtils")
__system_path = Path(os.environ["TEMP"]) / "system_info.json"


def get_system_info() -> dict:
    """获取系统信息"""
    _system_info: dict
    if __system_path.exists():
        with open(__system_path, encoding="utf-8") as _file:
            try:
                _system_info = json.load(_file)
            except Exception as e:
                logger.exception(e)
                logger.warning(f"读取缓存出错，重新计算：{str(e)}")
            else:
                for _key, _value in _system_info.items():
                    if not _value:
                        logger.warning(f"缓存信息不完整，重新计算：{_system_info}")
                        break
                else:
                    timestamp = _system_info.pop("timestamp")
                    if int(time.time()) - timestamp <= 1 * 24 * 60 * 60:
                        logger.debug(
                            f"系统信息缓存未过期：{json.dumps(_system_info, ensure_ascii=False, indent=4)}"
                        )
                        return _system_info
                    else:
                        logger.info(f"缓存过期，重新获取")

    # 实时获取系统信息
    systems = {
        "host_name": "",
        "os_name": "",
        "os_version": "",
        "os_arch": "",
        "ip_address": "",
        "mac_address": "",
    }
    try:
        res = execute_cmd(["systemInfo"], encoding=None, level=None)
        system_info = byte_to_str(res.stdout)
        for line in system_info.split("\n"):
            line = line.strip()
            if (
                line.startswith("主机名:")
                or line.startswith("主機名稱:")
                or line.startswith("Host Name:")
            ):
                systems["host_name"] = line.split(":")[-1].strip()
            elif (
                line.startswith("OS 名称:")
                or line.startswith("作業系統名稱:")
                or line.startswith("OS Name:")
            ):
                systems["os_name"] = line.split(":")[-1].strip()
            elif (
                line.startswith("OS 版本:")
                or line.startswith("作業系統版本:")
                or line.startswith("OS Version:")
            ):
                systems["os_version"] = line.split(":")[-1].strip()
            elif (
                line.startswith("系统类型:")
                or line.startswith("系統類型:")
                or line.startswith("System Type:")
            ):
                systems["os_arch"] = line.split(":")[-1].strip()
        try:
            from . import net as net_utils
        except ImportError:
            import net as net_utils
        systems["ip_address"] = net_utils.get_host_ip()
        systems["mac_address"] = get_mac_address(systems["ip_address"])
        logger.info(f"当前机器系统信息：{json.dumps(systems, ensure_ascii=False, indent=4)}")
        with open(__system_path, mode="w", encoding="utf-8") as _file:
            _temp = systems
            _temp["timestamp"] = int(time.time())
            json.dump(_temp, _file, ensure_ascii=False, indent=4)
        return systems
    except Exception as e:
        logger.exception(e)
        return systems


def get_mac_address(ip_address: str) -> str:
    """根据IP地址获取网卡MAC地址，兼容中文简体、中文繁体、英文"""
    mac_address: str = ""
    try:
        res = execute_cmd(["ipconfig", "/all"], encoding=None, level=None)
        network_info = byte_to_str(res.stdout)
        for _line in network_info.split("\n"):
            _line = _line.strip()
            if _line:
                if (
                    _line.startswith("Physical Address")
                    or _line.startswith("物理地址")
                    or _line.startswith("實體位址")
                ):
                    mac_address = _line.split(":")[-1].strip()
                elif (
                    _line.startswith("IPv4 Address")
                    or _line.startswith("IPv4 地址")
                    or _line.startswith("IPv4 位址")
                ):
                    if ip_address in _line:
                        return mac_address
            else:
                # 切换网卡、重置mac
                mac_address = ""
    except Exception as e:
        logger.exception(e)

    return ""


def is_running_as_admin() -> bool:
    """检查当前是否以管理员权限运行"""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:
        return False


if __name__ == "__main__":
    print(get_system_info())
