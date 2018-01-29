import time
from selenium import webdriver
drive = webdriver.Firefox()

url = 'file:///C:百度一下，你就知道.html'
drive.get(url)
time.sleep(5)
drive.quit()