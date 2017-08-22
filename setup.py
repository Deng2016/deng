#!/usr/bin/env python
# coding:utf-8
"""将个人封装的公共方法打包"""
from setuptools import setup, find_packages


setup(
    name="deng",
    version="0.1",
    summary="个人常用方法封装",
    author="dengqingyong",
    author_email="yu12377@163.com",
    packages=find_packages(),
    exclude_package_data={"": [".gitignore"]},
    install_requires=[
        "requests>=2.18.2",
        "python-dateutil>=1.5",
    ]
)
