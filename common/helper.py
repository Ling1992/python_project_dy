# -*- coding: UTF-8 -*-
import random
import time
import os
import re
import hashlib


agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]


urls = [
        "{}/dy/index{}.html",  # # 最新 1
        "{}/gydy/index{}.html",  # # 国语  2
        "{}/zydy/index{}.html",  # # 微电影 3
        "{}/gq/index{}.html",  # # 经典高清    4
        "{}/jddy/index{}.html",  # # 动画电影    5
        "{}/3D/index{}.html",  # # 3 D 电影  6
        "{}/dlz/index{}.html",  # # 国剧  7
        "{}/rj/index{}.html",  # # 日剧  8
        "{}/mj/index{}.html",  # # 欧美剧 9
        "{}/zy/index{}.html",  # # 综艺  10
    ]


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'no-cache',
    'Host': 'www.XXX.com',
    'Pragma': 'no-cache'
}


def get_random_agent():
    return random.choice(agent)


def log(logs):
    with open('cache/py_collect_ip.log', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        f.write(' :')
        f.write(logs)
        f.write('\n')
    f.close()
    pass


def str_decode(content, priority='utf-8'):
    """
    将不是文本内容转按 ['utf-8', 'gb2312', 'gbk', 'gb18030'] 解码 至utf-8
    :param content: 
    :param priority: 
    :return: 
    """
    decode_types = ['utf-8', 'gb2312', 'gbk', 'gb18030']

    if priority not in decode_types:
        priority = 'utf-8'

    try:
        return content.decode(priority)
    except Exception as e:
        print('str_decode {} exception {}'.format(priority, e))

    for decode_type in decode_types:
        if decode_type == priority:
            continue
        try:
            return content.decode(decode_type)
        except Exception as e:
            print('str_decode {} exception {}'.format(priority, e))


def rm_a(content):
    """
    去除 文本所包含的 <a></a> a标签
    :param content: 
    :return: 
    """
    dr = re.compile(r'<[/]*a[^>]*>', re.S)
    if content:
        return dr.sub('', content)
    else:
        return content


def rm_blank1(content):
    if content:
        return re.sub(r'\u3000', '', content)
    else:
        return content


def md5(str_):
    return hashlib.md5(str_.encode(encoding='UTF-8')).hexdigest()


def str_to_time(format_, str_):
    return time.mktime(time.strptime(str_, format_))


def re_br(content):
    if content:
        return re.sub(r'<br\s*/>', '', content)
    else:
        return content


def create_pid_file():
    with open('collect_ip.pid', 'w') as f:
        f.write('{}'.format(os.getpid()))
    f.close()


def delete_pid_file():
    os.remove('collect_ip.pid')


def if_exists_pid_file():
    return os.path.exists('collect_ip.pid')
