from selenium import webdriver
import time
import selenium.webdriver.support.ui as ui

qq = webdriver.Firefox()
url = 'https://qzone.qq.com/'
qq.get(url)
time.sleep(2)
qq.switch_to.frame("login_frame")
qq.find_element_by_xpath(".//*[@id='switcher_plogin']").click()
time.sleep(3)
qq.find_element_by_id("u").send_keys("1978529954")
time.sleep(1)
qq.find_element_by_id("p").send_keys("xuwei@1.2.3.")
time.sleep(3)

qq.find_element_by_xpath(".//*[@id='login_button']").click()

qq.switch_to.default_content()




qq.quit()