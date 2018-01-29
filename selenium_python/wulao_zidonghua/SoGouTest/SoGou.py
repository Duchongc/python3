from selenium import webdriver
import unittest
import time,traceback
from ObjectMap import ObjectMap

class TestDemo(unittest.TestCase):
    def setUp(self):
        self.obj = ObjectMap()
        self.driver = webdriver.Firefox()

    def test_SoGou(self):
        url = "https://www.sogou.com/"
        self.driver.get(url)
        try:
            searchBox = self.obj.getElementObject(self.driver,"sogou","searchBox")
            searchBox.send_keys("python")
            searchButton = self.obj.getElementObject(self.driver,"sogou","searchButton")
            searchButton.click()
            time.sleep(5)
            self.assertTrue("python" in self.driver.page_source,"assert error!")
        except Exception,e:
            print traceback.print_exc()
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()