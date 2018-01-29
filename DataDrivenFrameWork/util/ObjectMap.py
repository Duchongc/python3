#encoding=utf-8
from selenium.webdriver.support.ui import WebDriverWait
def getElement(driver,locateType,locatorExperession):
    try:
        element = WebDriverWait(driver,30).until(lambda x:x.find_element(by=locateType,value=locatorExperession))
        return element
    except Exception,e:
        raise e
def getElements(driver,locateType,locatorExperession):
    try:
        elements = WebDriverWait(driver,30).until(lambda x:x.find_elements(by=locateType,value=locatorExperession))
        return elements
    except Exception, e:
        raise e
if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Firefox()
    driver.get("http://www.baidu.com")
    searchBox = getElement(driver,"id","kw")
    print (searchBox.tag_name)
    aList = getElements(driver,"tag name","a")
    print (len(aList))
    driver.quit()


