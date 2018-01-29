
from selenium import webdriver
import time,os
import unittest
if 'HTTP_PROXY' in os.environ:del os.environ['HTTP_PROXY']

class kaoshi(unittest.TestCase):
    def setUp(self):
        self.drivr = webdriver.Firefox()
        self.drivr_url = 'http://www.qq.mail.com'

        time.sleep(5)
    def test_youxiang_login_01(self):
        d = self.drivr
        url = self.drivr_url
        d.get(url)
        d.find_element_by_xpath(".//*[@id='login']/li[1]/label/input").send_keys("admin")
        d.find_element_by_xpath(".//*[@id='login']/li[2]/label/input").send_keys("hyrt123456")
        d.find_element_by_xpath(".//*[@id='login']/li[3]/a").click()
        time.sleep(5)
    def test_youxiang_02(self):
        drivr.find_element_by_xpath(".//*[@id='accordion']/li[1]/div").click()
        time.sleep(2)
        drivr.find_element_by_css_selector("ul#accordion > li:nth-child(1) >  ul > li:nth-child(1)> a").click()
        time.sleep(3)
        drivr.find_element_by_css_selector("ul#accordion > li:nth-child(1) >  ul > li:nth-child(3)> a").click()
        time.sleep(3)
        drivr.find_element_by_id("add_user2").click()
        time.sleep(3)
    def tearDown(self):
        drivr.quit()




