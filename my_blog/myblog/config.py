import os

class Config:
  con = f'mysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DB")}'
  SECRET_KEY =os.getenv("APP_SECRET_KEY")
  SQLALCHEMY_DATABASE_URI = con
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.getenv("EMAIL_USER")
  MAIL_PASSWORD = os.getenv("EMAIL_PASS")