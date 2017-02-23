#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search


class Mail(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 50

    class Scaffold:
        display_in_list = ['title', 'mail_title']
        hidden_in_form = ['name']
        excluded_in_form = ()

    @route_menu(list_name=u'backend', text=u'郵件寄送樣版', sort=9941, group=u'系統設定', need_hr=True)
    def admin_list(self):
        return scaffold.list(self)

    @route
    def admin_add(self):
        return scaffold.add(self)

    @route
    def admin_edit(self, key):
        return scaffold.edit(self, key)

    @route
    def admin_reset_mail_list(self):
        m = self.meta.Model
        m.replace_context('notice_create_user_by_email', u'帳號註冊完成通知信', u"{{ site_name }} 帳號註冊完成通知信", u'''
<p>已完成註冊帳號。</p>
<p>感謝您註冊本平台的帳號。</p>
<p>您所註冊的內容如下。</p>
<p>E-Mail ：{{ email }}</p>
''')

        m.replace_context('send_token_to_reset_password', u'忘記密碼通知信', u"{{ site_name }} 忘記密碼通知信", u'''
<p>親愛的 {{ name }} 您好:</p>
<p>您於 {{ created_date }} 回報無法登入，申請重新設定密碼 <br />
請您點下面連結進行密碼重新設定： http://{{ domain }}/reset_password.html?token={{ token }} <br /><br />
基於安全理由，密碼重設連結將在重設密碼後失效。</p>
<p>--<br /> 此通知為系統自動發送，若您沒有使用『無法登入』功能，請忽略此信</p>
''')
        return u'已重置樣板'
