#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import requests
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')

url = [
    "http://www.hao6v.com/dy/index{}.html",     # # 最新
    "http://www.hao6v.com/gydy/index{}.html",   # # 国语
    "http://www.hao6v.com/zydy/index{}.html",   # # 微电影
    "http://www.hao6v.com/gq/index{}.html",     # # 经典高清
    "http://www.hao6v.com/jddy/index{}.html",   # # 动画电影
    "http://www.hao6v.com/3D/index{}.html",     # # 3 D 电影
    "http://www.hao6v.com/dlz/index{}.html",    # # 国剧
    "http://www.hao6v.com/rj/index{}.html",     # # 日剧
    "http://www.hao6v.com/mj/index{}.html",     # # 欧美剧
    "http://www.hao6v.com/zy/index{}.html",     # # 综艺
       ]
url1 = [
    "http://www.bd-film.co/zx/index{}.htm",       # # 最新
    "http://www.bd-film.co/gq/index{}.htm",       # # 高清
    "http://www.bd-film.co/gy/index{}.htm",       # # 国语
    "http://www.bd-film.co/zy/index{}.htm",       # # 微电影
    "http://www.bd-film.co/jd/index{}.htm",       # # 经典电影
    "http://www.bd-film.co/dh/index{}.htm",       # # 动画电影
    "http://www.bd-film.co/hj/index{}.htm",       # # 集合
]

if __name__ == "__main__":
    print sys.version
    print time.ctime()
    # #  "" 或者 "_{}".format(n)
    print url[0]
    content = None

    with open('test.html', 'r') as f:
        content = f.read()

    if content is None:
        sys.exit("content is None")

    # print content
    # text = unicode(content, encoding='utf-8')  # 解决乱码问题 TypeError: 'unicode' object is not callable
    dom = pq(content)
    # print dom
    index_str = dom('#main .listpage').find('b').html()
    print index_str.split("/")




