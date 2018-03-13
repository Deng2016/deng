# 个人常用工具类封装

## 依赖包安装说明  
**注意：mac系统或是linux系统跳过此步骤**    
[windows64位系统安装mysql-python跳坑说明](http://blog.csdn.net/yu12377/article/details/79525470)    
> 本包中mysql连接池类用到了mysql-python包，上述指引是mysql-python包的安装说明 

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
