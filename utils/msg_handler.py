#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
import time

import xmltodict

from app import db
from config import REDIS_USER_SN
from models.ifw import UserSn
from utils.get_wechat_args import get_user_info


class GetParam(object):
    """
    获取dom中的各个参数
    """

    def __init__(self, param, dom):
        self.param = param  # 获取什么
        self.dom = dom
        self.md = {
            'ToUserName': self.to_username,
            'FromUserName': self.from_username,
            'CreateTime': self.create_time,
            'MsgType': self.msg_type,
            'Event': self.event,
            'EventKey': self.event_key,
            'Ticket': self.ticket,
            "Content": self.content
        }

    def get_param(self):
        param = self.md[self.param]()
        return param

    def msg_type(self):
        """
        获取消息类型：event、text
        :return:
        """
        msg_type = self.dom.getElementsByTagName('MsgType')[0].childNodes[0].data
        return msg_type

    def to_username(self):
        """
        获取开发者微信号
        :return:
        """
        to_username = self.dom.getElementsByTagName('ToUserName')[0].childNodes[0].data
        return to_username

    def from_username(self):
        """
        获取发送方帐号（一个OpenID）
        :return:
        """
        from_username = self.dom.getElementsByTagName('FromUserName')[0].childNodes[0].data
        return from_username

    def create_time(self):
        create_time = self.dom.getElementsByTagName('CreateTime')[0].childNodes[0].data
        return create_time

    def event(self):
        event = self.dom.getElementsByTagName('Event')[0].childNodes[0].data
        return event

    def event_key(self):
        event_key = self.dom.getElementsByTagName('EventKey')[0].childNodes[0].data
        return event_key

    def ticket(self):
        ticket = self.dom.getElementsByTagName('Ticket')[0].childNodes[0].data
        return ticket

    def content(self):
        content = self.dom.getElementsByTagName('Content')[0].childNodes[0].data
        return content


