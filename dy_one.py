#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import time
import lrequest
import requests
import json
from SSDB import SSDB
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('utf8')

url = [
    "http://www.hao6v.com/dy/index{}.html",     # # 最新 1
    "http://www.hao6v.com/gydy/index{}.html",   # # 国语  2
    "http://www.hao6v.com/zydy/index{}.html",   # # 微电影 3
    "http://www.hao6v.com/gq/index{}.html",     # # 经典高清    4
    "http://www.hao6v.com/jddy/index{}.html",   # # 动画电影    5
    "http://www.hao6v.com/3D/index{}.html",     # # 3 D 电影  6
    "http://www.hao6v.com/dlz/index{}.html",    # # 国剧  7
    "http://www.hao6v.com/rj/index{}.html",     # # 日剧  8
    "http://www.hao6v.com/mj/index{}.html",     # # 欧美剧 9
    "http://www.hao6v.com/zy/index{}.html",     # # 综艺  10
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


def get_content(dom):

    ul = dom('ul').filter('.list')
    lis = ul('li')
    pattern = re.compile(ur'[\u300a][\S\s]+[\u300b]')  # 获取电影name \u300b = 》;\u300a = 《
    dr = re.compile(r'<[/]*a[^>]*>', re.S)  # 去除 <a></a> 标签
    params = {}
    for li in lis.items():
        params['update_time'] = li('span').html() + " 8:00:00"
        if li('a').find('font').html() is None:
            params['title'] = li('a').html()
        else:
            params['title'] = li('a').find('font').html()
        match = re.search(pattern, params['title'])
        if match:
            params['name'] = match.group()
            pass
        else:
            if u"教你下载" in params['title']:
                # print u'教程'
                pass
                continue
            else:
                print u'错误 ！！！'
                params['name'] = params['title']
                print li.html()

        content_url = li('a').attr('href')
        print content_url
        ssdb_res = ssdb.request('get', ["{}".format(content_url)])
        if ssdb_res.code == 'ok':
            continue
        else:
            pass

        content_res = lrequest.request(content_url)

        print
        content_de = ling_decode(content_res)
        if content_de:
            content_dom = pq(content_de)
        else:
            continue
        params['image_url'] = content_dom('#endText').find('img').eq(0).attr('src')
        ps = content_dom('#endText').find('p')
        content = u""
        for p in ps.items():
            if p.html():
                content = content + u'<p>' + dr.sub('', p.html()) + u'</p>'
        if content_dom('table').html():
            params['content'] = content + u'<p><table border="0" cellspacing="1" cellpadding="10" width="100%">' + content_dom('table').html() + u'</table></p>'
        else:
            params['content'] = content

        params['category_id'] = url_index
        # print params
        response = requests.post("http://localhost:8083/addOneDY", params, timeout=5)
        print response.content
        data = json.loads(response.content)
        if data.get("result") == 200:
            ssdb.request('set', ["{}".format(content_url), "{}".format(params['title'])])
            pass
    pass


def ling_decode(content_res):
    try:
        text_content = unicode(content_res.content, 'gb2312')
    except Exception, ex:
        print ex
        try:
            text_content = unicode(content_res.content, 'gbk')
        except Exception, ex:
            print ex
            try:
                text_content = unicode(content_res.content, 'gb18030')
            except Exception, ex:
                print ex
                try:
                    text_content = unicode(content_res.content, 'utf-8')
                except Exception, ex:
                    print ex
                    text_content = None
    return text_content

if __name__ == '__main__':
    print sys.version
    print time.ctime()
    url_model = int(sys.argv[1])
    url_index = int(sys.argv[2])
    ssdb = SSDB("127.0.0.1", 8888)
    if url_model == 1:
        urls = url
    else:
        urls = url1

    print urls[url_index-1].format("")
    res = lrequest.request(urls[url_index-1].format(""))

    dom_index = pq(ling_decode(res))
    # 页码 判断页数 1/n 格式
    index_str = dom_index('#main .listpage').find('b').html()
    pagination = index_str.split("/")
    page_one = int(pagination[0])  # 当前页数
    page_n = int(pagination[1])  # 总页数
    print page_one
    print page_n
    get_content(dom_index)
    page_one = 31
    while page_one <= 88:
        page_one += 1

        print u'页码：', page_one
        res = lrequest.request(urls[url_index - 1].format("_{}".format(page_one)))
        get_content(pq(ling_decode(res)))

    pass


