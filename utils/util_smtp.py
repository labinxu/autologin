#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

class util_smtp:
    def  __init__(self, sender, receivers, password):
        #sender = 'laibin.xu@cienet.com.cn'
        #receivers = ['laibin.xu@cienet.com.cn']
        self.sender = sender
        self.receivers = receivers
        self.password = password

    def send(self,subject, msg):

        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = formataddr(["Self", self.sender])#Header("TEST", 'utf-8')   # 发送者
        message['To'] =  formataddr(['Har', ';'.join(self.receivers)])
        message['Subject'] =  subject

        try:
            smtpObj = smtplib.SMTP_SSL('smtp.263.net', 465)
            smtpObj.login(self.sender, self.password)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print ("send successfully")
        except smtplib.SMTPException as e:
            print (e)
