import smtplib

from email.message import EmailMessage
from email.header import Header

def sendMonitorEmail(content: str):
    """ 发送监控邮件
    :param content 邮件内容
     """

    myEmail = "18756762798@163.com"
    msg = EmailMessage()
    msg.set_content(content)

    subject = '后台监控'
    msg['Subject'] = subject
    msg['From'] = myEmail
    msg['To'] = myEmail

    host = 'smtp.163.com'
    # 授权码
    authorize = 'VGHSKVDYECTBSBCM'

    s = smtplib.SMTP()
    s.connect(host=host, port=25)

    loginRes = s.login(user=myEmail, password=authorize)
    # print(f'登陆结果:{loginRes}')
    s.send_message(msg)
    s.quit

if __name__ == '__main__':

    sendMonitorEmail("测试")