class Handler:
    # 普通消息
    def __init__(self, appid, m_type, dom):
        self.appid = appid
        self.md = {
            'text': self.text,
            'link': self.link,
            'event': self.event,
            'SCAN': self.scan,
            'CLICK': self.click,
            'subscribe': self.subscribe,
            'unsubscribe': self.unsubscribe,
        }
        self.type = m_type
        self.dom = dom

    def run(self):
        if self.type not in list(self.md.keys()):
            return self.error_md()
        data = self.md[self.type]()
        return data

    def error_md(self):
        to_username = GetParam("ToUserName", self.dom).get_param()
        from_username = GetParam("FromUserName", self.dom).get_param()
        create_time = GetParam("CreateTime", self.dom).get_param()
        dict_msg = {
            'xml': {'ToUserName': from_username, 'FromUserName': to_username, 'CreateTime': create_time,
                    'MsgType': 'text',
                    'Content': "请输入'绑定(1)/解绑(0)'进行后续操作，其他操作无效"}}

        xml = xmltodict.unparse(dict_msg, encoding='utf-8')
        return xml

    def temp_md(self):

        return "ok"

    def text(self):
        """
        text
        :return:
        """
        to_username = GetParam("ToUserName", self.dom).get_param()
        from_username = GetParam("FromUserName", self.dom).get_param()
        msg = GetParam("Content", self.dom).get_param()
        create_time = str(int(time.time()))
        open_id = GetParam("FromUserName", self.dom).get_param()
        user_info = get_user_info(self.appid, open_id)
        if not user_info:
            return ''

        sn = REDIS_USER_SN.get(from_username)

        if "绑定" in msg or ("1" in msg):
            exist_user = UserSn.query.filter(UserSn.openid == from_username).first()
            if exist_user:
                # if exist_sn.openid == from_username:
                content = '亲爱的%s，当前账户已经和设备%s绑定，请勿重复操作' % (user_info["nickname"], exist_user.sn)
                # else:
                #     content = '亲爱的%s，设备%s已经被其他用户绑定，无法和当前账户绑定' % (user_info["nickname"], sn)
            else:
                if not sn:
                    content = "绑定信息已失效，请重新扫描设备二维码进行设备绑定"
                else:
                    exist_sn = UserSn.query.filter(UserSn.openid == sn).first()
                    if exist_sn:
                        # if exist_sn.openid == from_username:
                        content = '亲爱的%s，当前设备%s已经被其他用户绑定，无法进行绑定操作' % (user_info["nickname"], sn)
                    else:
                        user_sn = UserSn()
                        user_sn.openid = from_username
                        user_sn.sn = sn
                        db.session.add(user_sn)
                        try:
                            db.session.commit()
                            content = '亲爱的%s，当前账户与设备%s绑定成功' % (user_info["nickname"], sn)
                            REDIS_USER_SN.delete(from_username)
                        except Exception as e:
                            db.session.rollback()
                            content = '亲爱的%s，当前账户与设备%s绑定失败' % (user_info["nickname"], sn)

            dict_msg = {
                'xml': {'ToUserName': from_username, 'FromUserName': to_username, 'CreateTime': create_time,
                        'MsgType': 'text',
                        'Content': content}}
            xml = xmltodict.unparse(dict_msg, encoding='utf-8')
            return xml
        elif "解绑" in msg or ("2" in msg):
            sn = UserSn.query.filter(UserSn.openid == from_username).first()
            if not sn:
                content = "当前用户未绑定任何设备，无法进行解绑操作"
            else:
                UserSn.query.filter(UserSn.openid == from_username).delete()
                try:
                    db.session.commit()
                    content = '亲爱的%s，当前账户与设备%s解绑成功' % (user_info["nickname"], sn.sn)
                except Exception as e:
                    db.session.rollback()
                    content = '亲爱的%s，当前账户与设备%s解绑失败' % (user_info["nickname"], sn.sn)
        elif "设备" in msg or ("3" in msg):
            sn = UserSn.query.filter(UserSn.openid == from_username).first()
            if not sn:
                content = "当前账号未绑定任何设备"
            else:
                content = '亲爱的%s，当前账户绑定的设备为：%s' % (user_info["nickname"], sn.sn)

        else:
            content = "请按照如下提示进行操作\n【1】绑定设备\n【2】解绑设备\n【3】当前账号绑定设备查询"
        dict_msg = {
            'xml': {'ToUserName': from_username, 'FromUserName': to_username, 'CreateTime': create_time,
                    'MsgType': 'text',
                    'Content': content}}

        xml = xmltodict.unparse(dict_msg, encoding='utf-8')
        return xml

    # 事件推送
    def event(self):
        """
        事件类型
        :return:
        subscribe 关注/取消关注事件
            扫描带参数二维码事件 eventkey
            qrscene_ 用户未关注时，进行关注后的事件推送
        SCAN 扫描带参数二维码事件
        """
        events = GetParam("Event", self.dom).get_param()
        if events not in list(self.md.keys()):
            return self.temp_md()

        data = self.md[events]()
        return data

    def subscribe(self, welcome_content=None):
        to_username = GetParam("ToUserName", self.dom).get_param()
        from_username = GetParam("FromUserName", self.dom).get_param()
        create_time = GetParam("CreateTime", self.dom).get_param()
        open_id = GetParam("FromUserName", self.dom).get_param()
        user_info = get_user_info(self.appid, open_id)
        if not user_info:
            return ''
        try:
            EventKey = GetParam("EventKey", self.dom).get_param()  # 扫描带参数的二维码的参数值
        except Exception as e:
            EventKey = None
            pass
        if EventKey:
            if "qrscene_" in EventKey:
                EventKey = EventKey[8:]
            REDIS_USER_SN.set(from_username, EventKey, ex=3600)  # openid和sn一一对应，有效期为1h
            pass
        exist_content = '感谢关注！\n请按照如下提示进行操作\n【1】绑定设备\n【2】解绑设备\n【3】当前账号绑定设备查询'
        welcome_content = welcome_content if welcome_content else exist_content
        content = '亲爱的%s，%s' % (user_info["nickname"], welcome_content)
        dict_msg = {
            'xml': {'ToUserName': from_username, 'FromUserName': to_username, 'CreateTime': create_time,
                    'MsgType': 'text',
                    'Content': content}}

        xml = xmltodict.unparse(dict_msg, encoding='utf-8')
        return xml

    def unsubscribe(self):
        """
        After unsubscribe, Unbind users and devices
        :return:
        """
        from_username = GetParam("FromUserName", self.dom).get_param()
        sn = UserSn.query.filter(UserSn.openid == from_username).first()
        if not sn:
            pass
        else:
            UserSn.query.filter(UserSn.openid == from_username).delete()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()

        dict_msg = {
            'xml': {'Content': "ok"}}
        xml = xmltodict.unparse(dict_msg, encoding='utf-8')
        return xml

    def link(self):
        """
        :return:
        """

    def scan(self):
        """
        :return:
        """
        welcome_content = "欢迎回来！"
        return self.subscribe()

    def click(self):
        pass
