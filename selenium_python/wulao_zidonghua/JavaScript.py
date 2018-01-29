#encoding=utf-8
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest
import traceback
import time
class TestDemo(unittest.TestCase):
    def setUp(self):

        self.driver = webdriver.Firefox()

    def test_executeScript(self):
        url = "http://www.baidu.com"

        self.driver.get(url)

        searchInputBoxJS = "document.getElementById('kw').value='html';"

        searchButtonJS = "document.getElementById('su').click()"
        try:

            self.driver.execute_script(searchInputBoxJS)
            time.sleep(5)

            self.driver.execute_script(searchButtonJS)
            time.sleep(5)

            self.assertTrue("JavaScript"  in self.driver.page_source)
        except WebDriverException, e:

            print u"The page elements to operate is not found in the page",traceback.print_exc()
        except AssertionError, e:
            print u"Keyword string without assertion on page"
        except Exception, e:
            print traceback.print_exc()
    def tearDown(self):
         self.driver.quit()

if __name__ == '__main__':
    unittest.main()