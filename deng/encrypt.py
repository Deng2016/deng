#-*- coding:utf-8 -*-
import sys
import imp
imp.reload( sys )
sys.setdefaultencoding('utf-8')
import json
from urllib.parse import urlencode
import requests

class encrypt(object):
    # 计算MD5值
    def getmd5(self, paramStr):
        try:
            import hashlib
            hash = hashlib.md5()
        except ImportError:
            # for Python << 2.5
            import md5
            hash = md5.new()
        hash.update(paramStr)
        return  hash.hexdigest()

    # 参数升序排序及拼接
    def join_array(self,param):
        str_data='' 
        sorted_x = sorted(iter(param.items()), key=lambda param : param[0])
        for tuple in sorted_x:
            str_data+=str(tuple[0])+str(tuple[1])
        return str_data
