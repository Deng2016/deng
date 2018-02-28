# 个人常用工具类封装

## 更新历史

#### 2018-02-27
* 新增mysql连接池类MysqlPool；

## 远程pip安装
```
pip install git+https://github.com/Deng2016/deng@201801
```

## 安装应用
```
python setup.py install
```

## 开发模式安装
```
python setup.py develop
```

## 创建egg包
```
# 生成egg包
python setup.py bdist_egg

# 安装egg包
easy_install deng-0.1-py2.7.egg
```

## 创建tar.gz包
```
# 创建tar.gz包
python setup.py sdist --formats=gztar

# 将tar.gz包安装到别处
pip install deng-0.1.tar.gz
```

[打包参考资料](http://www.bjhee.com/setuptools.html)
