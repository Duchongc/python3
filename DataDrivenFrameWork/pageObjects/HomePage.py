#encoding=utf-8

from DataDrivenFrameWork.util.ObjectMap import *
from DataDrivenFrameWork.util.ParseConfigurationFile import ParseCofigFile
class HomePage(object):
    def __init__(self,driver):
        self.driver = driver
        self.parseCF = ParseCofigFile()
    def addressLink(self):
        try:
            # 从定位表达式配置文件中读取定位通讯录按钮的定位方式和表达式
            locateType, locatorExperession = self.parseCF.getOptionValue("126mail_homePage","homepage.addressbook").split(">")
            # 获取登陆成功页面的通讯录页面元素,并返回给调用者
            elementObj = getElement(self.driver,locateType,locatorExperession)
            return elementObj
        except Exception,e:
            raise e

