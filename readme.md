# 个人常用工具类封装


## 更新历史
### 2021-11-17  
* 重构  

### 2019-11-07
* 新增生成银联卡卡号方法，可通过[支付宝校验](https://ccdcapi.alipay.com/validateAndCacheCardInfo.json?_input_charset=utf-8&cardNo=9400621673734008267&cardBinCheck=true)

### 2018-04-20  
* 新增to_dict方法，将x-www-form-urlencoded格式字符串转换成dict  

### 2018-02-27  
* 新增mysql连接池类MysqlPool；  

## pip安装
```
# 此方式安装方法最简便，但可能不是最新的
pip install deng
# 安装最新的版本
pip install git+https://github.com/Deng2016/deng@201801
```

## requirements.txt引用
```
-e git+git@github.com:Deng2016/deng.git@master#egg=deng
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

## 将包发布到pypi
```
# 先升级打包工具
pip install --upgrade setuptools wheel twine

# 打包
python setup.py sdist bdist_wheel

# 检查
twine check dist/*

# 上传pypi
twine upload dist/*
```

[打包参考资料](http://www.bjhee.com/setuptools.html)
