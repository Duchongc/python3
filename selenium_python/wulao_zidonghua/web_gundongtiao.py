from selenium import webdriver
import unittest
import traceback
import time
class TestDemo(unittest.TestCase):
    def setUp(self):
       self.drive = webdriver.Firefox()

    def test_scroll(self):
        url = "http://www.seleniumhq.org/"
        try:
            self.drive.get(url)
            time.sleep(2)
            self.drive.execute_script("window.scrollTo(100,document.body.scrollHeight);")
            time.sleep(2)
            self.drive.execute_script("document.getElementById('choice').scrollIntoView(true);")
            time.sleep(2)
            self.drive.execute_script("window.scrollBy(0,400);")
            time.sleep(2)
        except Exception,e:
            print traceback.print_exc()
    def tearDown(self):
        self.drive.quit()

if __name__ == '__main__':
    unittest.main()