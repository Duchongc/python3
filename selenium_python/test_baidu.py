#!/usr/bin/env python3
#coding=utf-8

from selenium import webdriver
import unittest
import time


class Baidu(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = 'https://www.baidu.com'
       
       
    def test_baidu_search(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id('kw').send_keys('HTML')
        time.sleep(5)
        driver.find_element_by_id('su').click()
        driver.quit()
       
    def tearDown(self):
        self.driver.quit()