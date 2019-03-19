# -*- coding: utf-8 -*-
# @Time    : 2019/3/17 0017 21:55
# @Author  : __Yanfeng
# @Site    : 
# @File    : good_search.py
# @Software: PyCharm

from elasticsearch import Elasticsearch
import json
from datetime import datetime, date

es = Elasticsearch()
s = datetime.strptime('2019-01-01 12:00:00', '%Y-%m-%d %H:%M:%S')
e = datetime.strptime('2019-01-02 00:00:00', '%Y-%m-%d %H:%M:%S')
dql = {
    'query': {
        'constant_score': {
            'filter': {
                'range': {
                    'price': {
                        'gte': 20,
                        'lte': 40
                    }
                }
            }
        }
    }
}
dql_1 = {
    'query': {
        'constant_score': {
            'filter': {
                'range': {
                    'date': {
                        'gt': '2019-01-01T12:00:00',
                        'lt': '2019-01-01T00:00:00||+1d',
                    }
                }
            }
        }
    }
}
res = es.search(index='store', doc_type='goods', body=dql_1)
print(json.dumps(res, indent=2, ensure_ascii=False))
