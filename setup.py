#!/usr/bin/env python
# coding:utf-8
"""将个人封装的公共方法打包"""
from setuptools import setup, find_packages


PACKAGE_NAME = "deng"
PACKAGE_VERSION = "2019.11.05"


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description="Personal method encapsulation",
    url="https://github.com/Deng2016/deng",
    author="dengqingyong",
    author_email="yu12377@163.com",
    packages=find_packages(),
    exclude_package_data={"": [".gitignore"]},
    install_requires=[
        "requests>=2.18.2",
        "python-dateutil>=1.5",
        "requests-html>=0.9.0",
        ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ]
)
