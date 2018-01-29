from selenium.webdriver.support.ui import WebDriverWait
import ConfigParser
import os
class ObjectMap(object):
    def __init__(self):
        self.uiObjMapPath = os.path.dirname(os.path.abspath(__file__))+"\\UiObjectMap.ini"
        print self.uiObjMapPath

    def getElementObject(self,driver,webSiteName,elementName):
        try:
            cd = ConfigParser.ConfigParser()
            cd.read(self.uiObjMapPath)
            locators = cd.get(webSiteName,elementName).split(">")
            locatorMethod = locators[0]
            locatorExpression = locators[1]
            print locatorMethod,locatorExpression
            element = WebDriverWait(driver,10).until(lambda x:x.find_element(locatorMethod,locatorExpression))
        except Exception,e:
            raise e
        else:
            return element
