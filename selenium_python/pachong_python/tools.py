# coding: UTF-8
import os
import sys
import requests
import random
import json
import MySQLdb
from bs4 import BeautifulSoup
reload(sys)
# ip地址 用户名 密码 数据库名称

connection = MySQLdb.connect("120.92.79.213","du","123456","test")
connection.set_character_set('utf8')
cursor = connection.cursor()
"""
conn = pymysql.Connect("120.92.79.213","du","AB1.2.3.","test")
conn.set_charset('utf8')
cur = conn.cursor()
"""


# 请求超时时间
REQUEST_TIME_OUT = 5
'''
USER_AGENTS 随机头信息
'''
USER_AGENTS = [
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
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

"""
reuqst请求发送
:param url: 需要请求的url
"""
def request_url(url='',method='',data=''):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection':'keep-alive',
    }
    #county = get_countiy(url)
    #ip_proexy = get_random_proxy(county)
    #返回内容
    result_text = '请求错误'
    try:
        if 'get' in method:
           # rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,proxies=ip_proexy)
            rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT)
            if rs.status_code == 200:
                result_text = rs.text
        if 'post' in method:
            #rs = requests.post(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT,proxies=ip_proexy)
            rs = requests.get(url, data=data, headers=HEADER, timeout=REQUEST_TIME_OUT)
            if rs.status_code == 200:
                result_text = rs.text
    except Exception, e:
        pass
    return result_text

"""
数据采集
"""
def get_data():
    url = 'http://www.youbian.com/shenghuo/hangzhou_yaodian/'
    rsp_data = request_url(url,'get','')
    soup = BeautifulSoup(rsp_data,'lxml')
    uri = 'http://www.youbian.com/'
    url_list = []
    for span in soup.find_all('span'):
        a = span.find('a',attrs={'target':'_blank'})
        if not a:
            continue
        if a['href']:
            url_list.append(uri+a['href'])

    # 开始数据爬虫信息
    for url in url_list:
        rsp_data = request_url(url,'get','')
        soup = BeautifulSoup(rsp_data,'lxml')
        div_list =  soup.find_all('div',attrs={'class':'xiangqing_leftblock1_b'})
        if len(div_list) == 0:
            continue
        div_tag = div_list[0]
        pharmacy_name = div_tag.find('h3').text
        if not pharmacy_name:
            continue
        dict_data = {}
        dict_data['pharmacy_name'] = pharmacy_name
        for p_index ,p in enumerate(div_tag.find_all('p')):
            if p_index == 0:
                pharmacy_address = ''
                if u'我来补充' in p.text:
                    pharmacy_address = ''
                else:
                    pharmacy_address = p.text
                pharmacy_address = pharmacy_address.replace('地址：','')
                dict_data['pharmacy_address'] = pharmacy_address
            elif p_index == 1:
                pharmacy_phone = ''
                if u'我来补充' in p.text:
                    pharmacy_phone = ''
                else:
                    pharmacy_phone = p.text
                pharmacy_phone = pharmacy_phone.replace('电话：','')
                dict_data['pharmacy_phone'] = pharmacy_phone
        insert_data(dict_data)
        print url
        print json.dumps(dict_data,ensure_ascii=False,indent=4)

"""
数据入库
"""
def insert_data(dict_data):
    pharmacy_name = dict_data['pharmacy_name']
    pharmacy_address = dict_data['pharmacy_address']
    pharmacy_phone = dict_data['pharmacy_phone']
    sql = "INSERT INTO pharmacy_dict VALUES (DEFAULT,'"+pharmacy_name+"','"+pharmacy_address+"','"+pharmacy_phone+"',NOW(),NOW())"
    conn.execute(sql)
    conn.commit()

if __name__ == '__main__':
    get_data()