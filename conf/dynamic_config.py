#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
# Store, get dynamic configuration
import time

import requests

from config import AppID, AppSecret, URL_DICT, REDIS_ACCESS_TOKEN


def generate_access_token():
    """
   Only support update_access_token() call
    :return:
    """
    appid = AppID
    appsercet = AppSecret
    url = URL_DICT.get("access_token").format(appid, appsercet)
    req = requests.get(url=url).json()
    access_token = req.get("access_token")
    print(access_token)
    return access_token


def update_access_token():
    """
    Update the access_token data of redis
     The current validity period of access_token is conveyed by the returned expire_in,
     The current value is within 7200 seconds. The central control server needs to refresh the new access_token in
     advance according to this valid time.
     :return:
     Timed task call
    """
    while True:
        access_token = generate_access_token()
        REDIS_ACCESS_TOKEN.set("access_token", access_token)
        time.sleep(6600)


def get_access_token():
    """
    How to get access_token on the device or the machine
    :return:
    """
    access_token = REDIS_ACCESS_TOKEN.get("access_token")
    return access_token
