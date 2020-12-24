import os

class Config:
    SECRET_KEY = '11111111'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'vadimsher83@gmail.com'
    MAIL_PASSWORD = 'xhzhtbxvchffalbs'
    ERROR_404_HELP = False

