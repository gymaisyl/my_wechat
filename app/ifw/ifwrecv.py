#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""

from flask import jsonify

from conf.dynamic_config import get_access_token
from . import ifwrecv_blu as ifwrecv


@ifwrecv.route("/get_access_token", methods=["GET"])
def access_token():
    """
    The device requests the accesstoken value
    :return:
    """
    access_token = get_access_token()
    data = {
        "access_token": access_token
    }
    return jsonify(status=0, msg="ok", data=data)
