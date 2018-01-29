#encoding=utf-8

from selenium import webdriver
import time,traceback
import unittest

class qq_mai(unittest.TestCase):
    def setUp(self):
        self.drive = webdriver.Firefox()
    def test_mail(self):
        url ="https://mail.qq.com/"
        self.drive.get(url)
        time.sleep(5)
        try:
            self.drive.switch_to.frame("login_frame")
            self.drive.find_element_by_xpath(".//*[@id='switcher_plogin']").click()
            self.drive.find_element_by_xpath(".//*[@id='u']").clear()
            self.drive.find_element_by_xpath(".//*[@id='u']").send_keys("1978529954")
            self.drive.find_element_by_xpath(".//*[@id='p']").clear()
            self.drive.find_element_by_xpath(".//*[@id='p']").send_keys("xuwei@1.2.3.")
            self.drive.find_element_by_xpath(".//*[@id='login_button']").click()
            time.sleep(5)
            try:
                self.assertTrue("QQ" in  self.drive.title)
            except Exception,e:
                raise e
        except Exception,e:
            print traceback.print_exc()
    def tearDown(self):
        self.drive.quit()

if __name__ == '__main__':
    unittest.main()
