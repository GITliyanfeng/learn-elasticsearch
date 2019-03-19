# -*- coding: utf-8 -*-
# @Time    : 2019/3/17 0017 16:08
# @Author  : __Yanfeng
# @Site    : 
# @File    : create_index.py
# @Software: PyCharm
from elasticsearch import Elasticsearch

# 创建elasticsearch实例
es = Elasticsearch()

# 创建一个index[数据库]news, ignore400是异常捕获, 捕获400的异常
# result = es.indices.create(index='news', ignore=400)
# 删除一个索引的时候,ignore404捕索引已经被删除,重复执行删除操作的时候
# result = es.indices.delete(index='news', ignore=[400, 404])
# 插入数据
# es.indices.create(index='news', ignore=400)
data = {
    'title': '中国美国百度',
    'url': 'http://www.baidu.com',
}
# result = es.create(index='news', doc_type='politics', id=1, body=data)  # 在news中的politics表中插入一行记录
# 可以直接使用index方法插入数据
data_2 = {
    'title': 'IT 腾讯 阿里',
    'url': 'http://im.qq.com'
}
# result = es.index(index='news', doc_type='politics', body=data_2, id=2)  # 如果不指定id,会生成一个默认唯一的随机字符串作为id
# 更新数据
data_1_1 = {
    'title': 'IT 腾讯 阿里',
    'url': 'http://im.qq.com',
    'date': '2012-02-03'
}
# result = es.update(index='news', doc_type='politics', body={'doc': data_1_1}, id=2)
result = es.delete(index='news', doc_type='politics', id=2)
print(result)
