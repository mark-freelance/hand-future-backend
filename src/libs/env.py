import os

import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
SECURITY_ALGO = os.environ['SECURITY_ALGO']

DATABASE_MONGO_URI = os.environ['MONGO_URI']
DATABASE_DB_NAME = os.environ['DATABASE_DB_NAME']

SMTP_USER = os.environ['SMTP_USER']
SMTP_SENDER = os.environ['SMTP_SENDER']
SMTP_SENDER_NAME = os.environ['SMTP_SENDER_NAME']
SMTP_PSWD = os.environ['SMTP_PSWD']
SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = int(os.environ['SMTP_PORT'])

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ['NOTION_DATABASE_ID']
