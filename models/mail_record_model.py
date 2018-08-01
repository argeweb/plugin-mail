#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.
import time

from argeweb import BasicModel
from argeweb import Fields


class MailRecordModel(BasicModel):
    title = Fields.StringProperty(verbose_name=u'標題', default=u'')
    send_to = Fields.StringProperty(verbose_name=u'發送對象', default=u'')
    cc = Fields.StringProperty(verbose_name=u'發送對象 cc', default=u'')
    content = Fields.RichTextProperty(verbose_name=u'信件內容', default=u'')
    send_date = Fields.DateTimeProperty(verbose_name=u'發送時間', auto_now_add=True)
    send_system = Fields.HiddenProperty(verbose_name=u'發送的系統', default=u'')

    @classmethod
    def replace_context(cls, name, title=None, content=None):
        record = cls.get_or_create_by_name(name)
        record.name = name
        if title:
            record.title = title
        if content:
            record.content = content
        record.put()


