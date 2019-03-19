# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 0019 15:22
# @Author  : __Yanfeng
# @Site    : 
# @File    : allarticle_save.py
# @Software: PyCharm
from elasticsearch import Elasticsearch

es = Elasticsearch()
es.indices.create(index='my_index', ignore=400)
datas = [
    {"title": "The quick brown fox"},
    {"title": "The quick brown fox jumps over the lazy dog"},
    {"title": "The quick brown fox jumps over the quick dog"},
    {"title": "Brown fox brown dog"},
]

for i, d in enumerate(datas):
    es.index(index='my_index', doc_type='my_type', body=d, id=i + 1)
