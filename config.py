#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
import logging
import os

from redis import StrictRedis

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AppID = "wxbefc6a7f25b049fe"
AppSecret = "e1c8c7fa48c34e2e6b9b89ddf54b744c"
TemplateId = "kInVOR3WMbf9y3quXp9GBXfh2lPzooprX8DZMofSkz0"

# Store regularly updated access_token value
REDIS_ACCESS_TOKEN = StrictRedis(host='127.0.0.1', port=6379, decode_responses=True, db=1)
# The storage key is the user id and the value is the data of sn
REDIS_USER_SN = StrictRedis(host='127.0.0.1', port=6379, decode_responses=True, db=2)

# URL dictionary for interaction with WeChat official account platform
URL_DICT = {
    "access_token": "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}",
    "user_info": "https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN",
    "send_template": "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}"
}

# TODO -----------------------------Dividing Line-----------------------------


mysql_account = 'root'
mysql_passwd = 'adminxxxx'
mysql_ip = '127.0.0.1'
mysql_port = 3306


class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 1  # js/css长
    SECRET_KEY = 'jypj9KH3bh19LQhaHi9MeH+BKGuYc/iO/tj5hHMB9EMyZkNxLsxPKSd210EoQSAW'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{account}:{password}@{ip}:{port}/reactinfo".format(
        account=mysql_account,
        password=mysql_passwd,
        ip=mysql_ip,
        port=mysql_port)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 50  # fix TimeoutError and QueuePool limit
    SQLALCHEMY_POOL_TIMEOUT = 60
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_MAX_OVERFLOW = 500

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    LOG_LEVEL = logging.DEBUG


class Development(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class Production(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING


class Testing(Config):
    DEBUG = True
    TESTING = True


config = {
    "development": Development,
    "production": Production,
    "test": Testing,
}
