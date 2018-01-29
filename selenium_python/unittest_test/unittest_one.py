import unittest, time
import re
from selenium import webdriver
class test(unittest.TestCase):
    def setUp(self):
        self.d = webdriver.Firefox()
        self.d.implicitly_wait(30)
        self.url = 'https://baidu.com'
    def test_01(self):
        d = self.d
        d.get(self.url)
        d.find_element_by_id("kw").clear()
        d.find_element_by_id("kw").send_keys("unittest")
        d.find_element_by_id("su").click()
        time.sleep(3)
        title = d.title
        self.assertEqual(title, u"unittest_百度搜索")
    def tearDown(self):
        self.d.quit()
if __name__ == '__main__':
    unittest.main()


