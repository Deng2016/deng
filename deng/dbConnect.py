#!/usr/bin/env python
# coding:utf-8
"""功能简要说明
作者：dengqingyong
邮箱：yu12377@163.com
时间：2018/2/26 22:34
"""
try:
    import MySQLdb
except ImportError as e:
    print(e.message)
    import os
    os.system('pip install mysql-python')
    import MySQLdb

try:
    from DBUtils.PooledDB import PooledDB
except ImportError as e:
    print(e.m)
    import os
    os.system('pip install DBUtils')
    from DBUtils.PooledDB import PooledDB


class MysqlPool(object):
    """mysql连接池"""
    def __init__(self, username, password, db_name, db_host, db_port, maxconnections=100):
        self.pool = PooledDB(MySQLdb,
                             mincached=5,
                             maxcached=20,
                             maxconnections=maxconnections,
                             blocking=True,
                             host=db_host,
                             user=username,
                             passwd=password,
                             db=db_name,
                             port=db_port,
                             charset='utf8')

    def get_cur(self):
        """获取连接与游标"""
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur
