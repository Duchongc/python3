#encoding=utf-8
from DataDrivenFrameWork.pageObjects.HomePage import HomePage
from DataDrivenFrameWork.pageObjects.AddressBookPage import AddressBookPage
import traceback
import time
class AddContactPerson(object):
    def __init__(self):
        print u"添加联系人"
    @staticmethod
    def add(driver, contactName, contactEmail, isStar, contactPhone, contactComment):
        try:
            # 创建主页实例对象
            hp = HomePage(driver)
            # 单击通讯录连接
            hp.addressLink().click()
            time.sleep(3)
            # 创建添加联系人页实例对象
            apb = AddressBookPage(driver)
            apb.createContactPersonButton().click()
            if contactName:
                # 非必填项
                apb.contacPersonName().send_keys(contactName)
                # 必填项
                apb.contactPersonEmail().send_keys(contactEmail)
            if isStar == u"是":
                # 非必填项
                apb.starContacts().click()
            if contactPhone:
                # 非必填
                apb.contactPersonMobile().send_keys(contactPhone)
            if contactComment:
                apb.contactPersonComment().send_keys(contactComment)
            apb.savecontacePerson().click()
        except Exception,e:
            # 打印堆栈异常信息
            print traceback.print_exc()
            raise e
if __name__ == '__main__':
    from LoginAction import LoginAction
    from selenium import webdriver
    import time
    driver = webdriver.Firefox()
    driver.get("http://mail.126.com")
    time.sleep(5)
    LoginAction.login(driver,"du1978529954","AB1.2.3.")
    time.sleep(5)
    AddContactPerson.add(driver,u"张三","1978529954@qq.com",u"是","","")
    time.sleep(3)
    assert u"张三" in driver.page_source
    driver.quit()