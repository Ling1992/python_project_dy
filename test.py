#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import configparser
import pyssdb
import re
import pymysql
from pyquery import PyQuery as pq
from common import request
from common import helper


def insert(data1, data2):
    cursor = mysql.cursor()
    try:
        cursor.execute(insert_list_sql.format(**data1))
        data2['id'] = cursor.lastrowid
        cursor.execute(insert_content_sql.format(**data2))
        mysql.commit()
    except Exception as e:
        mysql.rollback()
        if 'Duplicate entry' in e.__str__():
            print(' 重复的 ！！！！')
        elif 'Out of range value for column' in e.__str__():
            print(' 字段超出范围 ！！！')
            helper.log('mysql insert 出错 ！！Exception: {}'.format(e))
        else:
            helper.log('mysql insert Exception: {}'.format(e))
            raise Exception(e)
    finally:
        cursor.close()


def select(url_md5_):
    data = None
    cursor = mysql.cursor()
    try:
        cursor.execute(select_list_sql.format(url_md5_))
        mysql.commit()
        data = cursor.fetchone()
    except Exception as e:
        mysql.rollback()
        if 'Duplicate entry' in e.__str__():
            print(' 重复的 ！！！！')
        elif 'Out of range value for column' in e.__str__():
            print(' 字段超出范围 ！！！')
            helper.log('mysql insert 出错 ！！Exception: {}'.format(e))
        else:
            helper.log('mysql insert Exception: {}'.format(e))
            raise Exception(e)
    finally:
        cursor.close()
    return data


def get_url(index):
    # 处理 url
    if index == 1:
        return url.format(base_url, '')
    else:
        return url.format(base_url, "_{}".format(index))


if __name__ == "__main__":

    # 初始化 配置 ssdb
    config = configparser.ConfigParser()
    config.read('config/test.ini')
    ssdb = pyssdb.Client(host=config.get('local', 'ssdb_host'),
                         port=config.getint('local', 'ssdb_port'))
    request = request.Request(ssdb, config)
    mysql = pymysql.Connect(host=config.get('server', 'mysql_host'),
                            port=config.getint('server', 'mysql_port'),
                            database=config.get('server', 'mysql_db'),
                            user=config.get('server', 'mysql_user'),
                            password=config.get('server', 'mysql_password'),use_unicode=True, charset="utf8")
    insert_list_sql = "INSERT INTO hao6v_list(title, image_url, url_md5, category_id, update_at) VALUES('{title}', '{image_url}', '{url_md5}', {category_id}, {update_at})"
    insert_content_sql = "INSERT INTO hao6v_content(id, content) VALUES({id}, '{content}')"
    select_list_sql = "SELECT * FROM hao6v_list WHERE url_md5 = '{}'"

    base_url = config.get('local', 'base_url')
    post_url = config.get('server', 'post_url')
    today = datetime.date.today()

    # 1、n天前  2、所有
    models = ['day', 'all']
    mode = sys.argv[1]

    if mode not in models:
        raise Exception('模式错误')

    if mode == 'day':
        if len(sys.argv) <= 2:
            day_n = '0'
        else:
            day_n = sys.argv[2]
        print(day_n)
        if not str.isdigit(day_n):
            raise Exception('模式days 参数错误')
    da1 = {}
    da2 = {}
    category_id = 1
    for url in helper.urls:
        page_index = 1
        error_index = 1
        break_two = False
        while True:
            # 获取列表信息
            res = request.get(get_url(page_index))
            if res is False:  # 400 没发现数据网页
                if error_index >= 6:
                    break    # 判断 如果返回 False 超过6次 直接退出 循环
                error_index += 1
            # 处理列表信息
            if res:
                dom = pq(helper.str_decode(res.content, 'gb2312'))
                ul = dom('ul').filter('.list')
                lis = ul('li')
                for li in lis.items():
                    # list: title update_at url
                    update_at = li('span').text()
                    movie_url = li('a').attr('href')
                    da1['title'] = li('a').text()
                    da1['url_md5'] = helper.md5(movie_url)
                    da1['update_at'] = helper.str_to_time('%Y-%m-%d %H:%M:%S', update_at + " 8:00:00")

                    if mode == 'day':  # 模式1
                        base_date = today - datetime.timedelta(days=int(day_n))
                        #  都转成 string 对比，但是 %M %m 是不相等的 所以都转成 datetime.date
                        date = datetime.datetime.strptime(update_at, '%Y-%m-%d').date()
                        if base_date > date:
                            print('no')
                            break_two = True
                            break
                    else:   # 模式2
                        pass
                    res = request.get(movie_url)
                    if res:
                        # # 开始抓取 数据
                        dom = pq(helper.str_decode(res.content, 'gb2312'))
                        endTextDom = dom('#endText')
                        # # 获取第一张图片
                        da1['image_url'] = endTextDom.find('img').eq(0).attr('src')
                        if len(da1['image_url']) > 100:
                            da1['image_url'] = 'url太长！！'
                        da1['category_id'] = category_id
                        content = ''
                        name = ''
                        category = ''
                        # 获取内容
                        ps = endTextDom.find('p')
                        for p in ps.items():
                            p_html = p.html()
                            pss = re.findall('片|名|类|别|主|演', p_html)
                            if len(pss) >= 4:
                                # 获取 片名 译名 类型 存入xunsearch搜索引擎 xunsearch 字段 id name title url
                                p_html = helper.rm_a(p_html)
                                content = content + '<p>' + p_html + '</p>'
                                con = helper.rm_blank1(p_html).split("\n")
                                print(con)
                                for c in con:
                                    if '片名' in c or '译名' in c:  # 片名 译名 类别 name; Translated name; type;
                                        name = name + "*" + helper.re_br(c)[3:]  # # 去除开头的 ['片名', '译名'] 和 结尾的 '<br />'
                                    elif '类别' in c:
                                        category = helper.re_br(c)[3:]
                                print('类型: {}'.format(category))
                                print('片名/译名: {}'.format(name))
                                continue
                            if '下载地址' in p.html():
                                break
                            content = content + p.__html__()
                        content = content + '<hr /> <strong><span style="font-size: large"><span style="color: #ff0000">资源:</span></span></strong>'
                        # 获取下载地址
                        tables = endTextDom.find('table')
                        for table in tables.items():
                            table_html = table.__html__()
                            if u"预告片" in table_html and u"play" in table_html:  # 测试这个...
                                continue
                            content = content + table_html
                        pass     # # 存入数据库  存入搜索引擎
                        da2['content'] = content
                        if not select(da1['url_md5']):
                            insert(da1, da2)
                if break_two:
                    break
            else:
                pass  # #  没有获取数据
            page_index += 1
        category_id += 1
    mysql.close()

