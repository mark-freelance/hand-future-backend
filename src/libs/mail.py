import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List

from src.libs.env import SMTP_SENDER, SMTP_SENDER_NAME, SMTP_PSWD, SMTP_HOST, \
    SMTP_PORT, SMTP_USER
from src.libs.log import getLogger
from src.libs.path import CONFIG_DIR

logger = getLogger("Mail")


class MyMail:
    """
    ref: https://mailtrap.io/blog/python-send-email-gmail/#:~:text=To%20send%20an%20email%20with%20Python%20via%20Gmail%20SMTP%2C%20you,Transfer%20Protocol%20(SMTP)%20server.
    """

    def __init__(self):
        self._smtp_user = SMTP_USER
        self._smtp_sender = SMTP_SENDER
        self._smtp_sender_name = SMTP_SENDER_NAME
        self._smtp_pswd = SMTP_PSWD
        self._smtp_host = SMTP_HOST
        self._smtp_port = SMTP_PORT
        # logger.info({
        #     "sender": self._smtp_sender, "sender_name": self._smtp_sender_name, "host": self._smtp_host,
        #     "port": self._smtp_port, "pswd": self._smtp_pswd
        # })

    def _send_html_mail(self, subject, content, recipients: List[str], kind: str):
        with smtplib.SMTP_SSL(self._smtp_host, self._smtp_port) as server:
            server.login(self._smtp_user, self._smtp_pswd)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = formataddr((self._smtp_sender_name, self._smtp_sender))
            msg['To'] = ";".join(recipients)
            # msg.attach(MIMEText(content, 'text'))
            msg.attach(MIMEText(content, 'html'))
            server.sendmail(self._smtp_sender, recipients, msg.as_string())
            server.close()

    def send_hand_future_activation_mail(self, recipients: List[str], activation_code: str, subject: str = None,
                                         kind: str = "html"):
        if kind == "html":
            with open(os.path.join(CONFIG_DIR, "template.html"), 'r') as f:
                content = f.read() \
                    .replace("{{code}}", activation_code)
        else:
            content = activation_code
        logger.info(f'sending content: {content}')
        self._send_html_mail(f"【{subject or '携手未来'}】验证码: {activation_code}", content, recipients, kind)


if __name__ == '__main__':
    my_mail = MyMail()
    my_mail.send_hand_future_activation_mail(['877210964@qq.com'], "3399", "html")
