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
    "http://www.hao6v.com/dy/index.html",     # # 最新 1
    "http://www.hao6v.com/gydy/index.html",   # # 国语  2
    "http://www.hao6v.com/zydy/index.html",   # # 微电影 3
    "http://www.hao6v.com/gq/index.html",     # # 经典高清    4
    "http://www.hao6v.com/jddy/index.html",   # # 动画电影    5
    "http://www.hao6v.com/3D/index.html",     # # 3 D 电影  6
    "http://www.hao6v.com/dlz/index.html",    # # 国剧  7
    "http://www.hao6v.com/rj/index.html",     # # 日剧  8
    "http://www.hao6v.com/mj/index.html",     # # 欧美剧 9
    "http://www.hao6v.com/zy/index.html",     # # 综艺  10
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
        ssdb_res = ssdb.request('get', ["{}_{}".format(params['name'], category_id)])
        if ssdb_res.code == 'ok':
            if ssdb_res.data == params['title']:
                continue
        else:
            pass

        content_res = lrequest.request(content_url)

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

        params['category_id'] = category_id
        # print params
        response = requests.post("http://localhost:8083/addOneDY", params, timeout=5)
        print response.content
        data = json.loads(response.content)
        if data.get("result") == 200 or data.get("result") == 201 or data.get("result") == 222:
            ssdb.request('set', ["{}_{}".format(params['name'], category_id), "{}".format(params['title'])])
            pass
        # time.sleep(2)
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

    ssdb = SSDB("127.0.0.1", 8888)
    category_id = 1
    for u in url:
        res = lrequest.request(u)
        dom_index = pq(ling_decode(res))
        index_str = dom_index('#main .listpage').find('b').html()
        get_content(dom_index)
        category_id += 1
    pass


