#!/usr/bin/env python
# coding:utf-8
"""
Created on 2016年1月28日
@author: dengqingyong
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
    """个人封闭的常用方法
        方法列表：
            format_print：格式化输出

    """

    @staticmethod    
    def format_print(res):
        """格式化输出
            格式化输出：字典、列表、Response对象
        """               
        if isinstance(res, Response):
            try:
                print "========请求体信息========"
                print "请求URL地址：%s" % res.request.url
                print "请求头："
                print res.request.headers
                print "请求体："
                if isinstance(res.request.body, (dict, list, tuple)):
                    print json.dumps(res.request.body, ensure_ascii=False, indent=4)
                # elif isinstance(res.request.body, str):
                #     try:
                #         print json.loads(res.request.body)
                #     except:
                #         print res.request.body
                else:
                    print res.request.body
                print "========响应体信息========"
                if res.status_code in range(200, 300):
                    print json.dumps(res.json(), ensure_ascii=False, indent=4)
                    print "长度：", len(res.json()), "返回码：", res.status_code, res.url
                else:
                    print "返回码：", res.status_code, res.url
                    print res.content 
            except Exception, e:
                print "返回码：", res.status_code, res.url
                print res.content
                print e
        elif isinstance(res, (tuple, list, dict, set)):
            if isinstance(res, set):
                res = list(res)
            try:
                print json.dumps(res, ensure_ascii=False, indent=4)
                print "长度：", len(res)
            except TypeError, e:
                print res
                print e
        elif isinstance(res, (str, unicode)):
            print res 
        elif isinstance(res, Element):
            print tostring(res)
        elif isinstance(res, CaseInsensitiveDict):
            print json.dumps(dict(res), ensure_ascii=False, indent=4)
        elif res is None:
            print "res对象为空！"
        else:
            print "非预期类型，对象类型为：", type(res)
            print res
    
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
            sorted(obj.iteritems(), key=lambda asd: asd[1], reverse=reverse)
        elif isinstance(obj, str):
            obj = "".join((lambda x: (x.sort(), x)[1])(list(obj)))
            if reverse:
                obj = obj[::-1]
        else:
            print "只能对字典、列表、字符串进行排序！"
        return obj 
    
    @staticmethod
    def time_format(ftime):
        return ftime.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def get_current_time(format=None):
        if format.lower() == "short":
            return time.strftime("%Y-%m-%d", time.localtime(time.time()))
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

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
    def get_params_dict(params, ignores=[]):
        """获取函数所有的参数，并以字典形式返回
        :param params: 函数中调用时通常传入locals()
        :param ignores: 忽略掉某些参数
        :return: 参数字典
        """
        if isinstance(ignores, str):
            ignores = [ignores]
        ignores.extend(["self", "cls", "args", "url"])

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
            num_str = raw_input("请输入一个有效数字：")
            if num_str.isdigit():
                num_int = int(num_str)
                if isinstance(params, (tuple, list)) and len(params) > 0:
                    if num_int in params:
                        break
                    else:
                        print "输入的不是一个有效选项！"
                else:
                    break
            else:
                print "输入的不是一个数字！"
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
