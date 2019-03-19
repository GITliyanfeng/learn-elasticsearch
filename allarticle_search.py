# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 0019 15:26
# @Author  : __Yanfeng
# @Site    : 
# @File    : allarticle_search.py
# @Software: PyCharm
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

dql = {
    'query': {
        'match': {
            'title': 'QUICK!'
        }
    }
}
dql = {
    "query": {
        "match": {
            "title": {
                "query": "brown dog",
                "operator": "and"
            }
        }
    }
}
dql = {
    "query": {
        "match": {
            "title": {
                "query": "brown dog",
                "minimum_should_match": "75%"
            }
        }
    }
}
dql = {
    'query': {
        'bool': {
            'must': [{'match': {'title': 'quick'}}],
            'must_not': [{'match': {'title': 'lazy'}}],
            'should': [{'match': {'title': 'brown'}}, {'match': {'title': 'dog'}}],
        }
    }
}

dql = {
    'query': {
        'bool': {
            'should': [
                {'match': {'title': 'brown'}},
                {'match': {'title': 'fox'}},
                {'match': {'title': 'dog'}},
            ],
            'minimum_should_match': 2
        }
    }
}

res = es.search(index='my_index', doc_type='my_type', body=dql)
print(json.dumps(res, indent=2, ensure_ascii=False))
