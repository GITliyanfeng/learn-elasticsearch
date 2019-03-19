# -*- coding: utf-8 -*-
# @Time    : 2019/3/17 0017 17:34
# @Author  : __Yanfeng
# @Site    :
# @File    : es_ik.py
# @Software: PyCharm
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

# mapping为某些字段配置字段类型,分词引擎
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
datas = [
    {
        'title': '美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'},
    {
        'title': '公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16'},
    {
        'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17'
    },
    {
        'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18'
    }

]
# 创建database
# es.indices.create(index='news', ignore=400)
# 添加分词引擎
# es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
# 添加数据
# for i, data in enumerate(datas):
#     es.index(index='news', doc_type='politics', body=data, id=i + 1)
# 查询所有
res = es.search(index='news', doc_type='politics')
# 全文检索
dql = {
    'query': {
        'match': {
            'title': '中国 领事馆'
        }
    }
}
dql_1 = {
    'query': {
        'constant_score': {
            'filter': {
                'term':
                    {
                        'date': '2011-12-18'
                    }
            }
        }
    }
}
dql_2 = {
    'query': {
        'constant_score': {
            'filter': {
                'term':
                    {
                        'title': '中国'
                    }
            }
        }
    }
}


res = es.search(index='news', doc_type='politics', body=dql_2)
print(json.dumps(res, indent=4, ensure_ascii=False))
