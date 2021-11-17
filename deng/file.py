import os
import re
import json
import time
import stat
import shutil
import tarfile
import zipfile
import logging
import datetime
from pathlib import Path
from typing import Union


logger = logging.getLogger("DengUtils")


def check_path_is_exits(src_path: Union[str, Path], path_type=None):
    """检查目录或文件是否存在
    :param src_path: 源路径
    :param path_type: 源路径类型，可选值：file/dir
    """
    if isinstance(src_path, str):
        src_path = Path(src_path)

    if not src_path.exists():
        raise FileNotFoundError(f"目录或文件不存在：{src_path}")

    if path_type and path_type.lower() not in ("file", "dir"):
        raise ValueError("参数path_type非法，可选值有：file/dir")

    if path_type and path_type.lower() == "file":
        if not src_path.is_file():
            raise FileNotFoundError(f"{src_path}不是有效的文件！")

    if path_type and path_type.lower() == "dir":
        if not src_path.is_dir():
            raise FileNotFoundError(f"{src_path}不是有效的目录！")


def ensure_empty_dir(target: Union[str, Path], mkdir=True, parents=True) -> None:
    """确保目录为空目录
    :param target: 目标目录路径
    :param mkdir: bool, 目标目录不存在时自动创建
    :param parents: bool, 是否递归创建目录
    """
    if isinstance(target, str):
        target = Path(target)

    # 删除目录时，时常报拒绝访问的错误，增加重试次数
    for _ in range(10):
        try:
            if target.exists():
                if target.is_dir() and len(os.listdir(str(target))) == 0:
                    logger.info(f"已经是空目录：{target}")
                else:
                    if target.is_dir():
                        shutil.rmtree(target, ignore_errors=False)
                        logger.info(f"删除非空目录成功：{target}")
                    else:
                        target.unlink()
                        logger.info(f"删除文件成功：{target}")
                    # 防止报错，有时rmtree删除命令返回成功，但目录并还没有被删除完成，直接创建目录会报错
                    time.sleep(2)
                    if mkdir:
                        target.mkdir(parents)
                        logger.info(f"创建目录成功：{target}")
            else:
                if mkdir:
                    target.mkdir(parents)
                    logger.info(f"创建目录成功：{target}")
        except Exception as e:
            time.sleep(1)
        else:
            break
    else:
        raise ValueError(f"删除目录出错：{target}")


def compress_zip(src_path: str, compress_abs_path: str) -> None:
    """压缩zip文件
    :param src_path: 待压缩文件或目录路径
    :param compress_abs_path: 压缩包输出绝对路径
    """
    with zipfile.ZipFile(compress_abs_path, "w", zipfile.ZIP_DEFLATED) as compress_file:
        for abs_dir_path, dir_list, file_list in os.walk(src_path):
            relative_path = abs_dir_path.replace(src_path, "")
            relative_path = (relative_path and relative_path + os.sep) or ""
            for filename in file_list:
                compress_file.write(
                    os.path.join(abs_dir_path, filename), relative_path + filename
                )


def extract_zip(src_zip: str, dst_dir: str) -> None:
    """解压zip文件
    :param src_zip: 待解压压缩包路径
    :param dst_dir: 解压目的路径
    """
    # zip文件不存在时报错
    check_path_is_exits(src_zip, path_type="file")

    # 解压目录不存在时新建
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    if zipfile.is_zipfile(src_zip):
        fz = zipfile.ZipFile(src_zip, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        raise ValueError(f"{src_zip}不是一个有效的zip文件")


def compress_tgz(source_files, compress_name):
    """将源文件打包成tar.gz格式
    :param source_files：str, 源文件路径，传入相对路径时，压缩包中也为相当路径，为绝对路径时，压缩包中同样为绝对路径
    :param compress_name: str, 生成的压缩包路径
    """
    tar = tarfile.open(compress_name, "w:gz")

    for root, _dir, files in os.walk(source_files):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath)
    tar.close()


def uncompress_tgz(compress_file, target_path="."):
    """解压tar.gz格式文件
    :param compress_file: str, 压缩包路径
    :param target_path: str, 解压后存储路径
    """
    tar = tarfile.open(compress_file)
    names = tar.getnames()
    for name in names:
        tar.extract(name, path=target_path)
    tar.close()


def rm(src_path: Union[str, Path], *args, **kwargs):
    """删除文件或目录
    :param src_path: str, 源文件或目录路径
    """
    check_path_is_exits(src_path)

    # 统一转换成Path处理
    if isinstance(src_path, str):
        src_path = Path(src_path)

    if src_path.is_file():
        src_path.unlink()
    else:
        shutil.rmtree(str(src_path), onerror=rm_readonly)

    logger.info(f"删除成功：{src_path}")


def rm_readonly(fn, tmp, info):
    """删除只读文件"""
    os.chmod(tmp, stat.S_IWRITE)
    if os.path.isfile(tmp):
        os.remove(tmp)
    elif os.path.isdir(tmp):
        shutil.rmtree(tmp)


def move_to_dir(
    src_path: Union[str, Path], dst_path: Union[str, Path], *args, **kwargs
):
    """移动文件
    :param src_path: str or Path, 源文件或目录路径
    :param dst_path: str or Path, 目标文件或目录路径
    """
    src_path = Path(src_path)
    dst_path = Path(dst_path)

    check_path_is_exits(src_path)
    if not dst_path.exists():
        dst_path.mkdir(parents=True)
    shutil.move(str(src_path), str(dst_path))


