import os

import dotenv

dotenv.load_dotenv()

ENV_SECRET_KEY = os.environ['SECRET_KEY']
ENV_SECURITY_ALGO = os.environ['SECURITY_ALGO']
ENV_MONGO_URI = os.environ['MONGO_URI']

ENV_MAIL_SENDER_ADDRESS = os.environ['MAIL_SENDER_ADDRESS']
ENV_MAIL_SENDER_NAME = os.environ['MAIL_SENDER_NAME']
ENV_MAIL_APP_PASSWORD = os.environ['MAIL_APP_PASSWORD']
ENV_MAIL_SMTP_SERVER = os.environ['MAIL_SMTP_SERVER']
ENV_MAIL_SMTP_PORT = os.environ['MAIL_SMTP_PORT']
