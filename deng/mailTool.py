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
from os.path import exists


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

    def _attachment(self, attobj, filename):
        """将单个文件添加到附件对象中"""
        if exists(filename):
            attachname = filename.split('/')[-1]
            if len(filename) == 0:
                attachname = filename.split('\\')[-1]
        else:
            raise IOError("文件不存: %s" % filename)
        attach = MIMEText(open(filename, "rb").read(), "base64", "utf-8")
        attach["Content-Type"] = "application/octet-stream"
        attach["Content-Disposition"] = "attachment; filename='%s'" % attachname
        attobj.attach(attach)
        return attobj

    def _attachment(self, msg, attachs):
        """处理附件,将附件添加到邮件中"""
        msg_part = MIMEMultipart()
        msg_part["From"] = msg["From"]
        msg_part["To"] = msg["To"]
        msg_part["Subject"] = msg["Subject"]
        # print msg.get_payload(decode=True)
        msg_part.attach(msg)
        if isinstance(attachs, (list, tuple)):
            for attach in attachs:
                if exists(attach):
                    msg_part = self._attachment(msg_part, attach)
                else:
                    print "附件不存在, 跳过: %s" % attach
        else:
            if exists(attachs):
                msg_part = self._attachment(msg_part, attachs)
            else:
                print "附件不存在, 跳过: %s" % attachs
                return msg
        return msg_part

    def send(self, receiver, subject, content, mail_format="plain", mail_charset="utf-8", attachs=None, echo=False):
        """
            发送邮件
            参数:
                receiver:接收人邮箱列表,
                subject:邮件主题,
                content:邮件主题,
                mail_format:邮件格式,取值有plain和html,
                mail_charset:邮件字符集,
                attachs:附件路径列表
        """
        # 转换正文类型为规范类型
        if mail_format == "text":
            mail_format = "plain"

        # 处理邮件正文格式
        if mail_format == "plain":
            pass
        elif mail_format == "html":
            content = "<html><body>%s</body></html>" % content
        else:
            print "邮件格式输入错误: %s, 应该为text或html" % mail_format
            return 1
        if len(content) > 5000:
            print "邮件长度：%d" % len(content)
            print "请注意邮件内容过多，可能会被过滤掉！"
            print "自动截取前5000个字符，后面的忽略……"
            content = content[:5000]
        msg = MIMEText(content, mail_format, mail_charset)
        msg["Subject"] = Header(subject, mail_charset)
        msg["From"] = Header(self.send_username, mail_charset)
        # 接收人receiver去重
        receiver = list(set(receiver))
        if isinstance(receiver, (list, tuple)):
            msg["To"] = Header(', '.join(receiver), 'utf-8')
        else:
            msg["To"] = Header(receiver, mail_charset)

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
