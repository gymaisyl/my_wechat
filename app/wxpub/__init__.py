#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
# TODO This is the interface module for the interaction between the local server and the WeChat official account
from flask import Blueprint

verify_blu = Blueprint("verify", __name__, url_prefix="/")
from . import verify
