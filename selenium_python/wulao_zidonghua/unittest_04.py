from selenium import webdriver
import unittest
import time
class drive_test(unittest.TestCase):
    def setUp(self):
        self.drive = webdriver.Firefox()

    def test_sogou(self):

        geturl = "http://www.baidu.com"
        self.drive.get(geturl)
        now_handle = self.drive.current_window_handle
        print(now_handle)
        self.drive.find_element_by_id("kw").send_keys("w3cschool")
        self.drive.find_element_by_id("su").click()
        time.sleep(3)
        self.drive.find_element_by_xpath('//div[@id="1"]//a[text()="w3"]').click()
        try:
            result = self.drive.get_screenshot_as_file(r"c:\img.png")
            print(result)
        except IOError:
            print('IOError')
        time.sleep(5)
        all_handles = self.drive.window_handles
        print('++++',self.drive.window_handles[-1])
        for handle in all_handles:
            if handle != now_handle:
                print(handle)

    def tearDown(self):
        self.drive.quit()

if __name__ == '__main__':
    unittest.main()
