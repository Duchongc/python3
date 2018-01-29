#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方SMTP服务
mail_host = "smtp.qq.com"  # 服务器地址
mail_user = "1978529954"  # 账号
mail_pass = "jgrmdfaghcwldchh"  # 授权码
sender = 'from@test.com'
receivers = ['3102733837@qq.com']  # 接收邮箱
message = MIMEText('python邮件发送测试。。。', 'plain', 'utf-8')
message['From'] = Header('菜鸟教程', 'utf-8')
message['To'] = Header('测试', 'utf-8')
subjecr = 'Python SMTP邮件测试'
message['Subject'] = Header(subjecr, 'utf-8')
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error:无法发送邮件")
