#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from DataDrivenFrameWork.util.ParseExcel import PatseExcel
from DataDrivenFrameWork.config.VarConfig import *
from DataDrivenFrameWork.appModules.AddContactPersonAction import AddContactPerson
from DataDrivenFrameWork.appModules.LoginAction import LoginAction
import traceback
from time import sleep
"""
def testMailLogin():
    try:
        driver = webdriver.Firefox()
        driver.get("http://126.com")
        driver.implicitly_wait(30)
        driver.maximize_window()
        time.sleep(5)
        LoginAction.login(driver,"du1978529954","AB1.2.3.")
        time.sleep(10)
        assert u"未读邮件" in driver.page_source
    except Exception,e:
        raise e
    finally:
        driver.quit()

if __name__ == '__main__':
    testMailLogin()
    print u"登录126邮箱成功"
"""
# 设置此次测试的环境编码为utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# 创建解析Excel对象
excelObj = PatseExcel()
# 将Excel数据文件加载到内存
excelObj.loadWorkBook(dataFilePath)

def LaunchBrowser():
    driver = webdriver.Firefox()
    driver.get("http://mail.126.com")
    sleep(3)
    return driver
def test126MailAddContacts():
    try:
        # 根据Excel文件中sheet名称获取此sheet对象
        userSheet = excelObj.getSheetByName(u"126账号")
        # 获取126账号sheet中是否执行列
        isExecuteUser = excelObj.getColumn(userSheet,account_inExecute)
        # 获取126账号sheet中数据表列
        dataBookColumn = excelObj.getColumn(userSheet,account_dataBook)
        print u"测试为126邮箱添加联系人执行开始..."
        for idx, i in enumerate(isExecuteUser[1:]):
            # 循环遍历126账号表中的账号,为需要执行的账号添加联系人
            if i.value == "y": # 表示要执行
                # 获取第i行的数据
                userRow = excelObj.getRow(userSheet,idx + 2)
                # 获取第i行中的用户名
                username = userRow[account_username - 1].value
                # 获取第i行中的密码
                password = str(userRow[account_password - 1].value)
                print username,password

                # 创建浏览器实例对象
                driver = LaunchBrowser()
                # 登录126邮箱
                LoginAction.login(driver,username,password)
                sleep(5)
                # 获取为第i行中用户添加的联系人数据表sheet名
                dataBookName = dataBookColumn[idx + 1].value
                # 获取对应的数据表对象
                dataSheet = excelObj.getSheetByName(dataBookName)
                # 获取联系人数据表中是都执行列对象
                isExecuteData = excelObj.getColumn(dataSheet,contacts_isExecute)
                contactNum = 0 # 记录添加成功联系人个数
                isExecuteNum = 0 # 记录需要执行联系人个数
                for id ,data in enumerate(isExecuteData[1:]):
                    # 循环遍历是否执行添加联系人列,如果被设置添加,则进行联系人添加操作
                    if data.value == "y":
                        # 如果第id行的联系人被设置为执行,则isExecuteNum自增1
                        isExecuteNum += 1
                        # 获取联系人表第id+2行对象
                        rowContent = excelObj.getRow(dataSheet,id+2)
                        # 获取联系人姓名
                        contactPersonName = rowContent[contacts_contactPersonName -1].value
                        # 获取联系人邮箱
                        contactPersonEmail = rowContent[contacts_contactPersonEmail -1].value
                        # 获取是否设置为星标联系人
                        isStar = rowContent[contacts_isStar -1].value
                        # 获取联系人手机号
                        contactPersonPhone = rowContent[contacts_contactPersonMobile -1].value
                        # 获取联系人备注信息
                        contactPersonComment = rowContent[contacts_contactPersonComment -1].value
                        # 添加联系人成功之后,断言的关键字
                        asserKeyWord = rowContent[contacts_assertKeyWords -1].value
                        print contactPersonName,contactPersonEmail,asserKeyWord
                        print contactPersonPhone,contactPersonComment,isStar
                        # 执行新建联系人操作
                        AddContactPerson.add(driver,
                                             contactPersonName,
                                             contactPersonEmail,
                                             isStar,
                                             contactPersonPhone,
                                             contactPersonComment)
                        sleep(1)
                        # 在联系人工作表中写入添加联系人执行时间
                        excelObj.writeCellCurrentTime(dataSheet,
                                                      rowNo=id + 2,colsNo=contacts_runTime)
                        try:
                            # 断言给定的关键字是否出现在页面中
                            assert asserKeyWord in driver.page_source
                        except AssertionError,e:
                            # 断言失败,在联系人工作表中写入添加联系人测试失败信息
                            excelObj.writeCell(dataSheet,"faild",rowNo=id+2,colsNo=contacts_testResult,style="red")
                        else:
                            # 断言成功,写入添加联系人成功信息
                            excelObj.writeCell(dataSheet,"pass",rowNo=id+2,colsNo=contacts_testResult,style="green")
                            contactNum +=1
                    print "contactNum = %s,isExecuteNum = %s" %(contactNum,isExecuteNum)
                    if contactNum == isExecuteNum:
                        # 如果成功添加的联系人数与需要添加的联系人数相等
                        # 说明给第i个用户添加联系人测试用例执行成功
                        # 在126账号工作表中写入成功信息,否则写入失败信息
                        excelObj.writeCell(userSheet,"pass",rowNo=idx+2,colsNo=account_testResult,style="green")
                        print u"为用户%s添加%d个联系人,测试通过!" %(username,contactNum)
                    else:
                        excelObj.writeCell(userSheet,"faild",rowNo=idx+2,colsNo=account_testResult,style="red")
                else:
                    print u"用户%s被设置为忽略执行!" %excelObj.getCellOfValue(userSheet,rowNo=idx+2,colsNo=account_username)
                    driver.quit()
    except Exception,e:
        print u"数据驱动框架主程序发生异常,异常信息为"
        print traceback.print_exc()
if __name__ == "__main__":
    test126MailAddContacts()
    print u"登录126邮箱成功"