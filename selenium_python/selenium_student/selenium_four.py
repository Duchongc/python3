from selenium import webdriver
import os
from time import sleep

if 'HTTP_PROXY' in os.environ:del os.environ['HTTP_PROXY']
dr = webdriver.Firefox()
url = 'http://www.sina.com.cn/'
dr.get(url)
print("title of cirrent page is %s" %(dr.title))
print("url of current page is %s" %(dr.current_url))
sleep(2)
dr.quit()