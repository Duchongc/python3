'''
功能: 爬取中关村的手机信息, 并存至数据库, 并进行一些有意思的分析
作者: BlueDamage, 部分bs代码来自rovo98
'''

import re
import os
import time
import random
import pickle
import sqlite3
import requests
from bs4 import BeautifulSoup as bs

# 手机类
class MobilePhone:
    def __init__(self):
        self.name = ''               # 手机名
        self.band = ''               # 品牌
        self.zolPhoneId = ''         # 手机id
        self.picUrl = ''             # 手机图片链接
        # 点评
        self.review = {'点评数':0, '平均评分':0.0, '性价比':0.0, '性能':0.0, '续航':0.0, '外观':0.0, '拍照':0.0, '好评块':0.0, '差评块':''}
        # 价格
        self.price = {'平均售价':0.0, '最高售价':0.0, '最低售价':0.0}
        # 属性
        self.attribute = {}
        # 基本参数
        self.attribute['基本参数'] = {'上市日期':'', '手机类型':'', '其它信息':''}
        # 屏幕
        self.attribute['屏幕'] = {'触摸屏类型':'', '主屏尺寸':'', '主屏分辨率':'', '屏幕像素密度':'', '窄边框':'', '屏幕占比':'', '其它信息':''}
        # 网络
        self.attribute['网络'] = {'4G网络':'', '3G网络':'', '支持频段':'', 'SIM':'', 'WLAN功能':'', '连接与共享':'', '导航':'', '其它信息':''}
        # 外观
        self.attribute['外观'] = {'造型设计':'', '机身颜色':'', '手机尺寸':'', '手机重量':'', '机身材质':'',
                            '操作类型':'', '感应器类型':'','指纹识别设计':'', '机身接口':'', '其它信息':''}
        # 硬件
        self.attribute['硬件'] = {'操作系统':'', '用户界面':'', '核心数':0, 'CPU型号':'', 'CPU频率':'', 'GPU型号':'',
                             'RAM容量':'', 'ROM容量':'', '存储卡':'', '扩展类型':'', '电池类型':'', '电池容量':0.0, '其它信息':''}
        # 摄像头
        self.attribute['摄像头'] = {'摄像头类型':'', '前置摄像头':'', '后置摄像头':'', '传感器类型':'', '传感器型号':'', '闪光灯':'',
                                '光圈':'', '摄像头特色':'', '视频拍摄':'', '拍照功能':'', '其它信息':''}
        # 服务与支持
        self.attribute['服务与支持'] = {'音频支持':'', '视频支持':'', '图片支持':'', '多媒体技术':'', '常用功能':'', '商务功能':'', '服务特色':'', '其它信息':''}
        # 手机附件
        self.attribute['手机附件'] = {'包装清单':'', '其它信息':''}
        # 保修信息
        self.attribute['保修信息'] = {'保修政策':'', '质保时间':'', '质保备注':'', '客服电话':'', '电话备注':'', '详细内容':'', '其它信息':''}

# 代理类
class Proxy:
    MAXTRYTIME = 5
    def __init__(self):
        # 请求头
        self.headers = {
            "Host": "detail.zol.com.cn",
            "Referer": "https://detail.zol.com.cn/",
            'User-Agent': '',
            'Connection': 'keep-alive'
        }
        self.userAgents = eval(open('E:\BaiduNetdiskDownload\中关村手机信息爬取\手机小虫_userAgents.txt', 'r', encoding='utf-8').read())

    # 爬取并返回url的内容, 成功爬取某url的同时
    # 新建一个temp.html文件
    def getPage(self, url):
        failTime = 0
        while True:
            try:
                time.sleep(1)
                self.headers['User-Agent'] = random.choice(self.userAgents)
                r = requests.get(url, headers=self.headers, timeout=15)
                r.encoding = 'gb18030'

                with open('temp.html', 'w', encoding = 'gb18030') as temp:
                    temp.write(r.text)
                # 内容过少, 应该没有成功地打开网页
                if len(r.text) < 100:
                    continue

                return r.text
            except:
                failTime += 1
                if failTime == self.MAXTRYTIME:
                    print(url)
                    return ''

