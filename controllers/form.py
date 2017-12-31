#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from argeweb import auth, add_authorizations, require_post
from argeweb import Controller, scaffold, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from ..models.config_model import ConfigModel


class Form(Controller):
    class Meta:
        default_view = 'json'

    class Scaffold:
        display_in_form = ['user_name', 'account', 'is_enable', 'sort', 'created', 'modified']

    @route
    @require_post
    @route_with(name='form:mail:send')
    def send(self):
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.meta.change_view('json')
        self.context['data'] = {'result': 'failure'}

        to = self.params.get_string('to')
        subject = self.params.get_string('subject')
        content = self.params.get_string('content')
        if subject is u'' or content is u'':
            return self.json_failure_message(u'請輸入標題及內容')

        from ..mail import Mail
        m = Mail(self)
        return_msg = []

        a = m.send(
            send_to=to,
            subject=self.params.get_string('subject'),
            content=self.params.get_string('content'),
            cc=self.params.get_string('cc')
        )
        return_msg.append({
            'message': a['message'],
            'status': a['status']
        })
        self.json(return_msg)
