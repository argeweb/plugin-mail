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

    class Scaffold:
        display_in_list = ['title', 'mail_title']
        hidden_in_form = ['name']
        excluded_in_form = ()

    @route_menu(list_name=u'backend', text=u'郵件寄送樣版', sort=701, group=u'互動項目', need_hr=True)
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

        m.replace_context('order_create_send_to_user', u'訂購通知信', u"{{ site_name }} 訂購通知信", u'''
<p>親愛的 {{ purchaser_name }} 您好:</p>
<p>感謝您訂購「{{ site_name }}」的商品／服務，為確保訂單權益，請將款項匯入以下轉入帳號；您越早完成繳費，我們就能越快為您寄送商品／啟動服務。</p>
<p>您的訂單和轉帳資料如下：</p>
<table style="color: #000000; font: 13px Verdana;" border="0" width="100%" cellspacing="2" cellpadding="4"><tbody>
<tr><td><div align="center"><strong><span style="color: #535353;">訂單編號</span></strong></div></td><td>{{ order_no }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">訂購日期</span></strong></div></td><td>{{ created }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">付費方式</span></strong></div></td><td>{{ payment_type_title }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">付款狀態</span></strong></div></td><td>{{ payment_status_text }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">訂單明細</span></strong></div></td><td>{{ order_items }}</td></tr></tbody></table>''')

        m.replace_context('order_create_send_to_admin', u'訂購通知信', u"{{ site_name }} 訂購通知信，來至", u'''
<p>來至 {{ purchaser_name }} 的訂單:</p>
<table style="color: #000000; font: 13px Verdana;" border="0" width="100%" cellspacing="2" cellpadding="4"><tbody>
<tr><td><div align="center"><strong><span style="color: #535353;">訂單編號</span></strong></div></td><td>{{ order_no }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">訂購日期</span></strong></div></td><td>{{ created }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">總金額</span></strong></div></td><td>{{ total_amount }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">訂單備註</span></strong></div></td><td>{{ message }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">付費方式</span></strong></div></td><td>{{ payment_type_title }}  |  {{ payment_status_text }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">寄送方式</span></strong></div></td><td>{{ freight_type_title }}  |  {{ freight_status_text }}</td></tr>
<tr><td><div align="center"><strong><span style="color: #535353;">訂單明細</span></strong></div></td><td>{{ order_items }}</td></tr></tbody></table>''')
        return u'已重置樣板'