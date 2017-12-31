#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, route


class Mail(Controller):
    class Scaffold:
        display_in_list = ['title', 'mail_title', 'touch_event', 'is_enable']
        hidden_in_form = ['name']
        navigation = [{
            'uri': 'admin:mail:mail:reset_mail_list',
            'title': u'重置樣版',
            'use_json': True,
        }]

    @route_menu(list_name=u'system', group=u'郵件寄送', text=u'郵件寄送樣版', sort=701)
    def admin_list(self):
        return scaffold.list(self)

    @route
    def admin_add(self):
        return scaffold.add(self)

    @route
    def admin_edit(self, key):
        return scaffold.edit(self, key)

    @route
    def taskqueue_after_install(self):
        from ..models.config_model import ConfigModel
        ConfigModel.get_or_create_by_name('mail_config')
        return 'done'

    @route
    def admin_reset_mail_list(self):
        m = self.meta.Model
        m.replace_context(
            'send_verification_email',
            'user_request_verified_email',
            u'信箱驗証通知信',
            u'{{ site_name }} 信箱驗証通知信', u'''
            <p>感謝您使用{{ site_name }}會員服務。</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            <p>請於會員資料中回填 Email 驗證碼 : {{ code }} 或點下面連結進行驗証：</p>
            <p>
                <a href="http://{{ domain }}/verification_email.html?u={{ user.key.urlsafe() }}&code={{ code }}">
                http://{{ domain }}/verification_email.html?u={{ user.key.urlsafe() }}&code={{ code }}</a><br /><br />
            </p>
            <p>若您沒有使用過{{ site_name }}服務，請勿理會此封信件。</p>
            <p>如有任何問題，歡迎聯絡我們。</p>
            <p>&nbsp;</p>
            ''')

        m.replace_context(
            'notice_create_user_by_email',
            'after_user_signup',
            u'帳號註冊完成通知信',
            u'{{ site_name }} 帳號註冊完成通知信', u'''
            <p>已完成註冊帳號。</p>
            <p>感謝您註冊本平台的帳號。</p>
            <p>您所註冊的內容如下。</p>
            <p>帳號 ：{{ user.account }}</p>
            ''')

        m.replace_context(
            'send_token_to_reset_password',
            'user_request_email_reset',
            u'忘記密碼通知信',
            u'{{ site_name }} 忘記密碼通知信', u'''
            <p>親愛的 {{ user.name }} 您好:</p>
            <p>您於 {{ now }} 回報無法登入，申請重新設定密碼 <br />
            請您點下面連結進行密碼重新設定： <br /><br />
            <a href="http://{{ domain }}/reset_password.html?token={{ user.rest_password_token }}">
             http://{{ domain }}/reset_password.html?token={{ user.rest_password_token }}</a><br /><br />
            基於安全理由，密碼重設連結將在重設密碼後失效。</p>
            <p>--<br /> 此通知為系統自動發送，若您沒有使用『無法登入』功能，請忽略此信</p>
            ''')

        m.replace_context(
            'order_create_send_to_admin',
            'after_order_checkout',
            u'給管理者訂購通知信',
            u"{{ site_name }} 訂購通知信，來至", u'''
            <p>來至 {{ order.purchaser_name }} 的訂單:</p>
            <table style="color: #000000; font: 13px Verdana;" border="0" width="100%" cellspacing="2" cellpadding="4"><tbody>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂單編號</span></strong></div></td><td>{{ order.order_no }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂購日期</span></strong></div></td><td>{{ now }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">總金額</span></strong></div></td><td>{{ order.total_amount }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂單備註</span></strong></div></td><td>{{ order.message }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">付費方式</span></strong></div></td><td>{{ order.payment_type_object.get().title }}  |  {{ order.payment_status_title }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">寄送方式</span></strong></div></td><td>{{ order.freight_type_object.get().title }}  |  {{ order.freight_status_title }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂單明細</span></strong></div></td><td>{% for item in order.items %}{{ item.title }}<br />{% endfor %}</td></tr></tbody></table>
            ''')

        m.replace_context(
            'order_create_send_to_user',
            'after_order_checkout',
            u'訂購通知信',
            u'{{ site_name }} 訂購通知信', u'''
            <p>親愛的 {{ order.purchaser_name }} 您好:</p>
            <p>感謝您訂購「{{ site_name }}」的商品／服務，為確保訂單權益，請將款項匯入以下轉入帳號；您越早完成繳費，我們就能越快為您寄送商品／啟動服務。</p>
            <p>您的訂單和轉帳資料如下：</p>
            <table style="color: #000000; font: 13px Verdana;" border="0" width="100%" cellspacing="2" cellpadding="4"><tbody>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂單編號</span></strong></div></td><td>{{ order.order_no }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂購日期</span></strong></div></td><td>{{ now }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">付費方式</span></strong></div></td><td>{{ order.payment_type_object.get().title }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">應付金額</span></strong></div></td><td>{{ order.need_pay_amount }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">付款狀態</span></strong></div></td><td>{{ order.freight_type_object.get().title }}</td></tr>
            <tr><td><div align="center"><strong><span style="color: #535353;">訂單明細</span></strong></div></td><td>{% for item in order.items %}{{ item.title }}<br />{% endfor %}</td></tr></tbody></table>''')

        return self.json({
            'message': u'已重置樣板',
            'data': {'result': 'success'}
        })
