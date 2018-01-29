#encoding=utf-8
import os
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pageElementLocatorPath = parentDirPath + u"\\config\\PageElementLocator.ini"

# 获取数据文件存放绝对路径
dataFilePath = parentDirPath + u"\\testData\\126邮箱.xlsx"

# 126账号工作表中,每列对应的数字序号
account_username = 2
account_password = 3
account_dataBook = 4
account_inExecute = 5
account_testResult = 6

# 联系人工作表中,每列对应的数字序号
contacts_contactPersonName = 2
contacts_contactPersonEmail = 3
contacts_isStar = 4
contacts_contactPersonMobile = 5
contacts_contactPersonComment = 6
contacts_assertKeyWords = 7
contacts_isExecute = 8
contacts_runTime = 9
contacts_testResult = 10
