from selenium import webdriver
from selenium.webdriver import ActionChains
import time
def sleeps():
    time.sleep(1)
phpwind = webdriver.Firefox()
url = "http://192.168.0.134/phpwind/"
phpwind.get(url)
time.sleep(2)
phpwind.find_element_by_xpath(".//*[@id='J_username']").send_keys("admin")
time.sleep(2)
phpwind.find_element_by_xpath(".//*[@id='J_password']").send_keys("123456")
time.sleep(2)
phpwind.find_element_by_xpath(".//*[@id='J_sidebar_login']").click()
time.sleep(2)
p = phpwind.find_element_by_xpath(".//*[@id='J_head_forum_post']/span/span").text
try:
    php = u"发帖"
    assert p == php

    print("登陆成功")
except Exception as e:
    print("登录失败")

phpwind.find_element_by_xpath(".//*[@id='J_head_forum_post']/span/span").click()
sleeps()
p1 = phpwind.find_element_by_xpath(".//*[@id='J_head_forum_ct']/div[1]/h4").text
try:
    p2 = u"选择分类"
    assert p1 == p2
    print("发帖")
except Exception as e:
    print("发帖失败")
sleeps()
phpwind.find_element_by_xpath(".//*[@id='J_forum_list']/li[1]").click()
phpwind.find_element_by_xpath(".//*[@id='J_forum_ul']/li").click()
phpwind.find_element_by_xpath(".//*[@id='J_head_forum_sub']").click()
sleeps()
p3 = phpwind.find_element_by_xpath(".//*[@id='tabTypeHead']/li/a").text
try:
    p4 = u"发布主题"
    assert p3 == p4
    print("进入发帖")
except Exception as e:
    print("进入发帖失败")
sleeps()

phpwind.find_element_by_xpath(".//*[@id='J_atc_title']").send_keys("this is one")
element = phpwind.find_element_by_css_selector(".editor_content")
ActionChains(phpwind).double_click(element).perform()

'''phpwind.find_element_by_css_selector(".editor_content").send_keys("this is one")'''
phpwind.find_element_by_xpath(".//*[@id='J_post_sub']").click()
sleeps()
p5 = phpwind.find_elements_by_css_selector(".btn_replay")
try:
    p6 = u"回复"
    assert p5 == p6
    print("发帖成功")
except Exception as e:
    print("发帖失败")
sleeps()

phpwind.quit()