# coding = utf-8
import os
import json
import hashlib
from pathlib import Path
from typing import Union
from redis import Redis, ConnectionPool

from . import logger
from .encrypt import to_decode
from .file import read_file_content, save_json_to_file


def get_cache_obj():
    """获取缓存对象"""
    try:
        _redis = MyRedis(db_index=15)
    except Exception as _e:
        logger.exception(_e)
        logger.warning(f"redis缓存不可用，启动本地文件缓存！")
        return MyCache(Path(__file__).parent / "MyCookie.cache")
    else:
        logger.info(f"redis缓存初始成功！")
        return _redis


def get_redis_pool(db_index=0, max_connections=None):
    """获取redis连接池"""
    _connect = json.loads(to_decode(os.environ.get("REDIS_DB_CONNECT")))
    return ConnectionPool(
        host=_connect["host"],
        port=_connect["port"],
        password=_connect["pass"],
        db=db_index,
        max_connections=max_connections,
    )


def sum_md5(paramstr: str) -> str:
    """计算字符串MD5值"""
    if isinstance(paramstr, int):
        paramstr = str(paramstr)
    _hash = hashlib.md5()
    _hash.update(paramstr.encode("UTF-8"))
    return _hash.hexdigest()


def get_redis_handler(db_index=0):
    """获取redis连接"""
    redis_obj = Redis(connection_pool=get_redis_pool(db_index))
    if redis_obj.ping():
        return redis_obj
    else:
        return None


def clearup_temp_lock(name_expression):
    redis = get_redis_handler()
    temp_lock_list = redis.keys(name_expression)
    if len(temp_lock_list) > 0:
        redis.delete(*temp_lock_list)


class MyRedis(Redis):
    def __init__(self, db_index=0):
        super().__init__(connection_pool=get_redis_pool(db_index))

    def batch_delete(self, name_expression):
        temp_lock_list = self.keys(name_expression)
        if len(temp_lock_list) > 0:
            self.delete(*temp_lock_list)

    def get_to_json(self, name):
        if name:
            value_raw = self.get(name)
            if value_raw:
                try:
                    user = json.loads(value_raw)
                except (TypeError, json.decoder.JSONDecodeError) as e:
                    self.delete(name)
                else:
                    return MyDict(**user)
        return None

    def push_obj(self, queue_name: str, value):
        if isinstance(value, (dict, list, tuple)):
            value = json.dumps(value, ensure_ascii=False)
            return self.rpush(queue_name, value)
        else:
            return self.rpush(queue_name, value)

    def pop_obj(self, queue_name: str):
        value = self.lpop(queue_name)
        try:
            return json.loads(value)
        except Exception as e:
            return value

    def hgetall(self, _k):
        _v = super(MyRedis, self).hgetall(_k)
        if isinstance(_v, dict):
            return {
                _k.decode("utf-8"): _v.decode("utf-8")
                for _k, _v in _v.items()
            }
        else:
            return _v

    def lpop(self, name):
        _k = super(MyRedis, self).lpop(name)
        if _k:
            return _k.decode("utf-8")
        else:
            return _k

    def keys(self, pattern='*'):
        _l = super(MyRedis, self).keys(pattern)
        if _l:
            return [_i.decode("utf-8") for _i in _l]
        else:
            return _l

    def get(self, name):
        _v = super(MyRedis, self).get(name)
        if _v:
            _v = _v.decode("utf-8")
        return _v


class MyCache(object):
    """自定义缓存类，redis不可用时替代使用"""

    def __init__(self, cache_path: Union[Path, str]):
        self._dict = dict()
        self.cache_path = Path(cache_path)
        if self.cache_path.exists():
            cache = read_file_content(self.cache_path, encoding="utf-8", _return="json")
            if isinstance(cache, dict):
                self._dict.update(cache)
            else:
                raise ValueError(f"缓存文件内容格式错误，无法转换成python dict对象：{self.cache_path}")
        else:
            self.cache_path.touch()

    def save_cache(self):
        save_json_to_file(self._dict, self.cache_path)

    def exists(self, key: str):
        return key in self._dict

    def get(self, key: str):
        return self._dict.get(key)

    def delete(self, key: str):
        if key in self._dict:
            self._dict.pop(key)
            self.save_cache()

    def set(self, key: str, value):
        self._dict[key] = value
        self.save_cache()

    def setex(self, key, time, value):
        self._dict[key] = value
        self.save_cache()

    def hmset(self, key: str, value):
        self.set(key, value)

    def hgetall(self, key: str):
        return self.get(key)


class MyDict(dict):
    """自定义的字典类"""

    def __init__(self, *args, **kwargs):
        super(MyDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self[item]

    def __delattr__(self, item):
        del self[item]

    def __setattr__(self, key, value):
        self[key] = value
