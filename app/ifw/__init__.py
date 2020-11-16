#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
# TODO This is the interface module for the interaction between the local server and the device
from flask import Blueprint

ifwrecv_blu = Blueprint("ifwrecv", __name__, url_prefix="/api/ifw/ifwrecv")
ifwsend_blu = Blueprint("ifwsend", __name__, url_prefix="/api/ifw/ifwsend")
from . import ifwrecv, ifwsend
