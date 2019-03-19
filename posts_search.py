# -*- coding: utf-8 -*-
# @Time    : 2019/3/17 0017 23:48
# @Author  : __Yanfeng
# @Site    : 
# @File    : posts_search.py
# @Software: PyCharm
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

dql = {
    'query': {
        'constant_score': {
            'filter': {
                'exists': {'field': 'tags'}
            }
        }
    }
}
dql_1 = {
    'query': {
        'bool': {'must_not': {'exists': {'field': 'tags'}}}
    }
}
res = es.search(index='blog', doc_type='posts', body=dql_1)
print(json.dumps(res, indent=2, ensure_ascii=False))
