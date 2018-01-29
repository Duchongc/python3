#encoding=utf-8
from DataDrivenFrameWork.pageObjects.LoginPage import *
class LoginAction(object):
    def __init__(self):
        print "login.."
    @staticmethod
    def login(driver,username,password):
        try:
            login = LoginPage(driver)
            login.switchToFrame()
            login.userNameObj().send_keys(username)
            login.passwordObj().send_keys(password)
            login.loginButton().click()
            login.switchToDefaultFrame()
        except Exception,e:
            raise e
if __name__ == '__main__':
    from selenium import webdriver
    import time
    driver = webdriver.Firefox()
    driver.get("http://126.com")
    time.sleep(5)
    LoginAction.login(driver,username="du1978529954",password="AB1.2.3.")
    time.sleep(3)
    driver.quit()



