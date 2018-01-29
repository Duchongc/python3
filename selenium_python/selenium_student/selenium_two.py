from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

drive = webdriver.Firefox()
web_url = 'https://www.youku.com/'
drive.get(web_url)

drive.find_element_by_xpath(".//*[@id='topNav']/div/ul/li[3]/a").click()
text_a = drive.find_element_by_xpath(".//*[@id='topNav']/div/ul/li[3]/a").text
def test_04(self):
    try:
        test = str("电影")
        if test in text_a:
            print("ok")
        else:
            print("no")
    except:
        print("失败")




time.sleep(5)
drive.quit()