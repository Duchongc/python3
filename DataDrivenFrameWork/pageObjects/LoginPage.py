#encoding=utf-8

from DataDrivenFrameWork.util.ObjectMap import *
from DataDrivenFrameWork.util.ParseConfigurationFile import ParseCofigFile

class LoginPage(object):
    def __init__(self,driver):
        self.driver = driver
        self.parseCF = ParseCofigFile()
        self.loginOptions = self.parseCF.getItemsSection("126mail_login")
        print self.loginOptions
    def switchToFrame(self):
        try:
            locatorExpression = self.loginOptions["loginpage.frame".lower()].split(">")[1]
            self.driver.switch_to.frame(locatorExpression)
        except Exception,e:
            raise e
    def switchToDefaultFrame(self):
        try:
            self.driver.switch_to.default_content()
        except Exception,e:
            raise e
    def userNameObj(self):
        try:
            locateType,locatorExperession = self.loginOptions["loginpage.username".lower()].split(">")
            elementObj = getElement(self.driver,locateType,locatorExperession)
            return elementObj
        except Exception,e:
            raise e

    def passwordObj(self):
        try:
            locateType,locatorExperession = self.loginOptions["loginpage.password".lower()].split(">")
            elementObj = getElement(self.driver,locateType,locatorExperession)
            return elementObj
        except Exception,e:
            raise e
    def loginButton(self):
        try:
            locateType, locatoeExpression = self.loginOptions["loginpage.loginbutton".lower()].split(">")
            elementObj = getElement(self.driver,locateType,locatoeExpression)
            return elementObj
        except Exception,e:
            raise e
if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Firefox()
    driver.get("http://126.com")
    import time
    time.sleep(3)
    login = LoginPage(driver)
    login.switchToFrame()
    login.userNameObj().send_keys("du1978529954")
    time.sleep(1)
    login.passwordObj().send_keys("AB1.2.3.")
    login.loginButton().click()
    time.sleep(10)
    login.switchToDefaultFrame()
    assert u"未读邮件" in driver.page_source
    driver.quit()