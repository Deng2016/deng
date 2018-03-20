# 个人常用工具类封装


## 更新历史

#### 2018-02-27
* 新增mysql连接池类MysqlPool；

## API文档
### 1. [mysql连接池-dbConnect.py](deng/dbConnect.py)
```python
# MysqlPool连接池使用说明：
# 导入MysqlPool类
from deng.dbConnect import MysqlPool

# 实例化一个连接池对象
pool = MysqlPool(username='xxx', password='xxx', db_name='xxx', db_host='x.x.x.x', db_port='3306')
# 定义sql语句
sqlstr = 'select * from tables'
# 获取连接句柄与游标
conn, cursor = pool.get_cur()
# 执行sql语句，碰到异常时回滚
try:
    cursor.execute(sqlstr)
except Exception as e:
    print('执行SQL语句报错: {}'.format(sqlstr))
    # 回滚
    conn.rollback()
else:
    print('执行语句：{}'.format(sqlstr))
finally:
    # 关闭游标
    cursor.close()
    # 提交改变
    conn.commit()
    # 关闭连接
    conn.close()
```

### 2. [线程池-MultiThreading.py](deng/MultiThreading.py)
```python
# ThreadPool线程池使用说明
# 导入ThreadPool类
from deng.MultiThreading import ThreadPool
import random


# 定义业务函数
def multi_test(username=None):
    print('Hello {}!'.format(username))


# 实例化线程池
pool = ThreadPool()

# 往线程池队列中添加任务
for i in range(10000):
    username = random.choice(['熊大', '熊二', '光头强', '吉吉国王', '毛毛'])
    pool.add_job(multi_test, (username))

# 创建线程，创建后会自动运行，并消费队列中的任务，当没有任务等待timeout秒后超时退出
pool.create_threadpool(100, timeout=2)
```

### 3. [测试数据生成类-testdata.py](deng/testdata.py)
```python
from deng.testdata import TestData 

# 生成中国姓名：参数gender: 默认随机，女：woman, gril, 偶数，男：man, boy, 奇数 
TestData.get_name()

# 生成中国大陆18位身份证号码：参数sex，默认随机，女：偶数，男：奇数
TestData.get_idcards()

# 检查身份证号码是否合法
TestData.check_idcards(idcards=430521187907090987)

# 随机生成手机号码
TestData.get_phone_on()

# 随机生成手机串号
TestData.get_phone_serial_no()
```

### 4. [工具百宝箱-tools.py](deng/tools.py)  
```python
# 导入Tools类
from deng.tools import Tools 

# 格式化输出: 可以处理dist, list, tuple, set, requests.response对象, xml.etree.ElementTree.Element对象
Tools.format_print(res)

# 对字典，列表，字符串进行排序
Tools.sort_custom()

# 获取时间戳
# 参数length长度，默认10，取值有10，13
# 参数offset偏移量，单位为秒
Tools.get_timestamp()

# 获取当前时间，参数
# format：默认long，取值有long，short
# offset：默认0，单位为秒
Tools.get_current_time()

# 从键盘上获取一个数字，并做异常处理
Tools.get_digit()
```

### 5. [彩色输出-colors.py](deng/colors.py)
```python
# 导入所有颜色
from deng.colors import * 

# 红色
print(red('红色'))

# 绿色
print(green('绿色'))

# 黄色
print(yellow('黄色'))

# 蓝色
print(blue('蓝色'))
```

### 6. [图片处理工具类-colors.py](deng/image.py)

### 7. [邮件处理工具-mailTool.py](deng/mailTool.py)
```python
# 导入MailTool类
from deng.mailTool import MailTool

# 实例化邮件对象
mail = MailTool(send_username='xxx', send_password='xxx', send_smtp='stmp.qq.com')

# 发送邮件
mail.send(receiver='接收人邮箱', subject='邮件主题', content='邮件正文', attachs='邮件附件路径')
```

## 依赖包安装说明  
**注意：mac系统或是linux系统跳过此步骤**    
[windows64位系统安装mysql-python跳坑说明](http://blog.csdn.net/yu12377/article/details/79525470)    
> 本包中mysql连接池类用到了mysql-python包，上述指引是mysql-python包的安装说明 

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
