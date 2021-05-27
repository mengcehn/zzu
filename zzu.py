# -*- coding:utf-8 -*-
"""
作者:mengchen
日期:2021.05.25
"""
import requests
import re
from hashlib import sha1
import os
import time

def auto(xuehao,mima):
        url="https://jw.v.zzu.edu.cn/eams/login.action"
        headers={
                'Host':'jw.v.zzu.edu.cn',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type':'application/x-www-form-urlencoded',
                'Origin':'https://jw.v.zzu.edu.cn',
                'Connection':'close',
               # 'Referer':'https://jw.v.zzu.edu.cn/eams/login.action',
                'Upgrade-Insecure-Requests':'1',
        }

        session=requests.session()
        response=session.get(url=url,headers=headers)
        html=response.content.decode('utf-8')

        username0=xuehao
        password0=mima

        #print(html)
        password=re.findall(r"'(.+?)'",html)[5]
        password=password+password0
        password1=sha1(password.encode('utf8')).hexdigest()
        #print(password1)
        post_data={
            'username':username0,
            'password':password1,
            'encodedPassword':'',
            'session_locale':'zh_CN',
        }
        time.sleep(3)
        response1=session.post(url=url,headers=headers,data=post_data)
        html=response1.content.decode("utf-8")
        if "我的账户" in html:
                print("登录成功")                                                           #登录
        #print(html)
        url1="https://jw.v.zzu.edu.cn/eams/teach/grade/course/person!report.action"
        response2=session.post(url=url1,headers=headers)
        html2=response2.text
        name=re.findall('" >(.+?)</td>',html2)
        num=re.findall('Td">(.+?)</td>',html2)                                          #数据解析
        score=[]
        for i in range(len(num)):
            try:
                a=int(num[i])
                score.append(a)
            finally:
                continue
        # 写之前，先检验文件是否存在，存在就删掉
        if os.path.exists("成绩.txt"):
            os.remove("成绩.txt")
        txtName = "成绩.txt"
        f = open(txtName, 'w')
        for i in range(len(name)):
            new_context ="科目：" + name[i] + "------------" + str(score[i])+ "分" +'\n'
            f.write(new_context)
            print("科目："+name[i],end="----")
            print(score[i])
        f.close()


def Sendmall():

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header

    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "1375669090@qq.com"  # 用户名
    mail_pass = "vzzzgpxotmragdab"  # 口令

    sender = '1375669090@qq.com'  ##发邮件账号
    receivers = ['1375669090@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("mengchen", 'utf-8')
    message['To'] = Header("成绩单", 'utf-8')
    subject = 'zzu期末成绩单'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('zzu考试成绩', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('成绩.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="成绩.txt"'
    message.attach(att1)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
if __name__ == "__main__":
        xuehao = "201978030522"           #学号
        mima = "245438"                   #密码
        try:
            auto(xuehao,mima)
            Sendmall()
            print("程序运行成功。。。")

        except:
            print("error error error")
            print("程序运行失败。。。")

