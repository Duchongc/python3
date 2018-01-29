#encoding=utf-8
from ConfigParser import ConfigParser
from DataDrivenFrameWork.config.VarConfig import pageElementLocatorPath
class ParseCofigFile(object):
    def __init__(self):
        self.cf = ConfigParser()
        self.cf.read(pageElementLocatorPath)
    def getItemsSection(self,sectionName):
        # 获取配置文件中指定section下所有option键值对
        # 并以字典类型返回给调用者
        optionDict = dict(self.cf.items(sectionName))
        return optionDict
    def getOptionValue(self,sectionName,optionName):
        # 获取指定section下的指定option的值
        value = self.cf.get(sectionName,optionName)
        return value

if __name__ == '__main__':
    pc = ParseCofigFile()
    print pc.getItemsSection("126mail_login")
    print pc.getOptionValue("126mail_login","loginPage.frame")

