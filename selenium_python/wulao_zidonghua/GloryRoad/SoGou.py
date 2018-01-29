# encoding=utf-8
from selenium import webdriver
import unittest,time,os
from FileUtil import createDir
import traceback
 # 创建存放异常截图的目录,并得到本次实例中存放图片目录的绝对路径
 # 并且作为全局变量,以供本次所有测试用例调用
picDir = createDir()
def takeScreenshot(driver,savePath,picName):
     # 封装截屏方法
     # 构造截屏路径及图片
     # 转码
     picPath = os.path.join(savePath,str(picName).decode("utf-8").encode("gbk")+".png")
     try:
         # 调用webdriver提供的get_screenshot_as_file()方法
         # 将截取的屏幕图片保存为本地文件
         driver.get_screenshot_as_file(picPath)
     except Exception,e:
         print traceback.print_exc()
class TestFailCaptureScreen(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
    def testSoGouSearch(self):
        url = "http://www.baidu.com"
        self.driver.get(url)
        try:
            self.driver.find_element_by_id("kw").send_keys(u"光荣之路自动化测试")
            time.sleep(3)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            self.assertTrue(u"事在人为" in self.driver.page_source,"事在人为未找到")
        except AssertionError,e:
            takeScreenshot(self.driver,picDir,e)
        except Exception,e:
            print traceback.print_exc()
            takeScreenshot(self.driver,picDir,e)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
