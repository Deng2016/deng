#!/usr/bin/env python
# coding:utf-8
from fabric import Connection, task
from deng.colors import *


servers = [
            {"host": "off93", "virtualenv": "cstest_py3"}
           ]


def update():
    """将新push的脚本更新到jenkins上"""
    for server in servers:
        print(blue("\n\n开始部署 主机: %s, 虚拟环境：%s" % (server["host"], server["virtualenv"])))
        with Connection(server["host"]) as c:
            print(blue("部署：下载源码"))
            c.run("rm -rf ~/deng")
            c.run("git clone git@github.com:Deng2016/deng.git")
            with c.cd("~/deng"):
                if len(server["virtualenv"]) > 0:
                    with c.prefix("workon %s" % server["virtualenv"]):
                        _deploy(c)
                else:
                    _deploy(c)

            print(blue("部署：删除源码"))
            c.run("rm -rf ~/deng")
        print(blue("完成部署: %s, %s" % (server["host"], server["virtualenv"])))


def _deploy(c):
    """更新deng程序包"""
    try:
        print(blue("部署：删除旧版"))
        c.run("pip uninstall -y deng")
    except:
        print(red("删除原有deng包报错，忽略！"))
    print(blue("部署：部署新版"))
    c.run("pwd")
    c.run("python setup.py install")
    print(blue("查看deng包信息"))
    c.run("pip show deng")


if __name__ == "__main__":
    update()