#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.
import time

from argeweb import BasicModel
from argeweb import Fields


class MailModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(verbose_name=u'樣版名稱')
    mail_title = Fields.StringProperty(verbose_name=u'信件標題')
    mail_content = Fields.RichTextProperty(verbose_name=u'信件內容')
    touch_event = Fields.StringProperty(verbose_name=u'觸發時機', default=u'after_user_signup', choices=[
        'after_user_signup',
        'after_order_checkout',
        'after_user_verified_email',
        'after_user_verified_mobile',
        'after_user_verified_both',
        'user_request_verified_email',
        'user_request_email_reset',
    ], choices_text={
        'after_user_signup': u'使用者註冊後',
        'after_order_checkout': u'訂單建立後',
        'after_user_verified_email': u'使用者驗証手機後',
        'after_user_verified_mobile': u'使用者驗証手機後',
        'after_user_verified_both': u'使用者驗証信箱、手機後',
        'user_request_verified_email': u'使用者請求驗証信箱',
        'user_request_email_reset': u'使用者請求重設密碼',
    })
    is_enable = Fields.BooleanProperty(verbose_name=u'啟用觸發', default=True)
    send_to_admin = Fields.BooleanProperty(verbose_name=u'寄送給管理者', default=False)

    @classmethod
    def replace_context(cls, name, touch_event=None, title=None, mail_title=None, mail_content=None):
        record = cls.get_or_create_by_name(name)
        record.name = name
        if title:
            record.title = title
        if mail_title:
            record.mail_title = mail_title
        if mail_content:
            record.mail_content = mail_content
        if touch_event:
            record.touch_event = touch_event
        record.put()


