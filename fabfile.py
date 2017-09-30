#!/usr/bin/env python
# coding:utf-8
from fabric.api import settings, cd, run, prefix
from deng.colors import *


servers = [
            {"host": "ci", "virtualenv": "cloud_ci"},
            {"host": "ejen-root", "virtualenv": ""}
           ]


def update():
    """将新push的脚本更新到jenkins上"""
    for server in servers:
        print(blue("\n\n开始部署 主机: %s, 虚拟环境：%s" % (server["host"], server["virtualenv"])))
        with settings(forward_agend=True, use_ssh_config=True, host_string=server["host"], colorize_errors=True):
            print(blue("部署：下载源码"))
            run("rm -rf ~/deng")
            run("git clone ssh://git@gitlab/ci-python/deng.git")
            with cd("~/deng"):
                if len(server["virtualenv"]) > 0:
                    with prefix("workon %s" % server["virtualenv"]):
                        try:
                            print(blue("部署：删除旧版"))
                            run("pip uninstall -y deng")
                        except:
                            print red("删除原有deng包报错，忽略！")
                        print(blue("部署：部署新版"))
                        run("pwd")
                        run("python setup.py install")
                        print(blue("查看deng包信息"))
                        run("pip show deng")
                else:
                    try:
                        print(blue("部署：删除旧版"))
                        run("pip uninstall -y deng")
                    except:
                        print red("删除原有deng包报错，忽略！")
                    print(blue("部署：部署新版"))
                    run("python setup.py install")
                    print(blue("查看deng包信息"))
                    run("pip show deng")

            print(blue("部署：删除源码"))
            run("rm -rf ~/deng")
        print(blue("完成部署: %s, %s" % (server["host"], server["virtualenv"])))
