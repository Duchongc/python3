#encoding=utf-8

from DataDrivenFrameWork.util.ObjectMap import *
from DataDrivenFrameWork.util.ParseConfigurationFile import ParseCofigFile
class AddressBookPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.parseCF = ParseCofigFile()
        self.addContactsOptions = self.parseCF.getItemsSection("126mail_addContactsPage")
        print self.addContactsOptions
    def createContactPersonButton(self):
        # 获取新建联系人按钮
        try:
            # 从定位表达式配置文件中读取新建联系人按钮的定位方式和表达式
            locateType, locatorExperession = self.addContactsOptions["addContactsPage.createContactsBtn".lower().split(">")]
            # 获取新建联系人按钮页面元素,并返回给调用者
            elementObj = getElement(self.driver,locateType, locatorExperession)
            return elementObj
        except Exception,e:
            raise e
    def contacPersonName(self):
        # 获取新建联系人界面中的姓名输入框
        try:
            locateType, locatorExperession = self.addContactsOptions[
                    "addContactsPage.contactPersonName".lower().split(">")]
            # 获取新建联系人按钮页面元素,并返回给调用者
            elementObj = getElement(self.driver, locateType, locatorExperession)
            return elementObj
        except Exception, e:
            raise e
    def contactPersonEmail(self):
        # 获取新建联系人界面中的电子邮件输入框
        try:
            locateType, locatorExperession = self.addContactsOptions[
                    "addContactsPage.contactPersonEmail".lower().split(">")]
            # 获取新建联系人界面的邮箱输入框页面元素,并返回给调用者
            elementObj = getElement(self.driver, locateType, locatorExperession)
            return elementObj
        except Exception, e:
            raise e
    def starContacts(self):
        # 获取新建联系人界面中的星标联系人的输入框输入框
        try:
            locateType, locatorExperession = self.addContactsOptions[
                    "addContactsPage.starContacts".lower().split(">")]
            # 获取新建联系人界面中的星标联系人复选框页面元素,并返回给调用者
            elementObj = getElement(self.driver, locateType, locatorExperession)
            return elementObj
        except Exception, e:
            raise e
    def contactPersonMobile(self):
        # 获取新建联系人界面中的联系人手机号码输入框
        try:
            locateType, locatorExperession = self.addContactsOptions[
                    "addContactsPage.contactPersonMobile".lower().split(">")]
            # 获取新建联系人界面的联系人手机号输入框页面元素,并返回给调用者
            elementObj = getElement(self.driver, locateType, locatorExperession)
            return elementObj
        except Exception, e:
            raise e
    def contactPersonComment(self):
        # 获取新建联系人界面中的联系人备注信息输入框
        try:
            locateType, locatorExperession = self.addContactsOptions[
                    "addContactsPage.contactPersonComment".lower().split(">")]
            # 获取新建联系人界面中联系人备注信息输入框页面元素,并返回给调用者
            elementObj = getElement(self.driver, locateType, locatorExperession)
            return elementObj
        except Exception, e:
            raise e
    def savecontacePerson(self):
        # 获取新建联系人界面中的保存联系人按钮
        try:
            locateType, locatorExperession = self.addContactsOptions[
                    "addContactsPage.savecontacePerson".lower().split(">")]
            # 获取新建联系人界面中保存联系人按钮页面元素,并返回给调用者
            elementObj = getElement(self.driver, locateType, locatorExperession)
            return elementObj
        except Exception, e:
            raise e