# 数据库类
class DataBase:
    dbName = '手机小虫.db'
    cursor = ''
    connet = ''
    # 手机信息总数
    numOfPhones = 0
    def __init__(self):
        # 连接到数据库
        self.connet = sqlite3.connect(self.dbName)
        self.cursor = self.connet.cursor()
        # 建表
        self.creatTables()
        # 计算数据库手机信息的数量
        self.numOfPhones = len(list(self.cursor.execute('select * from phone')))

    # 建表
    def creatTables(self):
        # 表 - 手机基本信息
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS phone
                    (ID                 INT   PRIMARY KEY NOT NULL,
                     phone_name         TEXT     ,
                     phone_band         TEXT     ,
                     phone_timeToMarket TEXT     ,
                     phone_zolPhoneId   TEXT     ,
                     phone_picUrl       TEXT     );
                  ''')
        # 表 - 评分
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS review
                (ID                   INT   PRIMARY KEY NOT NULL,
                 review_belong        TEXT     ,
                 review_num           INT      ,
                 review_aveMarks      REAL     ,
                 review_costPerform   REAL     ,
                 review_performance   REAL     ,
                 review_continuation  REAL     ,
                 review_shape         REAL     ,
                 review_camera        REAL     ,
                 review_goodWords     TEXT     ,
                 review_badWords     TEXT      );
              ''')
        # 表 - 价格
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS price
                    (ID           INT   PRIMARY KEY NOT NULL,
                     price_belong TEXT    ,
                     price_top    TEXT    ,
                     price_ave    TEXT    ,
                     price_low    TEXT    );
                  ''')
        # 表 - 基础信息
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS baseInfo
                    (ID                     INT  PRIMARY KEY NOT NULL,
                     baseInfo_belong        TEXT ,
                     baseInfo_timeToMarket  TEXT ,
                     baseInfo_phoneType     TEXT ,
                     baseInfo_others        TEXT );
                  ''')
        # 表 - 屏幕
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS screen
                    (ID                 INT  PRIMARY KEY NOT NULL,
                     screen_belong      TEXT ,
                     screen_type        TEXT ,
                     screen_size        TEXT ,
                     screen_resolution  TEXT ,
                     screen_density     TEXT ,
                     screen_bezel       TEXT ,
                     screen_percentage  TEXT ,
                     screen_others      TEXT );
                  ''')
        # 表 - 网络
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS internet
                    (ID                   INT  PRIMARY KEY NOT NULL,
                     internet_belong      TEXT ,
                     internet_four        TEXT ,
                     internet_three       TEXT ,
                     internet_support     TEXT ,
                     internet_sim         TEXT ,
                     internet_wlan        TEXT ,
                     internet_navigation  TEXT ,
                     internet_conshare    TEXT ,
                     internet_others      TEXT );
                  ''')
        # 表 - 硬件
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hardware
                    (ID                     INT  PRIMARY KEY NOT NULL,
                     hardware_belong        TEXT ,
                     hardware_os            TEXT ,
                     hardware_ui            TEXT ,
                     hardware_coreNum       TEXT ,
                     hardware_cpuVersion    TEXT ,
                     hardware_cpuRate       TEXT ,
                     hardware_gpuVersion    TEXT ,
                     hardware_ram           TEXT ,
                     hardware_rom           TEXT ,
                     hardware_memoryCard    TEXT ,
                     hardware_extCapacity   TEXT ,
                     hardware_batryType     TEXT ,
                     hardware_batryCapacity TEXT ,
                     hardware_others        TEXT );
                  ''')
        # 表 - 摄像头
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS camera
                    (ID                     INT  PRIMARY KEY NOT NULL,
                     camera_belong          TEXT ,
                     camera_type            TEXT ,
                     camera_back            TEXT ,
                     camera_front           TEXT ,
                     camera_sensorType      TEXT ,
                     camera_sensorVersion   TEXT ,
                     camera_flashlight      TEXT ,
                     camera_aperture        TEXT ,
                     camera_feature         TEXT ,
                     camera_videoCapture    TEXT ,
                     camera_function        TEXT ,
                     camera_others          TEXT );
                  ''')
        # 表 - 外形
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shape
                    (ID                 INT  PRIMARY KEY NOT NULL,
                     shape_belong       TEXT ,
                     shape_design       TEXT ,
                     shape_color        TEXT ,
                     shape_size         TEXT ,
                     shape_weight       TEXT ,
                     shape_material     TEXT ,
                     shape_operType     TEXT ,
                     shape_sensors      TEXT ,
                     shape_fingerprint  TEXT ,
                     shape_interface    TEXT ,
                     shape_others       TEXT );
                  ''')
        # 表 - 服务与支持
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS service
                    (ID                   INT  PRIMARY KEY NOT NULL,
                     service_belong       TEXT ,
                     service_music        TEXT ,
                     service_video        TEXT ,
                     service_picture      TEXT ,
                     service_media        TEXT ,
                     service_commomFun    TEXT ,
                     service_businessFun  TEXT ,
                     service_feature      TEXT ,
                     service_others       TEXT );
                  ''')
        # 表 - 附件
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attachment
                    (ID                 INT  PRIMARY KEY NOT NULL,
                     attachment_belong  TEXT ,
                     attachment_list    TEXT ,
                     attachment_others  TEXT );
                  ''')
        # 表 - 保修信息
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warranty
                    (ID                     INT  PRIMARY KEY NOT NULL,
                     warranty_belong        TEXT ,
                     warranty_policy        TEXT ,
                     warranty_deadline      TEXT ,
                     warranty_remarks       TEXT ,
                     warranty_media         TEXT ,
                     warranty_phoneNumber   TEXT ,
                     warranty_phoneRemarks  TEXT ,
                     warranty_others        TEXT );
                  ''')

    # 存至数据库
    def save(self, mobilePhoneList):
        # 遍历手机列表
        for m in mobilePhoneList:
            # 添加信息至 表 - 手机基本信息
            self.cursor.execute("INSERT INTO phone (ID, phone_name, phone_band, phone_timeToMarket, phone_zolPhoneId, phone_picUrl) VALUES (?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.name, m.band, m.attribute['基本参数']['上市日期'], m.zolPhoneId, m.picUrl))

            # 添加信息至 表 - 评分
            self.cursor.execute("INSERT INTO review (ID, review_belong, review_num, review_aveMarks, review_costPerform, review_performance, review_continuation, review_shape, review_camera, review_goodWords, review_badWords) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.review['点评数'], m.review['平均评分'], m.review['性价比'], m.review['性能'], m.review['续航'], m.review['外观'], m.review['拍照'], m.review['好评块'], m.review['差评块']))

            # 添加信息至 表 - 价格
            self.cursor.execute("INSERT INTO price (ID, price_belong, price_top, price_ave, price_low) VALUES (?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.price['最高售价'], m.price['平均售价'], m.price['最低售价']))

            # 添加信息至 表 - 基本参数
            self.cursor.execute("INSERT INTO baseInfo (ID, baseInfo_belong, baseInfo_timeToMarket, baseInfo_phoneType, baseInfo_others) VALUES (?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['基本参数']['上市日期'], m.attribute['基本参数']['手机类型'], m.attribute['基本参数']['其它信息']))

            # 添加信息至 表 - 屏幕
            self.cursor.execute("INSERT INTO screen (ID, screen_belong, screen_type, screen_size, screen_resolution, screen_density, screen_bezel, screen_percentage, screen_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['屏幕']['触摸屏类型'], m.attribute['屏幕']['主屏尺寸'], m.attribute['屏幕']['主屏分辨率'], m.attribute['屏幕']['屏幕像素密度'], m.attribute['屏幕']['窄边框'], m.attribute['屏幕']['屏幕占比'], m.attribute['屏幕']['其它信息']))


            # 添加信息至 表 - 网络
            self.cursor.execute("INSERT INTO internet (ID, internet_belong, internet_four, internet_three, internet_support, internet_sim, internet_wlan, internet_navigation, internet_conshare, internet_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['网络']['4G网络'], m.attribute['网络']['3G网络'], m.attribute['网络']['支持频段'], m.attribute['网络']['SIM'], m.attribute['网络']['WLAN功能'], m.attribute['网络']['连接与共享'], m.attribute['网络']['导航'], m.attribute['网络']['其它信息']))

            # 添加信息至 表 - 硬件
            self.cursor.execute("INSERT INTO hardware (ID, hardware_belong, hardware_os, hardware_ui, hardware_coreNum, hardware_cpuVersion, hardware_cpuRate, hardware_gpuVersion, hardware_ram, hardware_rom, hardware_memoryCard, hardware_extCapacity, hardware_batryType, hardware_batryCapacity, hardware_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['硬件']['操作系统'], m.attribute['硬件']['用户界面'], m.attribute['硬件']['核心数'], m.attribute['硬件']['CPU型号'], m.attribute['硬件']['CPU频率'], m.attribute['硬件']['GPU型号'], m.attribute['硬件']['RAM容量'], m.attribute['硬件']['RAM容量'], m.attribute['硬件']['存储卡'], m.attribute['硬件']['扩展类型'], m.attribute['硬件']['电池类型'], m.attribute['硬件']['电池容量'], m.attribute['硬件']['其它信息']))
            # 添加信息至 表 - 摄像头
            self.cursor.execute("INSERT INTO camera (ID, camera_belong, camera_type, camera_back, camera_front, camera_sensorType, camera_sensorVersion, camera_flashlight, camera_aperture, camera_feature, camera_videoCapture, camera_function, camera_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['摄像头']['摄像头类型'], m.attribute['摄像头']['前置摄像头'], m.attribute['摄像头']['后置摄像头'], m.attribute['摄像头']['传感器类型'], m.attribute['摄像头']['传感器型号'], m.attribute['摄像头']['闪光灯'], m.attribute['摄像头']['光圈'], m.attribute['摄像头']['摄像头特色'], m.attribute['摄像头']['视频拍摄'], m.attribute['摄像头']['拍照功能'], m.attribute['摄像头']['其它信息']))


            # 添加信息至 表 - 外形
            self.cursor.execute("INSERT INTO shape (ID, shape_belong, shape_design, shape_color, shape_size, shape_weight, shape_material, shape_operType, shape_sensors, shape_fingerprint, shape_interface, shape_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['外观']['造型设计'], m.attribute['外观']['机身颜色'], m.attribute['外观']['手机尺寸'], m.attribute['外观']['手机重量'], m.attribute['外观']['机身材质'], m.attribute['外观']['操作类型'], m.attribute['外观']['感应器类型'], m.attribute['外观']['指纹识别设计'], m.attribute['外观']['机身接口'], m.attribute['外观']['其它信息']))

            # 添加信息至 表 - 服务
            self.cursor.execute("INSERT INTO service (ID, service_belong, service_music, service_video, service_picture, service_media, service_commomFun, service_businessFun, service_feature, service_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['服务与支持']['音频支持'], m.attribute['服务与支持']['视频支持'], m.attribute['服务与支持']['图片支持'], m.attribute['服务与支持']['多媒体技术'], m.attribute['服务与支持']['常用功能'], m.attribute['服务与支持']['商务功能'], m.attribute['服务与支持']['服务特色'], m.attribute['服务与支持']['其它信息']))

            # 添加信息至 表 - 手机附件
            self.cursor.execute("INSERT INTO attachment (ID, attachment_belong, attachment_list, attachment_others) VALUES (?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['手机附件']['包装清单'], m.attribute['手机附件']['其它信息']))


            # 添加信息至 表 - 保修信息
            self.cursor.execute("INSERT INTO warranty (ID, warranty_belong, warranty_policy, warranty_deadline, warranty_remarks, warranty_media, warranty_phoneNumber, warranty_phoneRemarks, warranty_others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.numOfPhones+1, m.zolPhoneId, m.attribute['保修信息']['保修政策'], m.attribute['保修信息']['质保时间'], m.attribute['保修信息']['质保备注'], m.attribute['保修信息']['客服电话'], m.attribute['保修信息']['电话备注'], m.attribute['保修信息']['详细内容'], m.attribute['保修信息']['其它信息']))
            self.connet.commit()
            self.numOfPhones += 1

    # 数据分析
    def analyzeData(self):
        print('数据爬取自zol手机, 某些分析定会有出入, 勿介意\n')
        print('dif :荣耀6p联通版16g版 与 荣耀6p联通版32g版 为两款手机')
        print('same:荣耀6p联通版16g版 与 荣耀6p联通版32g版 为同一款手机\n')
        # 提取手机名 手机品牌 上市日期 手机售价
        self.cursor.execute('select phone.phone_name, phone.phone_band, phone.phone_timeToMarket, price.price_ave from phone, price where phone.phone_zolPhoneId=price.price_belong')
        phoneList = self.cursor.fetchall()

        # 排除概念手机, 未上市, 停产等无金额的手机
        phoneList = [item for item in phoneList if item[-1].replace('.', '').isdecimal()]

        # 问题一: 手机出最多的前十个品牌是
        # 荣耀6p联通版16g版 与 荣耀6p联通版32g版 为两款手机
        print('问题一: 手机出最多的前五个品牌是?_dif')
        band_di_dif = {}
        for p in phoneList:
            phoneName, phoneBand = p[0], p[1]
            phonePrice = p[3]
            if phoneBand not in band_di_dif.keys():
                band_di_dif[phoneBand] = {}
                band_di_dif[phoneBand]['型号'] = [phoneName]
                band_di_dif[phoneBand]['价格'] = [phonePrice]
            else:
                band_di_dif[phoneBand]['型号'] += [phoneName]
                band_di_dif[phoneBand]['价格'] += [phonePrice]

        li = sorted(band_di_dif.keys(), key=lambda band:len(band_di_dif[band]['型号']), reverse = True)[:5]
        for bandName in li:
            print('\t{}:\t{}款'.format(bandName, len(band_di_dif[bandName]['型号'])))

        # 荣耀6p联通版16g版 与 荣耀6p联通版32g版 为同一款手机
        print('\n问题二: 手机出最多的前五个品牌是?_same')
        band_di_same = {}
        for p in phoneList:
            phoneName, phoneBand = p[0], p[1]
            phonePrice = p[3]
            # 去除版本信息
            phoneName = phoneName.split('（')[0]
            if phoneBand not in band_di_same.keys():
                band_di_same[phoneBand] = {}
                band_di_same[phoneBand]['型号'] = [phoneName]
                band_di_same[phoneBand]['价格'] = [phonePrice]
            else:
                if phoneName not in band_di_same[phoneBand]['型号']:
                    band_di_same[phoneBand]['型号'] += [phoneName]
                    band_di_same[phoneBand]['价格'] += [phonePrice]
        li = sorted(band_di_same.keys(), key=lambda band:len(band_di_same[band]['型号']), reverse = True)[:5]

        for bandName in li:
            print('\t{}:\t{}款'.format(bandName, len(band_di_same[bandName]['型号'])))

        # 问题三: 2017年, 哪个品牌出的手机最多
        print('\n问题三: 201x年, 哪个品牌出的手机最多?_same')
        for year in ['2017', '2016', '2015']:
            year_phoneList = [p for p in phoneList if year in p[2]]
            year_band_di = {}
            for p in year_phoneList:
                phoneName, phoneBand = p[0], p[1]
                # 去除版本信息
                phoneName = phoneName.split('（')[0]
                if phoneBand not in year_band_di.keys():
                    year_band_di[phoneBand] = [phoneName]
                else:
                    if phoneName not in year_band_di[phoneBand]:
                        year_band_di[phoneBand] += [phoneName]
            bandName = sorted(year_band_di.keys(), key=lambda key: len(year_band_di[key]), reverse=True)[0]
            print('\t{}: {}:\t{}款'.format(year, bandName, len(year_band_di[bandName])))

        # 问题四: 有哪些奇葩的品牌名?
        # 品牌品怪异的, 一般少见
        # 所以出的手机应该很少, 现选择仅出3(<=3)台手机的品牌
        print('\n问题四: 有哪些奇葩的品牌名?_same')
        li = sorted(band_di_same.keys(), key=lambda band:len(band_di_same[band]['型号']))
        li = [bandName for bandName in li if len(band_di_same[bandName]['型号']) <= 3]
        for index, bandName in enumerate(li):
            print('	{}'.format(bandName), end='')
            if (index+1) % 6 == 0:
                print()

        # 问题五:  201x年,出的手机中, 目前平均售价最高/低的是
        print('\n\n问题五: 201x年出的手机中, 目前平均售价最高/低的是哪几个品牌?_same')
        for year in ['2017', '2016', '2015', '2014', '2013']:
            year_band_di_same = {}
            for p in phoneList:
                timeToMrrket = p[2]
                if year in timeToMrrket:
                    phoneName, phoneBand = p[0], p[1]
                    phonePrice = p[3]
                    # 去除版本信息
                    phoneName = phoneName.split('（')[0]
                    if phoneBand not in year_band_di_same.keys():
                        year_band_di_same[phoneBand] = {}
                        year_band_di_same[phoneBand]['型号'] = [phoneName]
                        year_band_di_same[phoneBand]['价格'] = [phonePrice]
                    else:
                        if phoneName not in year_band_di_same[phoneBand]['型号']:
                            year_band_di_same[phoneBand]['型号'] += [phoneName]
                            year_band_di_same[phoneBand]['价格'] += [phonePrice]

            year_band_ave_price = []
            for band in year_band_di_same:
                # 该品牌的平均价格
                avePrice = sum([round(float(price), 3) for price in year_band_di_same[band]['价格']]) / len(year_band_di_same[band]['型号'])
                avePrice = round(avePrice, 3)
                year_band_ave_price.append([band, avePrice])
            year_band_ave_price = sorted(year_band_ave_price, key=lambda li: li[1])
            print(year+': ')
            print('\t最低价:', '  '.join(['{}: {}'.format(ele[0], ele[1]) for ele in year_band_ave_price[:6:]]))
            print('\t最高价:', '  '.join(['{}: {}'.format(ele[0], ele[1]) for ele in year_band_ave_price[-6::][::-1]]))


        # 提取手机名 手机品牌 上市日期 手机点评.* 手机售价
        self.cursor.execute('select phone.phone_name, phone.phone_band, phone.phone_timeToMarket, review.review_aveMarks, review.review_num, review.review_goodWords, review.review_badWords, price.price_ave from phone, review, price where phone.phone_zolPhoneId=review.review_belong and phone.phone_zolPhoneId=price.price_belong')
        phoneList = self.cursor.fetchall()
        # 排除概念手机, 未上市, 停产等无金额的手机
        phoneList = [item for item in phoneList if item[-1].replace('.', '').isdecimal()]


        # 问题六: 201x年, 哪几个品牌的手机, 平均评分最高
        print('\n问题六: 201x年, 哪几个品牌的手机, 平均评分最高/低?_same')
        # 存在问题 荣耀6p32g 荣耀6p16g为同一款手机, 在此会第一款出现的荣耀6p版本的点评代表荣耀6p
        for year in ['2017', '2016', '2015']:
            year_band_di_same = {}
            for p in phoneList:
                timeToMrrket = p[2]
                if year in timeToMrrket:
                    phoneName, phoneBand = p[0], p[1]
                    reviewAveMark, reviewNum = p[3], p[4]
                    goodWords, badWords = p[5], p[6]
                    # 排除点评数小于100的手机
                    if reviewNum <= 100:
                        continue
                    # 排除评分为0的手机
                    if float(reviewAveMark) == 0.0:
                        continue
                    # 去除版本信息
                    phoneName = phoneName.split('（')[0]
                    if phoneBand not in year_band_di_same.keys():
                        year_band_di_same[phoneBand] = {}
                        year_band_di_same[phoneBand]['型号'] = [phoneName]
                        year_band_di_same[phoneBand]['评分'] = [reviewAveMark]
                        year_band_di_same[phoneBand]['好评块'] = [goodWords]
                        year_band_di_same[phoneBand]['差评块'] = [badWords]
                    else:
                        if phoneName not in year_band_di_same[phoneBand]['型号']:
                            year_band_di_same[phoneBand]['型号'] += [phoneName]
                            year_band_di_same[phoneBand]['评分'] += [reviewAveMark]
                            year_band_di_same[phoneBand]['好评块'] += [goodWords]
                            year_band_di_same[phoneBand]['差评块'] += [badWords]

            year_band_ave_reviewMark = []
            for band in year_band_di_same:
                # 该品牌的平均价格
                aveReviewMark = sum([round(float(aveMark), 3) for aveMark in year_band_di_same[band]['评分']]) / len(year_band_di_same[band]['型号'])
                aveReviewMark = round(aveReviewMark, 3)
                year_band_ave_reviewMark.append([band, aveReviewMark])
                year_band_ave_reviewMark = sorted(year_band_ave_reviewMark, key=lambda li: li[1])
            print(year + ': ')

            print('\t最低评分:', '  '.join(['{}: {}'.format(ele[0], ele[1]) for ele in year_band_ave_reviewMark[:6:]]))
            print('\t最高评分:', '  '.join(['{}: {}'.format(ele[0], ele[1]) for ele in year_band_ave_reviewMark[-6::][::-1]]))

        # 问题七: 201x年, 点评人数/好评数/差评数最多的是哪款手机, 哪几款品牌
        print('\n问题七: 201x年, 好评数/差评数最多的是哪款手机, 哪几款品牌?_same')
        # 存在问题 荣耀6p32g 荣耀6p16g为同一款手机, 在此会第一款出现的荣耀6p版本的点评代表荣耀6p
        for year in ['2017', '2016', '2015']:
            year_band_di_same = {}
            for p in phoneList:
                timeToMrrket = p[2]
                if year in timeToMrrket:
                    phoneName, phoneBand = p[0], p[1]
                    reviewAveMark, reviewNum = p[3], p[4]
                    goodWords, badWords = p[5], p[6]
                    # 排除点评数小于100的手机
                    if reviewNum <= 100:
                        continue
                    # 排除评分为0的手机
                    if float(reviewAveMark) == 0.0:
                        continue
                    # 好评数, 差评数
                    goodNum = re.findall(re.compile('\d+'), goodWords)
                    badNum = re.findall(re.compile('\d+'), badWords)
                    # 去除版本信息
                    phoneName = phoneName.split('（')[0]
                    if phoneBand not in year_band_di_same.keys():
                        year_band_di_same[phoneBand] = {}
                        year_band_di_same[phoneBand]['型号'] = [phoneName]
                        year_band_di_same[phoneBand]['好评数'] = [goodNum]
                        year_band_di_same[phoneBand]['差评数'] = [badNum]
                    else:
                        if phoneName not in year_band_di_same[phoneBand]['型号']:
                            year_band_di_same[phoneBand]['型号'] += [phoneName]
                            year_band_di_same[phoneBand]['好评数'] += [goodNum]
                            year_band_di_same[phoneBand]['差评数'] += [badNum]

            print(year + ': ')
            year_band_ave_reviewNum = {}
            for comType in ['好评数', '差评数']:
                year_band_ave_reviewNum[comType] = []
                maxPhone = ''
                for band in year_band_di_same:
                    for index, phoneName in enumerate(year_band_di_same[band]['型号']):
                        comNum = sum(int(eachMark) for eachMark in year_band_di_same[band][comType][index])
                        if maxPhone == '':
                            maxPhone = [phoneName, comNum]
                        if comNum > maxPhone[1]:
                            maxPhone = [phoneName, comNum]
                    # 该品牌的平均点评数
                    aveReviewNum = sum([sum(int(eachMark) for eachMark in comNum) for comNum in year_band_di_same[band][comType]]) / len(year_band_di_same[band]['型号'])
                    aveReviewNum = round(aveReviewNum, 3)
                    year_band_ave_reviewNum[comType].append([band, aveReviewNum])
                    year_band_ave_reviewNum[comType]  = sorted(year_band_ave_reviewNum[comType] , key=lambda li: li[1])

                print('\t品牌 最多{}: {}'.format(comType, '  '.join(['{}: {}'.format(ele[0], ele[1]) for ele in year_band_ave_reviewNum[comType] [-6::][::-1]])))
                print('\t手机 最多{}: {}  数量: {}'.format(comType, maxPhone[0], maxPhone[1]))

# 爬取zol手机信息类
class crawlZol:
    def __init__(self):
        # 实例一个代理类
        self.proxy = Proxy()
        # 临时手机变量
        self.tempMobilePhone = None
        # 已爬取的手机列表
        self.phoneList = []
        # 实例一个数据库类
        self.DB = DataBase()
        # 加载pk文件
        if os.path.exists('phone.pk'):
            self.phoneList = pickle.load(open('phone.pk', 'rb'))
        else:
            open('phone.pk', 'wb').close()
            self.phoneList = []
        print('已爬取{}台手机的信息'.format(len(self.phoneList)))

    # 启动
    def start(self):
        phoneIdList = []

        # 按页码爬取简略手机信息页面, 并获取所有的手机id
        for pageId in range(1, 108):
            print('\n第{0:03d}页'.format(pageId))
            humblePhonePageUrl = 'http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_2_0_{}.html'.format(pageId)
            briefPhoneInfoHtml = self.proxy.getPage(humblePhonePageUrl)
            # 手机id集
            phoneIdList += self.analyzeBriefPhoneInfo(briefPhoneInfoHtml)
        phoneIdList = list(set(phoneIdList))
        print('共有个{}手机信息待爬取\n'.format(len(phoneIdList)))

        index = 0
        # 遍历手机id集
        for phoneId in  phoneIdList:
            index += 1

            # 检测当前手机是否已被爬取
            flag = False
            for p in self.phoneList:
                if phoneId == p.zolPhoneId:
                    print('{0:03d}_已爬取 {1}'.format(index, p.name))
                    flag = True
                    break
            if flag:
                continue

            # 临时手机实例
            self.tempMobilePhone = MobilePhone()
            # 赋值 - 手机id
            self.tempMobilePhone.zolPhoneId = phoneId
            print('\n'+'http://detail.zol.com.cn/cell_phone/index{}.shtml'.format(phoneId))

            # 爬取手机的综述介绍页面
            curPhoneMainHtml = self.proxy.getPage('http://detail.zol.com.cn/cell_phone/index{}.shtml'.format(phoneId))

            # 老旧页面
            if '综述介绍' not in curPhoneMainHtml and '评测行情' not in curPhoneMainHtml:
                print('老旧界面, 信息不完整, 不爬取!               -_-')
                continue

            if '您访问的页面已被删除或不存在' in curPhoneMainHtml:
                print('您访问的页面已被删除或不存在')
                continue

            # 获取前置id
            frontId = re.findall(re.compile('http://wap.zol.com.cn/(.*?)/(.*?)/index.html'), curPhoneMainHtml)[0][0]

            # 赋值 - 手机品牌 手机名
            soup = bs(curPhoneMainHtml, 'html.parser')
            try:
                self.tempMobilePhone.name = soup.find('div', attrs={'class':'page-title clearfix'}).find('h1').text
            except:
                self.tempMobilePhone.name = soup.find('div', attrs={'class':'page-title clearfix'}).find('span').text

            self.tempMobilePhone.band = re.findall(re.compile('target="_self">(.*?)手机</a>'), curPhoneMainHtml)[1]

            print('{0:03d}_品牌: {1:5s}\t型号: {2}'.format(index, self.tempMobilePhone.band, self.tempMobilePhone.name) )

            # 赋值 - 手机图片介绍url
            self.tempMobilePhone.picUrl = 'http://detail.zol.com.cn/{}/{}/pic.shtml'.format(frontId, phoneId)

            # 获手机取售卖状态
            # 有￥, 代表在售, 有报价
            # 无￥, 手机有可能为概念产品或已停产或即将上市

            # 价格列表
            priceList = []
            # 本地参考价
            localPrice = soup.find('div', attrs={'class': 'product-price-info'}, recursive=True)
            # 参考报价有价格, 正在售卖
            if '￥' in str(localPrice):
                # 定位到参考报价/在售状态
                localPrice = localPrice.find_all('b')[1].text
                if '万' in localPrice:       # 单位为万
                    localPrice = float(localPrice.replace('万', '')) * 10000
                priceList.append(int(localPrice))
                # 获取所有的商家报价
                try:
                    priceInfo = soup.find_all('div', attrs={'class': 'product-merchant-price clearfix'}, recursive=True)[0]
                    # 不同商家价格
                    b2cPrice = priceInfo.find_all('ul', attrs={'class': 'b2c-price-list clearfix'})[0].find_all('li')
                    # 遍历所有商家报价ul, 并提取其价格
                    for price in b2cPrice:
                        p = price.find_all('a')[1].text
                        p = int(p.replace('￥', ''))
                        priceList.append(p)
                except:
                    pass
                # 赋值 - 手机价格
                self.tempMobilePhone.price['平均售价'] = sum(priceList) / len(priceList)
                self.tempMobilePhone.price['最高售价'] = max(priceList)
                self.tempMobilePhone.price['最低售价'] = min(priceList)
            else:
                # 手机未正式开始售卖
                print('{}!                           -_-\n'.format(localPrice.find('b').text))
                self.tempMobilePhone.price['平均售价'] = localPrice.find('b').text
                self.tempMobilePhone.price['最高售价'] = localPrice.find('b').text
                self.tempMobilePhone.price['最低售价'] = localPrice.find('b').text

            # 爬取参数页面
            try:
                paramUrl = 'http://detail.zol.com.cn/{}/{}/param.shtml'.format(frontId, phoneId)
                paramHtml = self.proxy.getPage(paramUrl)
                self.analyzeParam(paramHtml)
            except:
                print('参数页面爬取失败!                         -_-')
                continue

            # 爬取评分页面
            try:
                reviewUrl = 'http://detail.zol.com.cn/{}/{}/review.shtml'.format(frontId, phoneId)
                reviewHtml = self.proxy.getPage(reviewUrl)
                self.analyzeReview(reviewHtml)
            except:
                print('评分页面爬取失败!                         -_-')
                continue

            # 添加实例至列表
            self.phoneList.append(self.tempMobilePhone)
            # 存至pk文件
            with open('phone.pk', 'wb') as pkFile:
                pickle.dump(self.phoneList, pkFile)

        # 输出到数据库
        self.DB.save(self.phoneList)

    # 分析点评页面
    def analyzeReview(self, reviewHtml):
        '''
        分析点评页面, 提取评分人数, 评分情况及评论块, 并赋值给临时手机实例

        :param html: 某手机的评分html
        :return: None
        '''
        soup = bs(reviewHtml,'html.parser')
        goodWords = []   # 好评
        badWords = []    # 差评
        scoreDetail = [] # 评分细节

        #totalNum = int(re.findall(re.compile('<span>(.*?)人评分</span>'), reviewHtml)[0])
        #totalNum = int(re.findall(re.compile('概括 <strong>(.*?)</strong> 名网友的点评内容'), reviewHtml)[0])

        # 评分人数
        try:
            totalNum = int(re.findall(re.compile('</i>点评<em>(.*?)</em>'), reviewHtml)[0].replace('(', '').replace(')', ''))
        except:
            totalNum = 0

        try:
            # 平均评分
            totalScore = soup.find_all('div',attrs={'class':'total-score'},recursive=True)[0].find('strong').text
            scores = soup.find_all('ul',attrs={'class':'canvas bar-5'},recursive=True)[0].find_all('div')
            # 具体评分
            for i in range(0,len(scores)):
                if i % 2 == 0 :
                    scoreDetail.append(float(re.sub(r'\n','',scores[i].text)))
        except:
            # 找不到评分
            totalScore = 0.0
            # 具体评分
            scoreDetail = [0.0, 0.0, 0.0, 0.0, 0.0]

        # 定位到评论块
        commentWords = soup.find('div',attrs={'id':'J_CommentWords'},recursive=True)
        # 存在好评块
        if 'good-words' in str(commentWords):
            # 定位到 好评块div
            gWords = soup.find('div', attrs={'class':'good-words'}, recursive=True)
            # 定位到 具体的好评无序列表
            gWords = gWords.find('ul', attrs={'class': 'words-list clearfix'}, recursive=True)
            # 好评块
            for eachGood in gWords.find_all('li'):
                goodWords.append(eachGood.text)

        # 存在差评块
        if 'bad-words' in str(commentWords):
            # 定位到 差评块div
            bWords = soup.find('div', attrs={'class':'bad-words'}, recursive=True)
            # 定位到 具体的差评无序列表
            bWords = bWords.find('ul', attrs={'class': 'words-list clearfix'}, recursive=True)
            # 差评块
            for eachBad in bWords.find_all('li'):
                badWords.append(eachBad.text)

        # 赋值 - 点评
        self.tempMobilePhone.review['点评数'] = totalNum
        self.tempMobilePhone.review['平均评分'] = totalScore
        self.tempMobilePhone.review['性价比'] = scoreDetail[0]
        self.tempMobilePhone.review['性能'] = scoreDetail[1]
        self.tempMobilePhone.review['续航'] = scoreDetail[2]
        self.tempMobilePhone.review['外观'] = scoreDetail[3]
        self.tempMobilePhone.review['拍照'] = scoreDetail[4]
        self.tempMobilePhone.review['好评块'] = ' '.join(goodWords)
        self.tempMobilePhone.review['差评块'] = ' '.join(badWords)

    # 分析参数页面
    def analyzeParam(self, paramHtml):
        '''
        分析参数页面, 制作属性字典并赋值给临时手机实例

        :param html: 某手机的参数html
        :return: None
        '''
        soup = bs(paramHtml,'html.parser')

        # 根据th, 提取参数页面中含有的大属性名
        bigAttrList = [attr.text for attr in soup.find_all('th', recursive=True)]
        # 根据param-content, 提取每个大属性对应的 小属性块
        attr_contents = soup.find_all('div', attrs={'class':'param-content'},recursive=True)

        # 分析参数页面, 构造属性字典
        # attrs = {'基本参数':{'上市日期':'', '手机类型':''}....}
        attrs = {}
        # 遍历每一个 小属性块
        for index, eachInfo in enumerate(attr_contents):
            # 在小属性块中提取span标签
            info = eachInfo.find_all('span')
            # 当前大属性对应的 小数属性字典
            # {'上市日期':'', '手机类型':''}
            smallAttr = {}
            # 遍历span标签
            for i in range(0, len(info)-1):
                # 奇数个, 进行赋值
                if i % 2 == 0 :
                    smAttrName, smAttrValue = info[i].text, info[i+1].text
                    smallAttr[smAttrName] = re.sub(r'\n|进入官网>>','',smAttrValue)
            bigAttrName = bigAttrList[index]
            attrs[bigAttrName] = smallAttr

        # 赋值 - 参数页面的各个信息
        for bigAttr in bigAttrList:
            smallAttrKeys = list(attrs[bigAttr].keys())
            for SMAkey in smallAttrKeys:
                if SMAkey in self.tempMobilePhone.attribute[bigAttr]:
                    self.tempMobilePhone.attribute[bigAttr][SMAkey] = attrs[bigAttr].get(SMAkey, '')
                    del attrs[bigAttr][SMAkey]
                else:
                    pass

            # 连接其它信息
            for SMAkey in attrs[bigAttr]:
                self.tempMobilePhone.attribute[bigAttr]['其它信息'] += '{}:{}\n'.format(SMAkey, attrs[bigAttr][SMAkey])

    # 分析简略手机信息页面
    def analyzeBriefPhoneInfo(self, briefPhoneInfoHtml):
        '''
        从简略手机信息html中, 找出每台手机对应的id, 返回由id构成的列表

        :param html: str - 简略手机信息html文本
        :return:     list - 手机id 构成的list
        '''
        idList = re.findall(re.compile('data-follow-id="p(.*?)"'), briefPhoneInfoHtml)
        return idList

crawl = crawlZol()
crawl.DB.analyzeData()
#rawl.start()
