Elasticsearch python3
---

> pip install elastcisearch

python 对Elasticsearch的操作基于Elasticsearch类创建的实例

创建索引index(database)

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()

result = es.indices.create(index='index-name', ignore = 400)
print(result)

# >> 创建成功 {'acknowledged': True, 'shards_acknowledged': True, 'index': 'index-name'}
# >> 捕获重复创建的400错误 {'error': {'root_cause': [{'type': 'resource_already_exists_exception', 're
# ason': 'index [index-name/QM6yz2W8QE-bflKhc5oThw] already exists', 'index_uuid'
# : 'QM6yz2W8QE-bflKhc5oThw', 'index': 'index-name'}], 'type': 'resource_already_
# exists_exception', 'reason': 'index [index-name/QM6yz2W8QE-bflKhc5oThw] already
#  exists', 'index_uuid': 'QM6yz2W8QE-bflKhc5oThw', 'index': 'index-name'}, 'stat
# us': 400}
```

删除index(database)

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()
result = es.indices.delete(index='index-name', ignore=[400,404])
print(result)

# >> {'acknowledged': True} 成功删除
# >> {'error':{xxxx}, 'status':404} 重复删除404错误捕获

```

插入数据两种方式

```python
from elasticsearch import Elasticsearch
es = Elasticsearch()
# 插入的数据为json数据, doc_type  相当于数据库中的tableName, id如果不给定会生成随机的唯一字符串
result = es.create(index='index-name', doc_type='table-name', id=1,body={'title', 'ttttt'})
# 第二种插入的方式
result = es.index(index='index_name', doc_type='table-name', id=1, body={'title':'tttt'})
print(result)
"""
>>     {'_index':'index-name',
        '_type':'table-name',
        '_id':'1',
        '_version':1,
        'result':'created', # 插入成功
        '_shards':{'total':2,'successful':1,'failed':0},
        '_seq_no':0,
        '_primary_term':1}
"""

```

更新数据

```python
from elasticsearch import Elasticsearch
es = Elasticsearch()
data = {}
# 指明id将数据更新
result = es.update(index='index-name', doc_type='table-name', body={'doc':data}, id=1)
print(result)
# 会将整条记录更新
# 返回的结果 中 {'result':'update'}

```

删除数据

```python
from elasticsearch import Elasticsearch
es = Elasticsearch()
result = es.delete(index='index-name',doc_type='table-name', id=1)
print(result)
# 返回数据中{'result':'delete'}
```

注意到: 每一条记录都有_version字段, 每当更改一次当前记录的数据,_version字段就会+1

除去增删改的功能外,Elasticsearch的特色在查询,针对中文,需要中文分词工具`https://github.com/medcl/elasticsearch-analysis-ik`
下载相对应版本的,解压到安装目录的plugin目录下,重启动es,插件将被加载

安装完中文分词后执行

```python
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
es.indices.create(index='news', ignore=400)
# 添加分词引擎
es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
# 添加数据
for i, data in enumerate(datas):
    es.index(index='news', doc_type='politics', body=data, id=i + 1)
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
res = es.search(index='news', doc_type='politics', body=dql)
print(json.dumps(res, indent=4, ensure_ascii=False))



```
结构化检索
---
```python

# 精确查找,内部无额外的评分计算,只对文档进行包括和排除计算
# constant_score 非评分模式
# filter 以过滤的方式
# term 执行精确查找
# 返回的结果中_score恒定为1
"select * from table-name where date=`2011-12-18`"
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
# 但是用term查询中文却得不到想要的结果,因为中文分词工具将中文字符串分成一个个小
# token储存, 例如:中国人民  -- 中  国  人  民   中国   人民

```

> 参考自:  	https://blog.csdn.net/wufaliang003/article/details/81368365
> 中文文档 https://www.elastic.co/guide/cn/index.html

多值过滤->组合过滤器
`SELECT product FROM table WHERE (price = 20 OR pid = "aacczz01") AND (price !=30)`

通过布尔过滤器组合
```json
{
  "bool" : {
      "must" :[],
      "should":[],
      "must_not":[]
  }
}
```
其中must=AND should=OR must_not=NOT

将上述sql改为dql
```python
dql = {
    'query': {
        'bool':{
            'should':[
                {'term':{'price':20}},
                {'term':{'pid':'aacczz01'}}
            ],
            'must_not':[{'term':30}]
        }
    }
}
``` 

虽然bool过滤器可以集成分支,但是它也就是一个过滤器,所以可做bool过滤器嵌套

`select document from table where pid = "xxxx1" or (pid=xxxx2 and price=30)`

```python
dql = {
'query':{
    'bool':{
        'should':[
            {'term':{'pir':'xxxx1'}},
            {'bool':{'must':[{'term':{'pid':'xxx2'}},{'term':{'price':30}}]}}
        ]
    }
}
}
```

`select name from goods where price in (20,30)`

```python
# 没必要使用bool过滤,直接terms即可
dql = {
    'query':{
        'const_score':{
            'filter':{
                'terms':{
                    'price':[20,30]
                }
            }
        }
    }
}

```

范围查询

`select document from table where price between 20 and 40`

```python
dql = {
    'query': {
        'constant_score':{
            'filter':{
                'range':{
                    'price':{
                        'gte':20,
                        'lte':40
                    }
                }
            }
        }
    }
}
```
使用range过滤器,
```
gt: >
lt: <
gte: >=
lte: <=
```
可以只规定一侧边界

