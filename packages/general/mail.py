import os.path
from typing import List

from log import getLogger
from config import MAIL_SENDER_ADDRESS, MAIL_SENDER_NAME, MAIL_APP_PASSWORD, MAIL_SMTP_SERVER, MAIL_SMTP_PORT

import smtplib
from email.mime.text import MIMEText

from path import CONFIG_DATA_DIR

logger = getLogger("Mail")


class MyMail:
    """
    ref: https://mailtrap.io/blog/python-send-email-gmail/#:~:text=To%20send%20an%20email%20with%20Python%20via%20Gmail%20SMTP%2C%20you,Transfer%20Protocol%20(SMTP)%20server.
    """

    def __init__(self):
        self._username = MAIL_SENDER_ADDRESS
        self._sender_name = MAIL_SENDER_NAME
        self._password = MAIL_APP_PASSWORD
        self._smtp_server = MAIL_SMTP_SERVER
        self._smtp_port = MAIL_SMTP_PORT
        logger.info(f"connecting SMTP server at: {self._smtp_server}:{self._smtp_port}...")
        self._server = smtplib.SMTP_SSL(self._smtp_server, self._smtp_port)
        logger.info("connected!")
        logger.info("login...")
        self._server.login(self._username, self._password)
        logger.info("logged in!")

    def _send_html_mail(self, subject, content, recipients, kind: str):
        sender = self._sender_name  # 会在收到邮件时显示名字（因此可以不必用地址）
        logger.info(f'sending from {sender} to {recipients}, kind={kind}')
        msg = MIMEText(content, kind)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipients if isinstance(recipients, str) else ', '.join(recipients)

        # from_addr 只能用ascii字符
        # UnicodeEncodeError: 'ascii' codec can't encode characters in position 11-12: ordinal not in range(128)
        self._server.sendmail(self._username, recipients, msg.as_string())
        logger.info("sent mail")

    def send_hand_future_activation_mail(self, recipients: List[str], activation_code: str, kind: str = "html"):
        if kind == "html":
            with open(os.path.join(CONFIG_DATA_DIR, "template.html"), 'r') as f:
                content = f.read() \
                    .replace("{{code}}", activation_code)
        else:
            content = activation_code
        logger.info(f'sending content: {content}')
        self._send_html_mail("【携手未来】激活验证码", content, recipients, kind)

    def __del__(self):
        self._server.close()


if __name__ == '__main__':
    my_mail = MyMail()
    my_mail.send_hand_future_activation_mail(['877210964@qq.com'], "3399", "html")
