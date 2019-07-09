#!/usr/bin/env python
# coding:utf-8
from fabric import Connection
from deng.colors import *


# 需要部署的环境
servers = [
    {"host": "apidev", "virtualenv": "api_test"},
    {"host": "apidev", "virtualenv": "ifd"},
    {"host": "apidev", "virtualenv": "dubbo_start"},
    {"host": "apidev", "virtualenv": "mock_service"},
    {"host": "apiweb", "virtualenv": "api_test"},
    {"host": "apiweb", "virtualenv": "ifd"},
    {"host": "apiweb", "virtualenv": "dubbo_start"},
    {"host": "apiweb", "virtualenv": "mock_service"},
    {"host": "apiweb", "virtualenv": "user_center"},
]


def package():
    """打包"""
    c = Connection("localhost")
    c.local("rm -f ./dist/*")
    c.local("python setup.py sdist --formats=gztar")
    res = c.local("ls dist")
    return res.stdout.strip()


def update(filename):
    """将新push的脚本更新到jenkins上"""
    for server in servers:
        print(blue("\n\n开始部署 主机: %s, 虚拟环境：%s" % (server["host"], server["virtualenv"])))
        with Connection(server["host"]) as c:
            print(blue("部署：推送新版安装包"))
            c.put(f"./dist/{filename}", filename)
            with c.cd("~"):
                if len(server["virtualenv"]) > 0:
                    with c.prefix("workon %s" % server["virtualenv"]):
                        _deploy(c, filename)
                else:
                    _deploy(c, filename)

            print(blue("部署：删除新版安装包"))
            c.run(f"rm -f ~/{filename}")
        print(blue("完成部署: %s, %s" % (server["host"], server["virtualenv"])))


def _deploy(c, filename):
    """更新程序包"""
    package_name = '-'.join(filename.split('-')[:-1])
    print(blue("部署：部署新版"))
    c.run(f"pip install {filename}")
    print(blue(f"查看{package_name}包信息"))
    c.run(f"pip show {package_name}")


if __name__ == "__main__":
    update(package())
