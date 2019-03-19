# -*- coding: utf-8 -*-
# @Time    : 2019/3/17 0017 21:29
# @Author  : __Yanfeng
# @Site    : 
# @File    : good_search.py
# @Software: PyCharm
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch()

mapping = {
    'properties': {
        'name': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        },
        'desc': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        },
    }
}
es.indices.delete(index='store', ignore=[404, 400])
es.indices.create(index='store', ignore=400)
es.indices.put_mapping(index='store', doc_type='goods', body=mapping)

datas = [
    {
        'name': '美团外卖',
        'price': 20,
        'desc': '这是美团外卖',
        'date': datetime.strptime('2019-01-01 11:11:11', '%Y-%m-%d %H:%M:%S')
    }, {
        'name': '百度地图',
        'price': 30,
        'desc': '这是百度地图',
        'date': datetime.strptime('2019-01-02 11:11:11', '%Y-%m-%d %H:%M:%S')
    }, {
        'name': '支付宝',
        'price': 15,
        'desc': '这是支付宝',
        'date': datetime.strptime('2019-01-01 12:11:11', '%Y-%m-%d %H:%M:%S')

    }, {
        'name': '蚂蚁花呗',
        'price': 70,
        'desc': '这是蚂蚁花呗',
        'date': datetime.strptime('2019-01-01 12:11:12', '%Y-%m-%d %H:%M:%S')
    }, {
        'name': '自行车',
        'price': 40,
        'desc': '这是自行车',
        'date': datetime.strptime('2019-01-02 11:15:11', '%Y-%m-%d %H:%M:%S')
    }, {
        'name': '王者荣耀',
        'price': 50,
        'desc': '这是王者荣耀',
        'date': datetime.strptime('2019-01-01 21:11:11', '%Y-%m-%d %H:%M:%S')
    }, {
        'name': '哈密瓜',
        'price': 60,
        'desc': '这是哈密瓜',
        'date': datetime.strptime('2019-01-01 11:22:22', '%Y-%m-%d %H:%M:%S')
    },
]

for i, data in enumerate(datas):
    es.index(index='store', doc_type='goods', body=data, id=i + 1)
