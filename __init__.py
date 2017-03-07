#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import ViewDatastore
from mail import Mail, MailConfigModel


__all__ = (
    'Mail'
    'MailConfigModel'
)

plugins_helper = {
    'title': u'郵件樣版與寄送設定',
    'desc': u'與郵件有關的相關設定，並可建立郵件樣版',
    'controllers': {
        'mail': {
            'group': u'郵件樣版管理',
            'actions': [
                {'action': 'list', 'name': u'郵件樣版'},
                {'action': 'add', 'name': u'新增樣版'},
                {'action': 'edit', 'name': u'編輯樣版'},
                {'action': 'view', 'name': u'檢視樣版'},
                {'action': 'delete', 'name': u'刪除樣版'},
            ]
        },
        'mail_config': {
            'group': u'郵件設定',
            'actions': [
                {'action': 'config', 'name': u'郵件相關設定'},
            ]
        },
    }
}
