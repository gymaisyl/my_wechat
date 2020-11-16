#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
import json
import threading

from flask import request, jsonify

from utils.msg_send import send_msg
from . import ifwsend_blu as ifwsend


@ifwsend.route("/receive_log", methods=["POST"])
def receive_log():
    """
    The device sends logs and the local receives logs
    :return:
    """
    data = json.loads(request.get_data().decode("utf-8"))
    print(data)
    sn = data.get("sn")
    a1 = threading.Thread(target=send_msg, args=(sn, data))
    a1.start()
    # send_msg(sn, log_num)
    return jsonify(status=0, msg="ok")


