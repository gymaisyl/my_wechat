#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
from app import db
from models.basemodel import BaseModel


class UserSn(db.Model, BaseModel):
    """
    One-to-one correspondence between official account users and sn
    """
    __tablename__ = "user_sn"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, comment="主键id")
    openid = db.Column(db.String(255), nullable=False, unique=True, comment="openID")
    sn = db.Column(db.String(255), nullable=False, unique=True, comment="设备sn")
