#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
@license : Copyright(C), ChangYang Technology Co. Ltd.
"""
from flask import request
from xml.dom.minidom import parseString

from . import verify_blu as verify
from wechatpy.utils import check_signature
from utils.get_wechat_args import get_all_args
from utils.msg_handler import Handler
from wechatpy.exceptions import InvalidSignatureException


@verify.route('/', methods=["POST", "GET"])
def wechat_verify():
    """
    Used to process the verification of the WeChat server to the backend, GET method.
    :return:
    :return:
    """
    if request.method == "POST":
        msg = request.data.decode()
        dom = parseString(msg)
        print("MsgType:", dom.getElementsByTagName('MsgType')[0].childNodes[0].data)
        print("ToUserName:", dom.getElementsByTagName('ToUserName')[0].childNodes[0].data)  # recv
        print("FromUserName:", dom.getElementsByTagName('FromUserName')[0].childNodes[0].data)  # send
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return post_handler(dom)
    else:
        # get param
        rq_dict = request.args
        if len(rq_dict) == 0:
            return ""
        tuple_args = get_all_args(rq_dict)
        token = "123456"  # it is up to you
        try:
            check_signature(token, tuple_args[1], tuple_args[2], tuple_args[3])
        except InvalidSignatureException as e:
            print(e)
            return ''
        else:
            return tuple_args[0]


def post_handler(dom):
    appid = ""
    msg_type = dom.getElementsByTagName('MsgType')[0].childNodes[0].data
    handler = Handler(appid, msg_type, dom)
    return handler.run()