时间类型的范围查询

```python
from datetime import datetime
start = datetime.strptime('2018-01-01 12:11:11','%Y-%m-%d %H:%M:%S')
end = datetime.strptime('2018-01-02 11:11:11','%Y-%m-%d %H:%M:%S')
dql = {
    'query':{
        'constant_score': {
            'filter':{
                'range':{
                    'date':{
                        'gt': start,
                        'lt': end
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
# 注意存储的时候转为时间对象存储,比较的时候也使用时间对象比较,使用字符串比较需要注意格式一致 

```

字符串也是有顺寻的 a<b<...<z,同样的,字符串也是可以用来比较的


处理空值

`SELECT tags FROM posts WHERE tags IS NOT NULL`

现在有数据
```python
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
# 查询tags字段为非空

dql = {
    'query': {
        'constant_score': {
            'filter': {
                'exists': {'field': 'tags'}
            }
        }
    }
}

```

`SELECT tags FROM posts WHERE tags IS NULL`

```python
dql_1 = {
    'query': {
        'bool': {'must_not': {'exists': {'field': 'tags'}}}
    }
}
```

过滤缓存器,相同的过滤器会被缓存

```python
dql = {
    'query':{
        'constant_score':{
            'filter':{
                'bool':{
                    'should':[
                        {'bool':{
                            'must':[
                                {'term':{'folder':'inbox'}},
                                {'term':{'read':False}},
                            ]
                        }},
                        {'bool':{
                            'must_not':[
                                {'term':{'folder':'inbox'}},
                                {'term':{'important':False}},
                            ]
                        }}
                    ]
                }
            }
        }
    }
}
```
以上两个对folder的过滤器用的是同一个过滤器,所以在执行第一个的时候就被缓存,第二次被使用的时候,直接在缓存中
获取结果

缓存条件:

- 最近多次被查询到
- 文档数量超出总文档数量的3%
- 如果缓满了,将从使用次数少的中剔除旧的缓存

全文检索
---

+ 相关性
    + TF/IDF  地理位置临近 模糊相似 等算法
+ 分析
    + 文本转换成token<建立倒排索引, 查询倒排索引>
    
文本查询:

+ 基于词项
    + term
    + fuzzy
+ 基于全文
    + match
    + query_string
    
    
 match不但可以处理全文字段,也可以处理精确字段
 
 数据+查询+结果:
 ```python
datas = [
    {"title": "The quick brown fox"},
    {"title": "The quick brown fox jumps over the lazy dog"},
    {"title": "The quick brown fox jumps over the quick dog"},
    {"title": "Brown fox brown dog"},
]

dql = {
    'query': {
        'match': {
            'title': 'QUICK!'
        }
    }
}
res =  [
      {
        "_index": "my_index",
        "_type": "my_type",
        "_id": "2",
        "_score": 0.59891266,
        "_source": {
          "title": "The quick brown fox jumps over the lazy dog"
        }
      },
      {
        "_index": "my_index",
        "_type": "my_type",
        "_id": "3",
        "_score": 0.39556286,
        "_source": {
          "title": "The quick brown fox jumps over the quick dog"
        }
      },
      {
        "_index": "my_index",
        "_type": "my_type",
        "_id": "1",
        "_score": 0.2876821,
        "_source": {
          "title": "The quick brown fox"
        }
      }
    ]
```
评分系统是根据关键字在全文中占据的比重计算的


多词语查询

```python
dql = {
    "query": {
        "match": {
            "title": "BROWN DOG!"
        }
    }
}
```
多词语查询

结果:有brown或者dog,计算评分是按照两个词语来计算的,只有一个词语命中,评分低

如果想提高精度,那么就要使用and配置
```python
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
```

以可通过百分比来控制精度

```python
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
```

组合查询,结构化查询+全文查询

```python

dql = {
    'query': {
        'bool': {
            'must': [{'match': {'title': 'quick'}}],
            'must_not': [{'match': {'title': 'lazy'}}],
            'should': [{'match': {'title': 'brown'}}, {'match': {'title': 'dog'}}],
        }
    }
}
```
查询的是有quick没有lazy,有或者没有(brown or dog)

组合查询也是可以控制精度的

```python
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

```
控制最小需要有两个should匹配到


如上所示,控制精度的多词语查询可以转变成为bool查询



现在有查询

```python

dql = {
    "query": {
        "bool": {
            "must": {
                "match": {
                    "content": { 
                        "query":    "full text search",
                        "operator": "and"
                    }
                }
            },
            "should": [ 
                { "match": { "content": "Elasticsearch" }},
                { "match": { "content": "Lucene"        }}
            ]
        }
    }
}

```
上述查询中must是必须字段,should中,匹配的should越多,结果相关性越高,评分越高

现在又有需求,匹配到Elasticsearch的评分要比Lucene高(权重),可以通过boost来提高字段权重,默认boost是1

```python
dql = {
    "query": {
        "bool": {
            "must": {
                "match": {  
                    "content": {
                        "query":    "full text search",
                        "operator": "and"
                    }
                }
            },
            "should": [
                { "match": {
                    "content": {
                        "query": "Elasticsearch",
                        "boost": 3 
                    }
                }},
                { "match": {
                    "content": {
                        "query": "Lucene",
                        "boost": 2 
                    }
                }}
            ]
        }
    }
}

```
