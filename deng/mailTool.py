#!/usr/bin/env python
# coding=utf-8
"""
Author: DENGQINGYONG
Time:   17/2/10 11:05 
Desc:   发送邮件示例代码
"""
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from os.path import exists, basename
from deng.colors import *


class MailTool(object):
    """
        用途：
            邮件发送工具
        初始化：
            send_username:  发送者邮箱
            send_smtp:      发送者邮箱对应的smtp服务器地址
            send_password:  发送都邮箱密码
        方法：
            send()
    """

    def __init__(self, send_username, send_smtp=None, send_password=None, echo=False):
        """初始化实例,需要提供发送方信息:发送smtp服务器,用户名,密码等"""
        self.echo = echo
        if self.echo:
            print "send_smtp=%s" % send_smtp
            print "send_username=%s" % send_username
            print "send_password=%s" % send_password
        self.send_smtp = send_smtp
        self.send_username = send_username
        self.send_password = send_password

    def _add_attach(self, attobj, filename):
        """将单个文件添加到附件对象中"""
        if exists(filename):
            attachname = basename(filename)
            # attachname = Header(attachname, "utf-8")
            # # linux系统
            # attachname = filename.split('/')[-1]
            # # windows系统
            # if len(filename) == 0:
            #     attachname = filename.split('\\')[-1]
        else:
            raise IOError("文件不存: %s" % filename)
        attach = MIMEText(open(filename, "rb").read(), "base64", "utf-8")
        attach["Content-Type"] = "application/octet-stream"
        attach["Content-Disposition"] = "attachment; filename='%s'" % attachname
        attobj.attach(attach)
        return attobj

    def _attachment(self, msg, attachs):
        """处理附件,将附件添加到邮件中"""
        if isinstance(attachs, (list, tuple)):
            for attach in attachs:
                if exists(attach):
                    msg = self._add_attach(msg, attach)
                else:
                    print "附件不存在, 跳过: %s" % attach
        else:
            if exists(attachs):
                msg = self._add_attach(msg, attachs)
            else:
                print "附件不存在, 跳过: %s" % attachs
        return msg

    def send(self, receiver, subject, content, mail_charset="utf-8", attachs=None, echo=False):
        """
            发送邮件
            参数:
                receiver:接收人邮箱列表,
                subject:邮件主题,
                content:邮件主题,
                mail_charset:邮件字符集,
                attachs:附件路径列表
        """
        # 字符串单收件人时转换成列表格式
        if isinstance(receiver, (str, unicode)):
            receiver = [receiver]
        # 收件人格式检查
        if not isinstance(receiver, (tuple, list)):
            print red("参数receiver格式不正确!")
            print red("receiver预期格式：str、tuple或list")
            print red("receiver实际格式：%s" % type(receiver))
        # 接收人receiver去重
        if isinstance(receiver, (tuple, list)):
            receiver = list(set(receiver))

        # 邮件长度检查，超大时只截取前5000个字符
        if len(content) > 5000:
            print yellow("邮件长度：%d" % len(content))
            print yellow("请注意邮件内容过多，可能会被过滤掉！")
            print yellow("自动截取前5000个字符，后面的忽略……")
            content = content[:5000]

        # msg = MIMEMultipart("alternative")
        msg = MIMEMultipart("related")
        # text
        text = MIMEText(content, 'plain', mail_charset)
        msg.attach(text)
        # html
        html = MIMEText("<html><body><p>%s</p></body></html>" % content, "html", mail_charset)
        msg.attach(html)
        msg['Date'] = formatdate(localtime=True)
        msg["Subject"] = Header(subject, mail_charset)
        msg["From"] = Header(self.send_username, mail_charset)
        msg["To"] = Header(', '.join(receiver), 'utf-8')

        # 处理附件
        if attachs:
            msg = self._attachment(msg, attachs)

        smtp = smtplib.SMTP()
        smtp.set_debuglevel(self.echo)
        smtp.connect(self.send_smtp)
        smtp.login(self.send_username, self.send_password)
        smtp.sendmail(self.send_username, receiver, msg.as_string())
        smtp.quit()

        # 日志显示
        if self.echo or echo:
            print "邮件发送人：%s" % self.send_username
            print "邮件接送人：%s" % receiver
            print "邮件标题：%s" % subject
            if str(echo).lower() == "vv":
                print "邮件内容：%s" % content
            elif str(echo).lower() == "vvv":
                print "邮件内容：%s" % msg.as_string()
