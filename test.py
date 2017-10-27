#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import time
import requests
from SSDB import SSDB
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
    "http://www.bd-film.co/zx/index{}.htm",  # # 最新
    "http://www.bd-film.co/gq/index{}.htm",  # # 高清
    "http://www.bd-film.co/gy/index{}.htm",  # # 国语
    "http://www.bd-film.co/zy/index{}.htm",  # # 微电影
    "http://www.bd-film.co/jd/index{}.htm",  # # 经典电影
    "http://www.bd-film.co/dh/index{}.htm",  # # 动画电影
    "http://www.bd-film.co/hj/index{}.htm",  # # 集合
]

if __name__ == "__main__":
    print sys.version
    print time.ctime()
    # # #  "" 或者 "_{}".format(n)
    # print url[0].format("")
    # content = None
    #
    # with open('test.html', 'r') as f:
    #     content = f.read()
    #
    # if content is None:
    #     sys.exit("content is None")
    #
    # # print content
    # # text = unicode(content, encoding='utf-8')  # 解决乱码问题 TypeError: 'unicode' object is not callable
    # dom = pq(content)
    # # 页码 判断页数 1/n 格式
    # index_str = dom('#main .listpage').find('b').html()
    # pagination = index_str.split("/")
    # page_one = pagination[0]  # 当前页数
    # page_n = pagination[1]  # 总页数
    #
    # ul = dom('ul').filter('.list')
    # lis = ul('li')
    # pattern = re.compile(ur'[\u300a][\S\s]+[\u300b]')  # 获取电影name \u300b = 》;\u300a = 《
    #
    # for li in lis.items():
    #     # print li.html()
    #     # print li('span').html()
    #     params = {}
    #     dy_name = None
    #     if li('a').find('font').html() is None:
    #         dy_name = li('a').html()
    #     else:
    #         dy_name = li('a').find('font').html()
    #     # print li('a').attr('href')
    #     match = re.search(pattern, dy_name)
    #     params['name'] = dy_name
    #     print params
    #     if match:
    #         # print match.group()
    #         pass
    #     else:
    #         if u"教你下载" in dy_name:
    #             # print u'教程'
    #             pass
    #         else:
    #             print u'错误 ！！！'
    #             print li.html()
    #             continue
    # # name title category
    #
    # content = None
    #
    # with open('test1.html', 'r') as f:
    #     content = f.read()
    #
    # dom = pq(content)
    # content = dom('#endText').html()
    # print dom('#endText').find('img').eq(0).attr('src')
    # # print content
    # ps = dom('#endText').find('p')
    #
    # content = u""
    # dr = re.compile(r'<[/]*a[^>]*>', re.S)  # 去除 <a></a> 标签
    # for p in ps.items():
    #     content = content + u'<p>' + dr.sub('', p.html()) + u'</p>'
    # content = content + u'<p><table border="0" cellspacing="1" cellpadding="10" width="100%">' + dom('table').html() + u'</table></p>'
    #
    # # print content
    # content_res = requests.get("http://www.hao6v.com/gydy/2013-11-26/21859.html")
    # # print content_res.content
    # # print content_res.content
    # try:
    #     text_content = unicode(content_res.content, 'gb2312')
    # except Exception, ex:
    #     print ex
    #     try:
    #         text_content = unicode(content_res.content, 'gbk')
    #     except Exception, ex:
    #         print ex
    #         try:
    #             text_content = unicode(content_res.content, 'gb18030')
    #         except Exception, ex:
    #             print ex
    #             try:
    #                 text_content = unicode(content_res.content, 'utf-8')
    #             except Exception, ex:
    #                 print ex
    #                 text_content = content_res.content
    # content_dom = pq(text_content)
    # # print content_dom.html()
    # ps = content_dom('#endText').find('p')
    # content = u""
    # dr = re.compile(r'<[/]*a[^>]*>', re.S)  # 去除 <a></a> 标签
    # for p in ps.items():
    #     print p.html()
    # for p in ps.items():
    #     if p.html():
    #         content = content + u'<p>' + dr.sub('', p.html()) + u'</p>'
    # print content
    # content = content + u'<p><table border="0" cellspacing="1" cellpadding="10" width="100%">' + content_dom('table').html() + u'</table></p>'
    # print content

    ssdb = SSDB("127.0.0.1", 8888)

    ssdb_res = ssdb.request('get', ["{}_{}".format("名称", 1)])
    print ssdb_res.data

    print ssdb_res

    ssdb.request('set', ["{}_{}".format("名称", 1), "{}".format("标题")])
    ssdb.request('expire', ["{}_{}".format("名称", 1), 60 * 60 * 24 * 1])  # 1天有效期

