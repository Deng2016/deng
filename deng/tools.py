#!/usr/bin/env python
# coding:utf-8
"""
Created on 2016年1月28日
@author: dengqingyong
@email: yu12377@163.com
"""
import os
import json 
import time
import random
import string
import tarfile
from dateutil.parser import parser
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from xml.etree.ElementTree import Element, tostring


class Tools(object):
    """个人封装的常用方法
        方法列表：
            format_print：格式化输出
    """

    @staticmethod    
    def format_print(res):
        """格式化输出
            格式化输出：字典、列表、Response对象
        """               
        if isinstance(res, Response):
            print("================请求体信息================")
            print("请求URL：{}".format(res.request.url))
            print("请求头：\n")
            Tools.format_print(res.request.headers)
            print("请求体：\n")
            Tools.format_print(res.request.body)
            print("================响应体信息================")
            print("返回码：{} URL: {}".format(res.status_code, res.url))
            print("响应头：\n")
            Tools.format_print(res.headers)
            print("响应体：\n")
            try:
                print(json.dumps(res.json(), ensure_ascii=False, indent=4))
            except ValueError as e:
                print(res.text)
        elif isinstance(res, (tuple, list, dict, set)):
            if isinstance(res, set):
                res = list(res)
            try:
                print(json.dumps(res, ensure_ascii=False, indent=4))
                print(u"长度：", len(res))
            except ValueError as e:
                print(res)
                print(e)
        elif isinstance(res, str):
            try:
                Tools.format_print(json.loads(res))
            except ValueError as e:
                print(res)
        elif isinstance(res, Element):
            print(tostring(res))
        elif isinstance(res, CaseInsensitiveDict):
            print(json.dumps(dict(res), ensure_ascii=False, indent=4))
        elif res is None:
            print("对象为空！")
        else:
            print("非预期类型，对象类型为：", type(res))
            print(res)
    
    @staticmethod        
    def sort_custom(obj, sort_column=None, reverse=False):
        """
        自定义排序：可对字典，列表，字符串进行排序
        """
        if isinstance(obj, list):
            if isinstance(obj[0], dict):
                obj = sorted(obj, key=lambda project: project[sort_column], reverse=reverse)
            else:
                obj.sort() 
        elif isinstance(obj, dict):
            sorted(iter(obj.items()), key=lambda asd: asd[1], reverse=reverse)
        elif isinstance(obj, str):
            obj = "".join((lambda x: (x.sort(), x)[1])(list(obj)))
            if reverse:
                obj = obj[::-1]
        else:
            print("只能对字典、列表、字符串进行排序！")
        return obj 
    
    @staticmethod
    def time_format(ftime):
        return ftime.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_timestamp(length=10, offset=0):
        if not isinstance(offset, int):
            offset = 0
        if length == 10:
            timestamp = round(time.time()) - offset
        else:
            timestamp = round(time.time() * 1000) - offset * 1000
        return timestamp

    @staticmethod
    def get_current_time(format="long", offset=0):
        if not isinstance(offset, int):
            offset = 0
        if format.lower() == "short":
            return time.strftime("%Y-%m-%d", time.localtime(time.time() - offset))
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - offset))

    @staticmethod
    def str_to_time(str_time):
        datetime_struct = parser(str_time)
        return datetime_struct

    @staticmethod
    def utc_to_bjtime(utctime):
        """
        把UTC时间转换为北京时间
        """
        pass
    
    @staticmethod
    def get_params_dict(params, ignores=None):
        """获取函数所有的参数，并以字典形式返回
        :param params: 函数中调用时通常传入locals()
        :param ignores: 忽略掉某些参数
        :return: 参数字典
        """
        if isinstance(ignores, str):
            ignores = [ignores]
        if ignores is None:
            ignores = []
        ignores.extend(["self", "cls", "args"])

        for keys_ in ignores:
            if keys_ in params:
                del params[keys_]

        if "kwargs" in params:
            temp_dict = params["kwargs"]
            del params["kwargs"]
            params = dict(params, **temp_dict)
        return params
    
    @staticmethod 
    def get_digit(params=None):
        """
        作用：从键盘获取一个数字，并做规范性检查
        参数：params列表或元组，为可选，如果给出，则输入的数字必须在params内。
        """
        while True:
            num_str = input("请输入一个有效数字：")
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

    @staticmethod
    def compress_tgz(sourc_files, compress_name):
        """将源文件打包成tar.gz格式
        sourc_files：传入相对路径时，压缩包中也为相当路径，为绝对路径时，压缩包中同样为绝对路径
        """
        tar = tarfile.open(compress_name, "w:gz")

        for root, dir, files in os.walk(sourc_files):
            for file in files:
                fullpath = os.path.join(root, file)
                tar.add(fullpath)
        tar.close()
    
    @staticmethod
    def uncompress_tgz(compress_file, target_path=None):
        """解压tar.gz格式文件"""
        tar = tarfile.open(compress_file)
        names = tar.getnames()
        for name in names:
            tar.extract(name, path=".")
        tar.close()

    @staticmethod
    def gen_phone_on():
        """生成随机手机号码"""
        phone_head = [130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                      150, 151, 152, 155, 158,
                      170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
                      181, 186, 187, 188, 189]
        phone_on = str(random.choice(phone_head)) + "".join(
            random.choice("0123456789") for i in range(8))
        return phone_on

    @staticmethod
    def gen_phone_serial_no():
        """生成手机串号"""
        serial_no = "".join(random.choice(string.ascii_uppercase) for i in range(4))
        serial_no += "-" + "".join(random.choice(string.ascii_uppercase) for i in range(4))
        serial_no += "-" + "".join(random.choice(string.digits) for i in range(5))
        return serial_no
