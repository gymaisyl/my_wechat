#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""

import requests
from flask import json

from conf.dynamic_config import get_access_token
from config import URL_DICT


def get_all_args(req_dict):
    print(req_dict)
    echostr = req_dict.get("echostr")  # Get random string
    signature = req_dict.get("signature")  # Get the encrypted signature first
    timestamp = req_dict.get("timestamp")  # Get timestamp
    nonce = req_dict.get("nonce")  # Get random number
    return echostr, signature, timestamp, nonce


def get_user_info(appid, open_id):
    access_token = get_access_token()
    rp = requests.get(URL_DICT.get("user_info").format(access_token, open_id))
    rp_data = json.loads(rp.text)
    print(rp_data)
    if rp_data.get('errcode') or not access_token:
        return {'nickname': '用户'}
    return rp_data