def copy_to_target(
    src_path: Union[str, Path], dst_path: Union[str, Path], *args, **kwargs
):
    """复制文件或目标到目标路径
    :param src_path: str, 源文件或目录路径，不支持正则表达式；
    :param dst_path: str, 目标字符串路径；
    """
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    check_path_is_exits(src_path)

    if not dst_path.parent.exists():
        dst_path.parent.mkdir(parents=True)

    # 当源对象为文件时
    if src_path.is_file():
        shutil.copy2(str(src_path), str(dst_path))

    # 当源对象为目录时
    if src_path.is_dir():
        if dst_path.exists():
            # 将目录复制到已经存在的目录下
            shutil.copytree(str(src_path), str(dst_path / src_path.name))
        else:
            # 复制源目标生成指定的新目录
            shutil.copytree(str(src_path), str(dst_path))
            return


def copy_to_target_by_pattern(
    src_path: Union[str, Path],
    dst_path: Union[str, Path],
    recursion: bool = True,
    excludes: str = "",
):
    """通过表达式复制文件或目标到目标路径
    :param src_path: str, 源文件或目录路径，支持正则表达式；
    :param dst_path: str, 目标字符串路径；
    :param recursion: bool, 递归子目录；
    :param excludes: str, 排除表达式，排除单个目录如："x86"，同时排除多个目录用分号分隔如"x86;x64"；
    """
    src_path = str(src_path)
    dst_path = str(dst_path)
    # 两种情况，表达式与绝对路径
    if os.path.exists(src_path):
        # 绝对路径
        pattern = r".+"
    else:
        # 表达式
        last_sep_index = src_path.rfind(os.sep)
        pattern = src_path[last_sep_index + 1 :]
        src_path = src_path[:last_sep_index]
    # 排除项表达式
    if excludes:
        excludes = excludes.split(";")
    else:
        excludes = []

    # 遍历源目录
    for child in os.listdir(src_path):
        # 跳过子目录
        if not recursion and os.path.isdir(src_path + os.sep + child):
            continue

        # 判断是否为排除的项
        is_exclude = False
        for _p in excludes:
            if _p and re.match(_p, child, re.I):
                is_exclude = True
                break
        if is_exclude:
            continue

        # 判断是否为匹配的项
        if re.match(pattern, child, re.I):
            copy_to_target(src_path + os.sep + child, dst_path)


def read_file_stream(file_path: str, start_index, end_index):
    """读取文件流"""
    check_path_is_exits(file_path, path_type="file")
    with open(file_path, mode="rb") as _file:
        _file.seek(start_index)
        return _file.read(end_index - start_index)


def read_file_raw_content(file_path: Union[str, Path], encoding=None) -> tuple:
    """读取文件内容"""
    check_path_is_exits(file_path)
    file_path = Path(file_path)

    if encoding:
        encoding_list = [encoding]
    else:
        encoding_list = ["utf-8", "GBK", "GB2312", "GB18030"]

    error = None
    for encoding in encoding_list:
        try:
            with open(file_path, encoding=encoding) as _file:
                return _file.read(), encoding
        except Exception as e:
            error = e
    else:
        raise error


def read_file_content(file_path: Union[Path, str], encoding=None, _return=None, default=None):
    """读取文件内容"""
    if default is None:
        default = {}
    _raw_content, _ = read_file_raw_content(file_path, encoding)
    if _return and _return.lower() == "json":
        _raw_content = _raw_content.strip()
        if _raw_content:
            return json.loads(_raw_content)
        else:
            return default
    else:
        return _raw_content


def save_obj_to_file(obj, file_abs_path: str, exist_ok=True):
    """保存对象到文件"""
    if isinstance(obj, (dict, list, tuple)):
        return save_json_to_file(obj, file_abs_path, exist_ok)

    if isinstance(obj, bytes):
        obj = obj.decode("utf-8")
    else:
        obj = str(obj)

    with open(file_abs_path, mode="w", encoding="utf-8") as _file:
        return _file.write(obj)


def save_json_to_file(
    content: dict or list or tuple,
    file_abs_path: Union[Path, str],
    exist_ok=True,
    encoding="utf-8",
):
    """将字典、列表、元组保存到文件中"""
    file_abs_path = Path(file_abs_path)
    if not exist_ok:
        if file_abs_path.exists():
            raise FileExistsError(f"文件已经存在：{file_abs_path}")

    if not file_abs_path.parent.exists():
        file_abs_path.parent.mkdir(parents=True)

    with open(file_abs_path, mode="w", encoding=encoding) as _file:
        return json.dump(content, _file, ensure_ascii=False, indent=2)


def get_newest_file(target: str, _type: str = "c"):
    """获取目录下最新的文件
    :param target: str，目标目录；
    :param _type: str，类型，c按创建时间，m按修改时间，a按访问时间
    """
    if _type.lower() not in ("c", "m", "a"):
        raise ValueError(f"_type参数非法，正确的取值为：a,m,c")
    else:
        _method = getattr(os.path, f"get{_type}time")

    if os.path.isdir(target):
        file_list = os.listdir(target)
        file_list.sort(key=lambda _file: _method(target + os.sep + _file))
        return target + os.sep + file_list[-1]


def get_file_time(file_path: Union[Path, str], _type: str = "c", _return=None):
    """根据文件修改日期获取插件版本号"""
    file_path = Path(file_path)
    if _type.lower() not in ("c", "m", "a"):
        raise ValueError(f"_type参数非法，正确的取值为：a,m,c")
    else:
        _method = getattr(file_path.stat(), f"st_{_type}time")
        _time_obj = datetime.datetime.fromtimestamp(_method)
        if _return == datetime.datetime:
            return _time_obj
        elif _return == datetime.date:
            return _time_obj.date()
        elif _return == float:
            return _time_obj.timestamp()
        elif _return == int:
            return round(_time_obj.timestamp())
        else:
            return _time_obj.strftime("%Y-%m-%d %H:%M:%S")
