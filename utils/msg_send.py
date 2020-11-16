#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
import time

import requests
from flask import json

from conf.dynamic_config import get_access_token
from config import URL_DICT, TemplateId
from models.ifw import UserSn

access_token = get_access_token()


def get_touser(sn):
    """
     Obtain the corresponding bound user according to the sn number
     :return:
    """
    user_sn = UserSn.query.filter(UserSn.sn == sn).first()
    if user_sn:
        touser = user_sn.openid
    else:
        return False, ""
    return True, touser


def get_data(data):
    """
    Construct the data data that needs to be sent according to data
    :param data:
    :return:
    """
    first = "尊敬的用户"
    info = "当前账户绑定的设备通知信息如下"
    key1 = data.get("level")
    key2 = data.get("log_num")
    key3 = "网页端"
    datas = {

        "first": {

            "value": first,

            "color": "#173177"

        },
        "info": {

            "value": info,

            "color": "#173177"

        },
        "key1": {

            "value": key1,

            "color": "#ff0000"

        },
        "key2": {

            "value": key2,

            "color": "#ff0000"

        },
        "key3": {

            "value": key3,

            "color": "#173177"

        }
    }
    return datas


def send_msg(sn, data):
    """
    Send template message (alarm log) to WeChat official account regularly
    :return:
    """
    url = URL_DICT.get("send_template").format(access_token)
    flag, touser = get_touser(sn)
    datas = get_data(data)
    if flag:
        data = {

            "touser": touser,

            "template_id": TemplateId,

            "data": datas

        }

        s = requests.post(url, json.dumps(data))
        print(s.content)

