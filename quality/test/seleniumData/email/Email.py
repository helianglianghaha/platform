#!/usr/bin/python
# -*- coding: UTF-8 -*-
import imaplib,requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
class email_client:
    def __init__(self,smtp_server,from_addr,to_addr,Cc_addr,password,
                 project,version,operatingEnvironment,triggerReason,testResult,testReport):
        '''
        :param smtp_server: 服务器地址
        :param from_addr: 发件人
        :param to_addr:收件人
        :param Cc_addr: 抄送人
        :param password: 密码
        :param project:项目
        :param version: 版本
        :param operatingEnvironment: 运行环境
        :param triggerReason: 触发原因
        :param testResult: 测试结果
        :param testReport: 测试报告
        '''
        self.smtp_server=smtp_server
        self.from_addr=from_addr
        self.to_addr=to_addr
        self.Cc_addr=Cc_addr
        self.password=password
        self.project=project
        self.version=version
        self.operatingEnvironment=operatingEnvironment
        self.triggerReason=triggerReason
        self.testResult=testResult
        self.testReport=testReport
    # @property
    def send_qixin(self):
        header = {'Content-Type': 'application/json;charset=UTF-8'}
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bbe3c1c3-9d8a-48f1-94ee-09200c2f4c01'

        data = {
            "msgtype": "text",
            "text": {
                "content": "jenkins maybe is unusealbe ,cause queue number is more than 5",
                "mentioned_mobile_list": ["13783783183", '15342209907']
            }
        }
        requests.post(url, json=data, headers=header)
    @property
    def mail(self):
        '''
        发送邮件
        :return:
        '''
        if self.testResult=='成功':
        #邮件定义内容区域
            mail_content='<!DOCTYPE html>'\
            '<html>'\
                '<head>'\
                    '<meta http-equiv=\'Content-Type\' content=\'text/html; charset=utf-8\' />' \
                    '<title>次构建日志</title>'\
                '</head>'\
                '<body>'\
                '<table  width=\'95%\' cellpadding=\'0\' cellspacing=\'0\' style=\'font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif\'>' \
                 '<tr>'\
                        '<td colspan=\'2\'>'\
                        '<h3 style=\'color:#0000FF\'> 各位领导你好:</h3>'\
                        '</td>'\
                '</tr>' \
                 '<tr>'\
                    '<td colspan = \'2\'> &nbsp;&nbsp;&nbsp;&nbsp;'+self.project+\
                '的UI自动化测试运行报告已出，本次报告概要内容，详细请看附件: </td>'\
            '</tr>' \
            '<tr>'\
                    '<td colspan = \'2\'><br/><b> <fontcolor=\'#0000FF\'> 测试计划概况 </font> </b>'\
                    '<hr size=\'2\' width=\'100%\' align=\'center\'/></td>'\
            '</tr>'\
            '<tr>'\
            '<td> 版本名称：</td>' \
             '<td>'+self.version+'</td>' \
             '</tr>' \
             '<tr>' \
             '<td> 运行环境：</td>' \
            '<td> <a href=\''+self.operatingEnvironment+'\'>'+self.operatingEnvironment+'</a></td>'\
             '</tr>' \
             '<tr>' \
             '<td> 触发原因：</td>' \
             '<td>	Started by'+self.triggerReason+'</td>'\
             '</tr>' \
             '<tr>'\
                '<td style=\'color: #FF0000\'> <b> 测试结果：</b></td>' \
                '<td style=\'color: #FF0000\'>'+self.testResult+'</td>' \
            '</tr>' \
            '<tr>'\
            '<td>测试报告：</td>'\
            '<td><a href=\''+self.testReport+'\'>'+self.testReport+'</a></td>'\
            '</tr>'\
             '<tr>' \
             '<td colspan=\'2\'>' \
                 '<hr size=\'2\' width=\'100%\' align=\'center\'/>' \
                 '<b style=\'color:#FF0000\'>(本邮件是程序自动下发的，请勿回复！)</b>'\
            '</td>' \
             '</tr>' \
            '</table>'\
            '</body>'\
        '</html>'
        else:
            mail_content = '<!DOCTYPE html>' \
           '<html>' \
           '<head>' \
           '<meta http-equiv=\'Content-Type\' content=\'text/html; charset=utf-8\' />' \
           '<title>次构建日志</title>' \
           '</head>' \
           '<body>' \
           '<table  width=\'95%\' cellpadding=\'0\' cellspacing=\'0\' style=\'font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif\'>' \
           '<tr>' \
           '<td colspan=\'2\'>' \
           '<h3 style=\'color:#0000FF\'> 各位领导你好:</h3>' \
           '</td>' \
           '</tr>' \
           '<tr>' \
           '<td colspan = \'2\'> &nbsp;&nbsp;&nbsp;&nbsp;' + self.project + \
           '的UI自动化测试运行报告已出，本次报告概要内容，详细请看附件: </td>' \
           '</tr>' \
           '<tr>' \
           '<td colspan = \'2\'><br/><b> <fontcolor=\'#0000FF\'> 测试计划概况 </font> </b>' \
           '<hr size=\'2\' width=\'100%\' align=\'center\'/></td>' \
           '</tr>' \
           '<tr>' \
           '<td> 版本名称：</td>' \
           '<td>' + self.version + '</td>' \
           '</tr>' \
           '<tr>' \
           '<td> 运行环境：</td>' \
           '<td> <a href=\'' + self.operatingEnvironment + '\'>' + self.operatingEnvironment + '</a></td>' \
           '</tr>' \
           '<tr>' \
           '<td> 触发原因：</td>' \
           '<td>	Started by' + self.triggerReason + '</td>' \
           '</tr>' \
           '<tr>' \
           '<td> <b> 测试结果：</b></td>' \
           '<td >' + self.testResult + '</td>' \
           '</tr>'\
           '<tr>' \
           '<td>测试报告：</td>' \
           '<td><a href=\'' + self.testReport + '\'>' + self.testReport + '</a></td>' \
          '</tr>' \
          '<tr>' \
          '<td colspan=\'2\'>' \
          '<hr size=\'2\' width=\'100%\' align=\'center\'/>' \
          '<b style=\'color:#FF0000\'>(本邮件是程序自动下发的，请勿回复！)</b>' \
          '</td>' \
          '</tr>' \
          '</table>' \
          '</body>' \
          '</html>'
        msg = MIMEText(mail_content, 'html', 'utf-8')
        msg['Subject'] =self.version+ 'UI自动化测试报告'
        msg['From'] = self.from_addr
        msg['To'] =  self.to_addr 
        msg['Cc'] = self.Cc_addr
        print([self.to_addr])
        server = smtplib.SMTP(self.smtp_server, 25) # SMTP协议默认端口是25
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, self.to_addr, msg.as_string())
        server.quit()
    def rece_email_by_imap(self):
        email_address='heliangliang@aiyunxiao.com'
        email_passWord='hll@123QAZ'
        email_server_host='mail.aiyunxiao.com'
        email_server_port=993
        try:
            email_server=imaplib.IMAP4_SSL(host=email_server_host,port=email_server_port)
            print('登录成功')
        except:
            print('登录失败')
        try:
            email_server.login(email_address,email_passWord)
            print('login success')
        except:
            print('login error')
        # 邮箱中其收到的邮件的数量
        email_server.select()
        email_count = len(email_server.search(None, 'ALL')[1][0].split())
        # 通过fetch(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        email_content = email_server.fetch(f'{email_count}'.encode(), '(RFC822)')
        # 将邮件内存由byte转成str
        email_content = email_content[0][1].decode()
        print(email_content)
        # 关闭select
        email_server.close()
        # 关闭连接
        email_server.logout()
if __name__ == "__main__":
    smtpServer='mail.aiyunxiao.com'
    fromAddr='heliangliang@aiyunxiao.com'
    toAddr='heliangliang@aiyunxiao.com'
    CcAddr='heliangliang@aiyunxiao.com,liufang@aiyunxiao.com'
    passWord='hll@123QAZ'
    project='知识库'
    version='数字化V2.9.4'
    operatingEnvironment='http://127.0.0.1:8090/#/manage/UIExecuting'
    triggerReason='timer'
    testResult='fail'
    testReport='http://127.0.0.1:8090/#/UIreport?label=20fc945e5258fe20b0684de9543d6580'
    email_client(smtpServer,fromAddr,toAddr,CcAddr,passWord,
                 project,version,operatingEnvironment,triggerReason,testResult,testReport).mail
    # email_client().send_qixin
    print("发送邮件")