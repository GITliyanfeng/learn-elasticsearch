# -*- coding: utf-8 -*-
# @Time    : 2019/3/17 0017 23:35
# @Author  : __Yanfeng
# @Site    : 
# @File    : posts_save.py
# @Software: PyCharm
from elasticsearch import Elasticsearch

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

es.indices.create(index='blog', ignore=400)
es.indices.put_mapping(index='blog', doc_type='posts', body=mapping)
datas = [
    {
        'name': '美团外卖',
        'price': 20,
        'desc': '这是美团外卖',
        'tags': ['美团', None]
    }, {
        'name': '百度地图',
        'price': 30,
        'desc': '这是百度地图',
        'tags': ['地图', '百度']
    }, {
        'name': '支付宝',
        'price': 15,
        'desc': '这是支付宝',
        'tags': []

    }, {
        'name': '蚂蚁花呗',
        'price': 70,
        'desc': '这是蚂蚁花呗',
        'tags': [None, '阿里']
    },
]

for i, data in enumerate(datas):
    es.index(index='blog', doc_type='posts', body=data, id=i + 1)
