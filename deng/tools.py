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
            try:
                print "========请求体信息========"
                print "请求URL地址：%s" % res.request.url
                print "请求头："
                print res.request.headers
                print "请求体："
                if isinstance(res.request.body, (dict, list, tuple)):
                    print json.dumps(res.request.body, ensure_ascii=False, indent=4)
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
    def get_timestamp(length=10):
        if length == 10:
            timestamp = round(time.time())
        else:
            timestamp = round(time.time() * 1000)
        return timestamp

    @staticmethod
    def get_current_time(_format="long"):
        if _format.lower() == "short":
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


class TestData(object):
    """生成测试数据
    """

    @staticmethod
    def get_name(gender=''):
        firstname = ''
        secondname = ''
        firstnames = u"""
            赵钱孙李，周吴郑王。
            冯陈褚卫，蒋沈韩杨。
            朱秦尤许，何吕施张。
            孔曹严华，金魏陶姜。
            戚谢邹喻，柏水窦章。
            云苏潘葛，奚范彭郎。
            鲁韦昌马，苗凤花方。
            俞任袁柳，酆鲍史唐。
            费廉岑薛，雷贺倪汤。
            滕殷罗毕，郝邬安常。
            乐于时傅，皮卞齐康。
            伍余元卜，顾孟平黄。
            和穆萧尹，姚邵湛汪。
            祁毛禹狄，米贝明臧。
            计伏成戴，谈宋茅庞。
            熊纪舒屈，项祝董梁。
            杜阮蓝闵，席季麻强。
            贾路娄危，江童颜郭。
            梅盛林刁，钟徐邱骆。
            高夏蔡田，樊胡凌霍。
            虞万支柯，昝管卢莫。
            经房裘缪，干解应宗。
            丁宣贲邓，郁单杭洪。"""

        firstnames = firstnames.replace('，', '').replace('。', '').replace('\n', '').replace(' ', '')
        firstname = random.choice(firstnames)

        secondname_boy = """
        澄邈、德泽、海超、海阳、海荣、海逸、海昌、瀚钰、瀚文、涵亮、涵煦、涵蓄、涵衍、浩皛、浩波、浩博、浩初、浩宕、浩歌、浩广、浩邈、浩气、
        浩思、浩言、鸿宝、鸿波、鸿博、鸿才、鸿畅、鸿畴、鸿达、鸿德、鸿飞、鸿风、鸿福、鸿光、鸿晖、鸿朗、鸿文、鸿轩、鸿煊、鸿骞、鸿远、鸿云、
        鸿哲、鸿祯、鸿志、鸿卓、嘉澍、光济、澎湃、彭泽、鹏池、鹏海、浦和、浦泽、瑞渊、越泽、博耘、德运、辰宇、辰皓、辰钊、辰铭、辰锟、辰阳、
        辰韦、辰良、辰沛、晨轩、晨涛、晨濡、晨潍、鸿振、吉星、铭晨、起运、运凡、运凯、运鹏、运浩、运诚、运良、运鸿、运锋、运盛、运升、运杰、
        运珧、运骏、运凯、运乾、维运、运晟、运莱、运华、耘豪、星爵、星腾、星睿、星泽、星鹏、星然、震轩、震博、康震、震博、振强、振博、振华、
        振锐、振凯、振海、振国、振平、昂然、昂雄、昂杰、昂熙、昌勋、昌盛、昌淼、昌茂、昌黎、昌燎、昌翰、晨朗、德明、德昌、德曜、范明、飞昂、
        高旻、晗日、昊然、昊天、昊苍、昊英、昊宇、昊嘉、昊明、昊伟、昊硕、昊磊、昊东、鸿晖、鸿朗、华晖、金鹏、晋鹏、敬曦、景明、景天、景浩、
        俊晖、君昊、昆琦、昆鹏、昆纬、昆宇、昆锐、昆卉、昆峰、昆颉、昆谊、昆皓、昆鹏、昆明、昆杰、昆雄、昆纶、鹏涛、鹏煊、曦晨、曦之、新曦、
        旭彬、旭尧、旭鹏、旭东、旭炎、炫明、宣朗、学智、轩昂、彦昌、曜坤、曜栋、曜文、曜曦、曜灿、曜瑞、智伟、智杰、智刚、智阳、昌勋、昌盛、
        昌茂、昌黎、昌燎、昌翰、晨朗、昂然、昂雄、昂杰、昂熙、范明、飞昂、高朗、高旻、德明、德昌、德曜、智伟、智杰、智刚、智阳、瀚彭、旭炎、
        宣朗、学智、昊然、昊天、昊苍、昊英、昊宇、昊嘉、昊明、昊伟、鸿朗、华晖、金鹏、晋鹏、敬曦、景明、景天、景浩、景行、景中、景逸、景彰、
        昆鹏、昆明、昆杰、昆雄、昆纶、鹏涛、鹏煊、景平、俊晖、君昊、昆琦、昆鹏、昆纬、昆宇、昆锐、昆卉、昆峰、昆颉、昆谊、轩昂、彦昌、曜坤、
        曜文、曜曦、曜灿、曜瑞、曦晨、曦之、新曦、鑫鹏、旭彬、旭尧、旭鹏、旭东、浩涆、浩瀚、浩慨、浩阔、鸿熙、鸿羲、鸿禧、鸿信、泽洋、泽雨、
        哲瀚、胤运、佑运、允晨、运恒、运发、云天、耘志、耘涛、振荣、振翱、中震、子辰、晗昱、瀚玥、瀚昂、瀚彭、景行、景中、景逸、景彰、绍晖、
        文景、曦哲、永昌、子昂、智宇、智晖、晗日、晗昱、瀚玥、瀚昂、昊硕、昊磊、昊东、鸿晖、绍晖、文昂、文景、曦哲、永昌、子昂、智宇、智晖、
        浩然、鸿运、辰龙、运珹、振宇、高朗、景平、鑫鹏、昌淼、炫明、昆皓、曜栋、文昂"""

        secondname_grid = """
        恨桃、依秋、依波、香巧、紫萱、涵易、忆之、幻巧、水风、安寒、白亦、惜玉、碧春、怜雪、听南、念蕾、紫夏、凌旋、芷梦、凌寒、梦竹、千凡、
        采波、元冬、思菱、平卉、笑柳、雪卉、南蓉、谷梦、巧兰、绿蝶、飞荷、平安、芷荷、怀瑶、慕易、若芹、紫安、曼冬、寻巧、寄波、尔槐、以旋、
        初夏、依丝、怜南、傲菡、谷蕊、笑槐、飞兰、笑卉、迎荷、元冬、痴安、妙绿、觅雪、寒安、沛凝、白容、乐蓉、映安、依云、映冬、凡雁、梦秋、
        梦凡、秋巧、若云、元容、怀蕾、灵寒、天薇、翠安、乐琴、宛南、怀蕊、白风、访波、亦凝、易绿、夜南、曼凡、亦巧、青易。冰真、白萱、友安、
        海之、小蕊、又琴、天风、若松、盼菡、秋荷、香彤、语梦、惜蕊、迎彤、沛白、雁山、易蓉、雪晴、诗珊、春冬、又绿、冰绿、半梅、笑容、沛凝、
        映秋、盼烟、晓凡、涵雁、问凝、冬萱、晓山、雁蓉、梦蕊、山菡、南莲、飞双、凝丝、思萱、怀梦、雨梅、冷霜、向松、迎丝、迎梅、雅彤、香薇、
        以山、碧萱、寒云、向南、书雁、怀薇、思菱、忆文、翠巧、怀山、若山、向秋、凡白、绮烟、从蕾、天曼、又亦、从安、绮彤、之玉、凡梅、依琴、
        沛槐、又槐、元绿、安珊、夏之、易槐、宛亦、白翠、丹云、问寒、易文、傲易、青旋、思真、雨珍、幻丝、代梅、盼曼、妙之、半双、若翠、初兰、
        惜萍、初之、宛丝、寄南、小萍、静珊、千风、天蓉、雅青、寄文、涵菱、香波、青亦、元菱、翠彤、春海、惜珊、向薇、冬灵、惜芹、凌青、谷芹、
        雁桃、映雁、书兰、盼香、向山、寄风、访烟、绮晴、映之、醉波、幻莲、谷冬、傲柔、寄容、以珊、紫雪、芷容、书琴、寻桃、涵阳、怀寒、易云、
        代秋、惜梦、尔烟、谷槐、怀莲、夜山、芷卉、向彤、新巧、语海、灵珊、凝丹、小蕾、迎夏、慕卉、飞珍、冰夏、亦竹、飞莲、海白、元蝶、春蕾、
        怀绿、尔容、小玉、幼南、凡梦、碧菡、初晴、宛秋、傲旋、新之、凡儿、夏真、静枫、痴柏、恨蕊、乐双、念薇、靖雁、寄松、丹蝶、元瑶、冰蝶、
        念波、迎松、海瑶、乐萱、凌兰、曼岚、若枫、傲薇、凡灵、乐蕊、秋灵、谷槐、觅云、寻春、恨山、从寒、忆香、觅波、静曼、青寒、笑天、涵蕾、
        元柏、代萱、紫真、千青、雪珍、寄琴、绿蕊、醉柳、诗翠、念瑶、孤风、曼彤、怀曼、香巧、采蓝、芷天、尔曼、巧蕊"""

        if gender.lower() in ('girl', 'woman'):
            secondname = random.choice(secondname_grid.split('、'))
        elif gender.lower() in ('boy', 'man'):
            secondname = random.choice(secondname_boy.split('、'))
        elif isinstance(gender, int):
            if gender % 2 == 0:
                secondname = random.choice(secondname_grid.split('、'))
            else:
                secondname = random.choice(secondname_boy.split('、'))
        else:
            secondname = random.choice([random.choice(secondname_boy.split('、')),
                                        random.choice(secondname_grid.split('、'))])

        return '{}{}'.format(firstname, secondname)
